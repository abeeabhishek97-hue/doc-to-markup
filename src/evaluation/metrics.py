# src/evaluation/metrics.py

import re
from typing import List, Dict, Tuple
import nltk
from zss import simple_distance, Node


# ── Token Accuracy ────────────────────────────────────────────────────────────

def tokenize(text: str) -> List[str]:
    """Lowercase and tokenize text into words."""
    return nltk.word_tokenize(text.lower())


def token_accuracy(predicted: str, ground_truth: str) -> float:
    """
    Compute token-level accuracy between predicted and ground truth text.
    Returns a float between 0.0 and 1.0.
    """
    pred_tokens = tokenize(predicted)
    gt_tokens   = tokenize(ground_truth)

    if not gt_tokens:
        return 1.0 if not pred_tokens else 0.0

    # Count matching tokens at each position
    matches = sum(
        1 for p, g in zip(pred_tokens, gt_tokens) if p == g
    )
    return matches / max(len(pred_tokens), len(gt_tokens))


# ── Structure F1 ──────────────────────────────────────────────────────────────

def extract_structure_tags(markdown: str) -> List[str]:
    """
    Extract structural block types from Markdown in order.
    Returns a list like ['h1', 'paragraph', 'list', 'table', 'code']
    """
    tags = []
    for line in markdown.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#### "):
            tags.append("h4")
        elif stripped.startswith("### "):
            tags.append("h3")
        elif stripped.startswith("## "):
            tags.append("h2")
        elif stripped.startswith("# "):
            tags.append("h1")
        elif stripped.startswith("```"):
            tags.append("code")
        elif stripped.startswith("| "):
            tags.append("table")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            tags.append("list")
        else:
            tags.append("paragraph")
    return tags


def structure_f1(predicted: str, ground_truth: str) -> Dict[str, float]:
    """
    Compute per-tag precision, recall, F1 for structural elements.
    Returns dict with precision, recall, f1 keys.
    """
    pred_tags = extract_structure_tags(predicted)
    gt_tags   = extract_structure_tags(ground_truth)

    pred_counts = {}
    gt_counts   = {}
    match_counts = {}

    for tag in set(pred_tags + gt_tags):
        pred_counts[tag]  = pred_tags.count(tag)
        gt_counts[tag]    = gt_tags.count(tag)
        match_counts[tag] = min(pred_counts[tag], gt_counts[tag])

    total_pred    = sum(pred_counts.values())
    total_gt      = sum(gt_counts.values())
    total_matches = sum(match_counts.values())

    precision = total_matches / total_pred if total_pred > 0 else 0.0
    recall    = total_matches / total_gt   if total_gt   > 0 else 0.0
    f1        = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0 else 0.0
    )

    return {
        "precision": round(precision, 4),
        "recall":    round(recall,    4),
        "f1":        round(f1,        4),
    }


# ── Tree Edit Distance ────────────────────────────────────────────────────────

def markdown_to_tree(markdown: str) -> Node:
    """
    Convert Markdown to a tree structure for TED calculation.
    Root node is 'document', children are structural blocks.
    """
    root = Node("document")
    current_section = None

    for line in markdown.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("# "):
            node = Node("h1")
            node.addkid(Node(stripped[2:].strip()[:30]))
            root.addkid(node)
            current_section = node

        elif stripped.startswith("## "):
            node = Node("h2")
            node.addkid(Node(stripped[3:].strip()[:30]))
            root.addkid(node)
            current_section = node

        elif stripped.startswith("### "):
            node = Node("h3")
            node.addkid(Node(stripped[4:].strip()[:30]))
            root.addkid(node)

        elif stripped.startswith("#### "):
            node = Node("h4")
            node.addkid(Node(stripped[5:].strip()[:30]))
            root.addkid(node)

        elif stripped.startswith("```"):
            root.addkid(Node("code_block"))

        elif stripped.startswith("| "):
            root.addkid(Node("table_row"))

        elif stripped.startswith("- "):
            node = Node("list_item")
            node.addkid(Node(stripped[2:].strip()[:30]))
            root.addkid(node)

        else:
            node = Node("paragraph")
            node.addkid(Node(stripped[:30]))
            root.addkid(node)

    return root


def tree_edit_distance(predicted: str, ground_truth: str) -> float:
    """
    Compute normalized Tree Edit Distance between two Markdown strings.
    Returns 0.0 (identical) to 1.0 (completely different).
    """
    pred_tree = markdown_to_tree(predicted)
    gt_tree   = markdown_to_tree(ground_truth)

    distance = simple_distance(pred_tree, gt_tree)

    # Normalize by sum of node counts
    pred_size = count_nodes(pred_tree)
    gt_size   = count_nodes(gt_tree)
    max_size  = pred_size + gt_size

    return round(distance / max_size, 4) if max_size > 0 else 0.0


def count_nodes(node: Node) -> int:
    """Recursively count nodes in a tree."""
    return 1 + sum(count_nodes(child) for child in node.children)