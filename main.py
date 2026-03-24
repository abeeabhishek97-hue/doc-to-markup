from PIL import Image
from ocr.ocr_engine import run_ocr          # your Day 3 module
from layout.layout_detector import load_model, run_layout_detection
import json

# Load model once at startup (slow first time — downloads ~500MB)
processor, model = load_model()

def process_page(image_path: str) -> list[dict]:
    image = Image.open(image_path).convert("RGB")

    # OCR output from Day 3: list of {text, bbox}
    ocr_results = run_ocr(image_path)
    words = [r["text"] for r in ocr_results]
    bboxes = [r["bbox"] for r in ocr_results]  # [[x1,y1,x2,y2], ...]

    layout = run_layout_detection(image, words, bboxes, processor, model)
    return layout

if __name__ == "__main__":
    result = process_page("sample_docs/test_page.png")
    print(json.dumps(result, indent=2))