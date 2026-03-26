# scripts/batch_test_layout.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path
from src.ingestion import load_document
from src.ocr      import extract_text_boxes
from src.layout   import run_layout_inference
# scripts/batch_test_layout.py
import json
from pathlib import Path
from src.ingestion import load_document
from src.ocr      import extract_text_boxes
from src.layout   import run_layout_inference

TEST_DOCS   = Path("tests/sample_docs")
RESULTS_OUT = Path("tests/layout_results")
RESULTS_OUT.mkdir(exist_ok=True)

for doc_path in TEST_DOCS.rglob("*.pdf"):
    image_tensors = load_document(doc_path)
    ocr_output    = extract_text_boxes(image_tensors)
    layout_result = run_layout_inference(ocr_output)

    out_file = RESULTS_OUT / f"{doc_path.stem}_layout.json"
    with open(out_file, "w") as f:
        json.dump(layout_result, f, indent=2)
    print(f"✅ Done: {doc_path.name}")