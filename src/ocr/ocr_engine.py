from paddleocr import PaddleOCR

def get_ocr_engine(lang: str = "en") -> PaddleOCR:
    return PaddleOCR(use_angle_cls=True, lang=lang, use_gpu=False)
import numpy as np

def extract_text_with_boxes(ocr_engine, image_array: np.ndarray) -> list[dict]:
    results = ocr_engine.ocr(image_array, cls=True)
    output = []
    for line in results[0]:
        bbox, (text, confidence) = line
        output.append({
            "text": text,
            "bbox": bbox,       # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            "confidence": confidence
        })
    return output
import pytesseract
from PIL import Image

def extract_text_tesseract(image_array: np.ndarray) -> list[dict]:
    pil_img = Image.fromarray(image_array)
    data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
    # parse and return in same format as PaddleOCR output
    ...