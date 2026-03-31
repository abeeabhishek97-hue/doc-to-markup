# src/api/routes.py

import os
import tempfile
import asyncio

from fastapi import APIRouter, UploadFile, File, HTTPException
from src.api.schemas import ConvertResponse, RegionResult

from src.ingestion.document_loader import load_document
from src.ocr.ocr_engine import extract_text_boxes
from src.layout.layout_detector import run_layout_detection, load_model
from src.generation.markdown_generator import generate_markdown
from src.generation.postprocessor import postprocess
from src.generation.validator import validate_markdown

router = APIRouter()

# Load layout model once at startup — not on every request
_processor, _model = load_model()


@router.post("/convert", response_model=ConvertResponse)
async def convert_document(file: UploadFile = File(...)):

    # ── Validate file type ────────────────────────────────────────────
    allowed = ["application/pdf", "image/jpeg", "image/png"]
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Upload a PDF or image."
        )

    # ── Read and check file ───────────────────────────────────────────
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # ── Save to temp file ─────────────────────────────────────────────
    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # ── Step 1: Ingestion ─────────────────────────────────────────
        pages = await asyncio.to_thread(load_document, tmp_path)

        all_regions = []

        # ── Step 2: OCR + Layout per page ─────────────────────────────
        for page_image in pages:

            # OCR — returns list of {text, bbox, confidence}
            ocr_results = await asyncio.to_thread(
                extract_text_boxes, page_image
            )

            if not ocr_results:
                continue

            # Extract words and bboxes for layout model
            words  = [r["text"] for r in ocr_results]
            bboxes = [r["bbox"] for r in ocr_results]

            # Layout detection
            regions = await asyncio.to_thread(
                run_layout_detection,
                page_image,    # PIL image
                words,
                bboxes,
                _processor,
                _model
            )

            # Attach confidence from OCR to each region
            for i, region in enumerate(regions):
                region["confidence"] = float(
                    ocr_results[i]["confidence"]
                ) if i < len(ocr_results) else 0.0

            all_regions.extend(regions)

        # ── Step 3: Generate Markdown ─────────────────────────────────
        raw_markdown = generate_markdown(all_regions)

        # ── Step 4: Post-process ──────────────────────────────────────
        clean_markdown = postprocess(raw_markdown)

        # ── Step 5: Validate ──────────────────────────────────────────
        is_valid, message = validate_markdown(clean_markdown)

        # ── Step 6: Build region results ──────────────────────────────
        region_results = [
            RegionResult(
                label=r.get("label", "unknown"),
                text=r.get("text", "")[:200],
                confidence=float(r.get("confidence", 0.0)),
            )
            for r in all_regions
        ]

        avg_confidence = round(
            sum(r.confidence for r in region_results) / len(region_results), 2
        ) if region_results else 0.0

        return ConvertResponse(
            markdown=clean_markdown,
            confidence=avg_confidence,
            regions=region_results,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        os.unlink(tmp_path)
        