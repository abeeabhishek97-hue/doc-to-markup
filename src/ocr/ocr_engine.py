# src/ocr/ocr_engine.py

import pytesseract
import numpy as np
from PIL import Image

# Point to Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_boxes(image) -> list[dict]:
    """
    OCR using Tesseract.
    Accepts PIL Image or numpy array.
    Returns list of dicts with text, bbox, and confidence.
    """
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT,
        config='--psm 4'    # ← changed from 3 to 4 (single column mode)
    )

    output = []
    for i, text in enumerate(data["text"]):
        if text.strip() and int(data["conf"][i]) > 30:
            output.append({
                "text": text.strip(),
                "bbox": [
                    data["left"][i],
                    data["top"][i],
                    data["left"][i] + data["width"][i],
                    data["top"][i] + data["height"][i]
                ],
                "confidence": int(data["conf"][i]) / 100.0
            })
    return output