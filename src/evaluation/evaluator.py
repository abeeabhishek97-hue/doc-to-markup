# src/evaluation/evaluator.py

import os
import json
import time
from typing import List, Dict, Any
from pathlib import Path

from src.evaluation.metrics import token_accuracy, structure_f1, tree_edit_distance


def evaluate_single(predicted: str, ground_truth: str) -> Dict[str, Any]:
    """
    Run all three metrics on a single predicted/ground_truth pair.

    Returns:
        dict with token_accuracy, structure_f1, tree_edit_distance
    """
    return {
        "token_accuracy":    token_accuracy(predicted, ground_truth),
        "structure_f1":      structure_f1(predicted, ground_truth),
        "tree_edit_distance": tree_edit_distance(predicted, ground_truth),
    }


def evaluate_batch(
    predicted_dir: str,
    ground_truth_dir: str,
) -> Dict[str, Any]:
    """
    Evaluate all .md files in predicted_dir against matching files
    in ground_truth_dir.

    Expected structure:
        predicted_dir/doc_001.md
        ground_truth_dir/doc_001.md

    Returns:
        Summary dict with per-file results and aggregate scores.
    """
    pred_path = Path(predicted_dir)
    gt_path   = Path(ground_truth_dir)

    pred_files = sorted(pred_path.glob("*.md"))

    if not pred_files:
        return {"error": f"No .md files found in {predicted_dir}"}

    results     = []
    total_ta    = 0.0
    total_f1    = 0.0
    total_ted   = 0.0
    found_count = 0

    for pred_file in pred_files:
        gt_file = gt_path / pred_file.name

        if not gt_file.exists():
            print(f"[SKIP] No ground truth for {pred_file.name}")
            continue

        predicted    = pred_file.read_text(encoding="utf-8")
        ground_truth = gt_file.read_text(encoding="utf-8")

        metrics = evaluate_single(predicted, ground_truth)
        metrics["file"] = pred_file.name

        results.append(metrics)
        found_count += 1

        total_ta  += metrics["token_accuracy"]
        total_f1  += metrics["structure_f1"]["f1"]
        total_ted += metrics["tree_edit_distance"]

        print(
            f"[{pred_file.name}] "
            f"TA={metrics['token_accuracy']:.3f} "
            f"F1={metrics['structure_f1']['f1']:.3f} "
            f"TED={metrics['tree_edit_distance']:.3f}"
        )

    if found_count == 0:
        return {"error": "No matching ground truth files found"}

    summary = {
        "total_files":          found_count,
        "avg_token_accuracy":   round(total_ta  / found_count, 4),
        "avg_structure_f1":     round(total_f1  / found_count, 4),
        "avg_tree_edit_distance": round(total_ted / found_count, 4),
        "per_file_results":     results,
    }

    return summary


def save_results(results: Dict[str, Any], output_path: str) -> None:
    """Save evaluation results to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to {output_path}")