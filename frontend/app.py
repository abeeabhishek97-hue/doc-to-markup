# frontend/app.py

import streamlit as st
import base64
import sys
import os

# ── Add project root to path ──────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import tempfile
import fitz
import numpy as np
from PIL import Image

from src.ocr.ocr_engine import extract_text_boxes
from src.layout.layout_detector import run_layout_detection
from src.generation.markdown_generator import generate_markdown
from src.generation.postprocessor import postprocess
from src.generation.validator import validate_markdown

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Document to Markdown Converter",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document to Markdown Converter")
st.caption("Upload a PDF or image to convert it to clean Markdown.")
st.divider()


# ── Pipeline ──────────────────────────────────────────────────────────────────

def load_pages(file_bytes: bytes, file_type: str) -> list:
    """Convert uploaded file to list of PIL Images."""
    if file_type == "application/pdf":
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = []
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pages.append(img)
        return pages
    else:
        from io import BytesIO
        img = Image.open(BytesIO(file_bytes)).convert("RGB")
        return [img]


def run_pipeline(file_bytes: bytes, file_type: str) -> dict:
    """
    Run the full conversion pipeline.
    Returns dict with markdown, confidence, regions.
    """
    pages      = load_pages(file_bytes, file_type)
    all_regions = []

    for page_image in pages:
        # OCR
        ocr_results = extract_text_boxes(page_image)
        if not ocr_results:
            continue

        words  = [r["text"] for r in ocr_results]
        bboxes = [r["bbox"]  for r in ocr_results]

        # Layout detection
        regions = run_layout_detection(
            page_image,
            words,
            bboxes,
            ocr_results=ocr_results
        )

        # Attach confidence
        for i, region in enumerate(regions):
            region["confidence"] = float(
                ocr_results[i]["confidence"]
            ) if i < len(ocr_results) else 0.9

        all_regions.extend(regions)

    # Generate Markdown
    raw_markdown   = generate_markdown(all_regions)
    clean_markdown = postprocess(raw_markdown)
    is_valid, msg  = validate_markdown(clean_markdown)

    avg_confidence = round(
        sum(r.get("confidence", 0.9) for r in all_regions) / len(all_regions), 2
    ) if all_regions else 0.0

    return {
        "markdown":   clean_markdown,
        "confidence": avg_confidence,
        "regions":    all_regions,
        "valid":      is_valid,
        "pages":      len(pages),
    }


# ── Upload ────────────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader(
    "Drag & drop or click to upload",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📎 Original Document")

        if uploaded_file.type == "application/pdf":
            pdf_bytes = uploaded_file.read()
            uploaded_file.seek(0)
            b64 = base64.b64encode(pdf_bytes).decode()
            st.markdown(
                f'<object data="data:application/pdf;base64,{b64}" '
                f'type="application/pdf" width="100%" height="600px">'
                f'<p>PDF cannot be displayed. '
                f'<a href="data:application/pdf;base64,{b64}" '
                f'download="{uploaded_file.name}">Download instead</a></p>'
                f'</object>',
                unsafe_allow_html=True
            )
        else:
            st.image(uploaded_file, use_container_width=True)

    st.divider()
    convert_clicked = st.button(
        "⚡ Convert to Markdown",
        type="primary",
        use_container_width=True
    )

    with col2:
        st.subheader("📝 Markdown Output")

        if convert_clicked:
            with st.spinner("Converting... please wait."):
                try:
                    uploaded_file.seek(0)
                    file_bytes = uploaded_file.read()
                    result     = run_pipeline(file_bytes, uploaded_file.type)

                    st.session_state["markdown"]   = result["markdown"]
                    st.session_state["confidence"] = result["confidence"]
                    st.session_state["regions"]    = result["regions"]
                    st.session_state["pages"]      = result["pages"]

                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.pop("markdown", None)

        if "markdown" in st.session_state:
            md       = st.session_state["markdown"]
            conf     = st.session_state.get("confidence", 0.0)
            regions  = st.session_state.get("regions", [])
            pages    = st.session_state.get("pages", 1)

            # ── Metrics ───────────────────────────────────────────────
            m1, m2, m3 = st.columns(3)
            m1.metric("Avg Confidence", f"{conf:.0%}")
            m2.metric("Pages",          pages)
            m3.metric("Regions",        len(regions))

            # ── Low confidence warning ─────────────────────────────
            low_conf = [r for r in regions if float(r.get("confidence", 1.0)) < 0.6]
            if low_conf:
                st.warning(
                    f"⚠️ {len(low_conf)} regions have low confidence "
                    f"(< 60%) — review these sections carefully."
                )

            # ── Markdown output ────────────────────────────────────
            st.markdown(md)
            st.divider()

            with st.expander("🔍 View raw Markdown"):
                st.code(md, language="markdown")

            st.download_button(
                label="⬇ Download .md file",
                data=md,
                file_name="output.md",
                mime="text/markdown",
                use_container_width=True
            )

        else:
            st.info("Click **Convert** to generate Markdown output.")