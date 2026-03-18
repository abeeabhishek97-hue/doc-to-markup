# src/ingestion/document_loader.py

import fitz          # PyMuPDF
from PIL import Image
import numpy as np


# Step 3 — PDF Loader
def load_pdf(filepath: str) -> list:
    doc = fitz.open(filepath)
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=150)
        pages.append(pix)
    return pages


# Step 4 — Image Loader
def load_image(filepath: str) -> Image.Image:
    return Image.open(filepath).convert("RGB")


# Step 5 — Normalize to Tensor
def to_tensor(image: Image.Image) -> np.ndarray:
    return np.array(image.resize((1024, 1024))) / 255.0


# Step 6 — Unified Loader
def load_document(filepath: str) -> list:
    if filepath.endswith(".pdf"):
        pages = load_pdf(filepath)
        # convert pixmaps to PIL then tensor
    else:
        img = load_image(filepath)
        return [to_tensor(img)]