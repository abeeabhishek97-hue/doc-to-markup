# scripts/run_evaluation.py

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import argparse
import requests
from pathlib import Path
from src.evaluation.evaluator import evaluate_single, save_results
from src.ingestion.document_loader import load_document
from src.ocr.ocr_engine import extract_text_boxes
from src.layout.layout_detector import run_layout_detection, load_model
from src.generation.markdown_generator import generate_markdown
from src.generation.postprocessor import postprocess


API_URL = "http://localhost:8000/convert"


def convert_via_api(pdf_path: str) -> str:
    """Convert a PDF to Markdown via the running API."""
    with open(pdf_path, "rb") as f:
        response = requests.post(
            API_URL,
            files={"file": (os.path.basename(pdf_path), f, "application/pdf")},
            timeout=120
        )
    response.raise_for_status()
    return response.json()["markdown"]


def run_eval_on_folder(
    input_dir: str,
    ground_truth_dir: str,
    output_path: str = "evaluation_results.json"
):
    """
    Convert all PDFs in input_dir via API and evaluate
    against ground truth Markdown files in ground_truth_dir.
    """
    input_path = Path(input_dir)
    gt_path    = Path(ground_truth_dir)
    pdf_files  = sorted(input_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files to evaluate\n")

    results     = []
    total_ta    = 0.0
    total_f1    = 0.0
    total_ted   = 0.0
    found_count = 0

    for pdf_file in pdf_files:
        gt_file = gt_path / (pdf_file.stem + ".md")

        if not gt_file.exists():
            print(f"[SKIP] No ground truth for {pdf_file.name}")
            continue

        print(f"[Processing] {pdf_file.name}...")

        try:
            predicted    = convert_via_api(str(pdf_file))
            ground_truth = gt_file.read_text(encoding="utf-8")

            from src.evaluation.evaluator import evaluate_single
            metrics = evaluate_single(predicted, ground_truth)
            metrics["file"] = pdf_file.name

            results.append(metrics)
            found_count += 1

            total_ta  += metrics["token_accuracy"]
            total_f1  += metrics["structure_f1"]["f1"]
            total_ted += metrics["tree_edit_distance"]

            print(
                f"  TA={metrics['token_accuracy']:.3f}  "
                f"F1={metrics['structure_f1']['f1']:.3f}  "
                f"TED={metrics['tree_edit_distance']:.3f}"
            )

        except Exception as e:
            print(f"  [ERROR] {e}")
            continue

    if found_count == 0:
        print("No files were evaluated.")
        return

    summary = {
        "total_files":            found_count,
        "avg_token_accuracy":     round(total_ta  / found_count, 4),
        "avg_structure_f1":       round(total_f1  / found_count, 4),
        "avg_tree_edit_distance": round(total_ted / found_count, 4),
        "per_file_results":       results,
    }

    print(f"\n{'='*50}")
    print(f"EVALUATION SUMMARY — {found_count} files")
    print(f"{'='*50}")
    print(f"Avg Token Accuracy    : {summary['avg_token_accuracy']:.4f}")
    print(f"Avg Structure F1      : {summary['avg_structure_f1']:.4f}")
    print(f"Avg Tree Edit Distance: {summary['avg_tree_edit_distance']:.4f}")
    print(f"{'='*50}")

    save_results(summary, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run evaluation on documents")
    parser.add_argument("--input",  required=True, help="Folder with PDF files")
    parser.add_argument("--gt",     required=True, help="Folder with ground truth .md files")
    parser.add_argument("--output", default="evaluation_results.json")
    args = parser.parse_args()

    run_eval_on_folder(args.input, args.gt, args.output)