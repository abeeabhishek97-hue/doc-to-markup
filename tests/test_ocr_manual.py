from src.ingestion import load_document
from src.ocr.ocr_engine import get_ocr_engine, extract_text_with_boxes

engine = get_ocr_engine()
pages = load_document("samples/sample1.pdf")

for page_img in pages:
    results = extract_text_with_boxes(engine, page_img)
    for r in results:
        print(r["text"], r["confidence"])