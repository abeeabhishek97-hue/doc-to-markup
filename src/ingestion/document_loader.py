# src/ingestion/document_loader.py

import fitz          # PyMuPDF
from PIL import Image
import numpy as np


def load_pdf(filepath: str) -> list:
    """Load PDF pages as PIL Images."""
    doc = fitz.open(filepath)
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=150)
        # Convert pixmap → PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)
    return pages


def load_image(filepath: str) -> Image.Image:
    """Load a single image file as PIL Image."""
    return Image.open(filepath).convert("RGB")


def to_tensor(image: Image.Image) -> np.ndarray:
    """Normalize PIL Image to numpy array."""
    return np.array(image.resize((1024, 1024))) / 255.0


def load_document(filepath: str) -> list:
    """
    Unified loader — returns a list of PIL Images, one per page.
    Works for both PDF and image files.
    """
    if filepath.lower().endswith(".pdf"):
        return load_pdf(filepath)        # ← was missing return
    else:
        img = load_image(filepath)
        return [img]                     # ← return PIL Image, not tensor
    