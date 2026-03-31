# src/ocr/ocr_engine.py

import pytesseract
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_boxes(image) -> list[dict]:
    """
    OCR using Tesseract.
    Accepts PIL Image or numpy array.
    Returns list of dicts with text, bbox, and confidence.
    """
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    # Upscale image for better OCR accuracy
    w, h = image.size
    if w < 2000:
        scale = 2000 / w
        image = image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT,
        config='--psm 6 --oem 3'  # psm 6 = uniform block of text, oem 3 = best engine
    )

    output = []
    for i, text in enumerate(data["text"]):
        if text.strip() and int(data["conf"][i]) > 20:  # lowered threshold
            output.append({
                "text": text.strip(),
                "bbox": [
                    data["left"][i],
                    data["top"][i],
                    data["left"][i] + data["width"][i],
                    data["top"][i] + data["height"][i]
                ],
                "confidence": int(data["conf"][i]) / 100.0,
                "block_num": data["block_num"][i],
                "line_num":  data["line_num"][i],
                "par_num":   data["par_num"][i],
            })
    return output