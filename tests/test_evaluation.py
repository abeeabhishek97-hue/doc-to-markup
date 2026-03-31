# tests/test_evaluation.py

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.evaluation.metrics import (
    token_accuracy,
    structure_f1,
    tree_edit_distance,
    extract_structure_tags,
)
from src.evaluation.evaluator import evaluate_single


def test_token_accuracy_perfect():
    assert token_accuracy("hello world", "hello world") == 1.0
    print("✅ test_token_accuracy_perfect passed")


def test_token_accuracy_partial():
    score = token_accuracy("hello world", "hello earth")
    assert 0.0 < score < 1.0
    print("✅ test_token_accuracy_partial passed")


def test_token_accuracy_empty():
    assert token_accuracy("", "") == 1.0
    print("✅ test_token_accuracy_empty passed")


def test_structure_tags_heading():
    tags = extract_structure_tags("# Title\n\nSome paragraph.")
    assert "h1" in tags
    assert "paragraph" in tags
    print("✅ test_structure_tags_heading passed")


def test_structure_f1_perfect():
    md = "# Title\n\nParagraph."
    result = structure_f1(md, md)
    assert result["f1"] == 1.0
    print("✅ test_structure_f1_perfect passed")


def test_structure_f1_different():
    pred = "# Title\n\nParagraph."
    gt   = "## Subtitle\n\n- item one\n- item two"
    result = structure_f1(pred, gt)
    assert result["f1"] < 1.0
    print("✅ test_structure_f1_different passed")


def test_tree_edit_distance_identical():
    md = "# Title\n\nParagraph.\n\n- item"
    assert tree_edit_distance(md, md) == 0.0
    print("✅ test_tree_edit_distance_identical passed")


def test_tree_edit_distance_different():
    pred = "# Title\n\nParagraph."
    gt   = "## Subtitle\n\n- item one\n- item two"
    assert tree_edit_distance(pred, gt) > 0.0
    print("✅ test_tree_edit_distance_different passed")


def test_evaluate_single():
    pred = "# Hello\n\nThis is a paragraph.\n\n- item one"
    gt   = "# Hello\n\nThis is a paragraph.\n\n- item one"
    result = evaluate_single(pred, gt)
    assert "token_accuracy"     in result
    assert "structure_f1"       in result
    assert "tree_edit_distance" in result
    assert result["token_accuracy"] == 1.0
    assert result["structure_f1"]["f1"] == 1.0
    assert result["tree_edit_distance"] == 0.0
    print("✅ test_evaluate_single passed")


if __name__ == "__main__":
    test_token_accuracy_perfect()
    test_token_accuracy_partial()
    test_token_accuracy_empty()
    test_structure_tags_heading()
    test_structure_f1_perfect()
    test_structure_f1_different()
    test_tree_edit_distance_identical()
    test_tree_edit_distance_different()
    test_evaluate_single()
    print("\n✅ All Day 13 evaluation tests passed")