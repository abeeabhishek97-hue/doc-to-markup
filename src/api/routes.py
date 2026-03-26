# src/api/routes.py
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.api.schemas import ConvertResponse, RegionResult

router = APIRouter()

@router.post("/convert", response_model=ConvertResponse)
async def convert_document(file: UploadFile = File(...)):

    # Validate file type
    allowed = ["application/pdf", "image/jpeg", "image/png"]
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Upload a PDF or image."
        )

    # Read the file
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # ── DUMMY OUTPUT (will be replaced on Day 12) ────────────────────────
    dummy_markdown = f"""# Sample Document

This is a dummy Markdown response for **{file.filename}**.

## Introduction

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
This output will be replaced with real content on Day 12.

## Key Points

- Point one about the document
- Point two about the document
- Point three about the document

## Results

| Column A | Column B | Column C |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |

## Code Example
```python
def hello():
    print("Hello from the converter!")
```
"""

    dummy_regions = [
        RegionResult(label="heading",   text="Sample Document",  confidence=0.97),
        RegionResult(label="paragraph", text="Lorem ipsum...",   confidence=0.89),
        RegionResult(label="list",      text="Point one...",     confidence=0.91),
        RegionResult(label="table",     text="Column A...",      confidence=0.85),
        RegionResult(label="code",      text="def hello()...",   confidence=0.93),
    ]

    return ConvertResponse(
        markdown=dummy_markdown,
        confidence=0.91,
        regions=dummy_regions
    )