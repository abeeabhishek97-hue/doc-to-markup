import streamlit as st
import requests
import base64

API_URL = "http://localhost:9000/convert"

st.set_page_config(
    page_title="Document to Markdown Converter",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document to Markdown Converter")
st.caption("Upload a PDF or image to convert it to clean Markdown.")
st.divider()

# ── Upload ──────────────────────────────────────────────
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
                f'<a href="data:application/pdf;base64,{b64}" download="{uploaded_file.name}">'
                f'Download instead</a></p>'
                f'</object>',
                unsafe_allow_html=True
            )
        else:
            st.image(uploaded_file, use_container_width=True)

    st.divider()
    convert_clicked = st.button("⚡ Convert to Markdown", type="primary", use_container_width=True)

    with col2:
        st.subheader("📝 Markdown Output")

        if convert_clicked:
            with st.spinner("Converting... this may take up to 2 minutes on first run."):
                try:
                    uploaded_file.seek(0)
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(API_URL, files=files, timeout=120)
                    response.raise_for_status()
                    markdown_text = response.json()["markdown"]

                except requests.exceptions.ConnectionError:
                    markdown_text = """# Sample Heading

This is **dummy output** — backend not reachable.

## Section 2

- Item one
- Item two
- Item three

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
"""
                    st.warning("⚠️ Backend not reachable — showing dummy output.")

                except requests.exceptions.HTTPError as e:
                    st.error(f"Backend error: {e}")
                    markdown_text = None

                except Exception as e:
                    st.error(f"Unexpected error: {e}")
                    markdown_text = None

            if markdown_text:
                st.session_state["markdown"] = markdown_text

        if "markdown" in st.session_state:
            md = st.session_state["markdown"]
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