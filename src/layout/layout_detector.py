# src/layout/layout_detector.py

from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from PIL import Image
import torch
import re

LABEL_MAP = {
    0: "other",
    1: "heading",
    2: "paragraph",
    3: "list",
    4: "table",
    5: "code"
}


# ── Model loader (kept for compatibility) ────────────────────────────────────

def load_model(model_name: str = "microsoft/layoutlmv3-base"):
    processor = LayoutLMv3Processor.from_pretrained(model_name, apply_ocr=False)
    model = LayoutLMv3ForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(LABEL_MAP)
    )
    model.eval()
    return processor, model


# ── Bbox helpers ──────────────────────────────────────────────────────────────

def normalize_bboxes(bboxes: list, page_width: int, page_height: int) -> list:
    normalized = []
    for bbox in bboxes:
        # Handle both flat [x1,y1,x2,y2] and nested [[x1,y1],[x2,y2]] formats
        x1, y1, x2, y2 = flatten_bbox(bbox)
        normalized.append([
            int(1000 * x1 / page_width),
            int(1000 * y1 / page_height),
            int(1000 * x2 / page_width),
            int(1000 * y2 / page_height),
        ])
    return normalized


def flatten_bbox(bbox) -> tuple:
    """Convert any bbox format to (x1, y1, x2, y2)."""
    if isinstance(bbox[0], (list, tuple)):
        # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]] format from Tesseract/PaddleOCR
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        return min(xs), min(ys), max(xs), max(ys)
    else:
        # [x1, y1, x2, y2] flat format
        return bbox[0], bbox[1], bbox[2], bbox[3]


# ── Line grouping ─────────────────────────────────────────────────────────────

def group_words_into_lines(words: list, bboxes: list, y_threshold: int = 10) -> list:
    """
    Group individual OCR words into lines based on Y position.
    Words on the same horizontal band are merged into one line.

    Returns list of {text, bbox, words} dicts.
    """
    if not words:
        return []

    # Pair words with their flat bboxes
    items = []
    for word, bbox in zip(words, bboxes):
        x1, y1, x2, y2 = flatten_bbox(bbox)
        items.append({
            "text": word,
            "x1": x1, "y1": y1,
            "x2": x2, "y2": y2,
        })

    # Sort by Y then X
    items.sort(key=lambda w: (w["y1"], w["x1"]))

    lines = []
    current_line = [items[0]]

    for item in items[1:]:
        last = current_line[-1]
        # Same line if Y centers are close
        last_center = (last["y1"] + last["y2"]) / 2
        curr_center = (item["y1"] + item["y2"]) / 2

        if abs(curr_center - last_center) <= y_threshold:
            current_line.append(item)
        else:
            lines.append(current_line)
            current_line = [item]

    lines.append(current_line)

    # Merge each line into a single region
    result = []
    for line in lines:
        text = " ".join(w["text"] for w in line)
        x1 = min(w["x1"] for w in line)
        y1 = min(w["y1"] for w in line)
        x2 = max(w["x2"] for w in line)
        y2 = max(w["y2"] for w in line)
        result.append({
            "text": text,
            "bbox": [x1, y1, x2, y2],
        })

    return result


# ── Rule-based classifier ─────────────────────────────────────────────────────

def classify_line(line: dict, all_lines: list, line_idx: int) -> str:
    """
    Classify a single line using rules based on:
    - bbox height (font size proxy)
    - text content patterns
    - position relative to other lines
    """
    text   = line["text"].strip()
    bbox   = line["bbox"]
    height = bbox[3] - bbox[1]
    width  = bbox[2] - bbox[0]
    words  = text.split()
    n_words = len(words)

    if not text:
        return "other"

    # ── Code block rules ──────────────────────────────────────────────
    code_patterns = [
        r"^\s*(def |class |import |from |if |for |while |return )",
        r"[{}\[\]();]",
        r"^\s{4,}",          # deeply indented
        r"^>>>",             # Python REPL
        r"^\$\s",            # shell prompt
    ]
    if any(re.search(p, text) for p in code_patterns):
        return "code"

    # ── List item rules ───────────────────────────────────────────────
    list_patterns = [
        r"^[\•\-\*\·\–]\s",
        r"^\d+[\.\)]\s",
        r"^[a-zA-Z][\.\)]\s",
    ]
    if any(re.search(p, text) for p in list_patterns):
        return "list_item"

    # ── Table row rules ───────────────────────────────────────────────
    # Lines with multiple numbers/percentages separated by spaces
    if re.search(r"\d+\s+\d+", text) and n_words >= 3:
        num_count = len(re.findall(r"\d+\.?\d*%?", text))
        if num_count >= 2:
            return "table"

    # ── Heading rules ─────────────────────────────────────────────────
    # Tall text, short line, title case or all caps
    is_tall       = height > 20
    is_short      = n_words <= 12
    is_title_case = text.istitle() or text.isupper()
    is_bold_like  = (
        text.isupper() or
        (is_short and is_tall and not text.endswith("."))
    )

    if is_tall and is_short and is_bold_like:
        # Determine heading level by height
        if height > 40:
            return "heading_1"
        elif height > 30:
            return "heading_2"
        elif height > 20:
            return "heading_3"
        else:
            return "heading_4"

    if is_short and is_title_case and not text.endswith(".") and height > 18:
        return "heading_2"

    # ── Paragraph (default) ───────────────────────────────────────────
    return "paragraph"


def map_to_generator_label(classification: str) -> str:
    """Map classifier output to markdown_generator label."""
    mapping = {
        "heading_1": "heading",
        "heading_2": "heading",
        "heading_3": "heading",
        "heading_4": "heading",
        "list_item": "list_item",
        "table":     "table",
        "code":      "code",
        "paragraph": "paragraph",
        "other":     "paragraph",
    }
    return mapping.get(classification, "paragraph")


def get_heading_level(classification: str) -> int:
    levels = {
        "heading_1": 1,
        "heading_2": 2,
        "heading_3": 3,
        "heading_4": 4,
    }
    return levels.get(classification, 1)


# ── Main detection function ───────────────────────────────────────────────────

def run_layout_detection(image, words, bboxes, processor=None, model=None) -> list:
    """
    Rule-based layout detection.
    processor and model args kept for API compatibility but not used.

    Returns list of region dicts compatible with markdown_generator.
    """
    if not words:
        return []

    # Step 1 — Group words into lines
    lines = group_words_into_lines(words, bboxes)

    # Step 2 — Classify each line
    regions = []
    for i, line in enumerate(lines):
        classification = classify_line(line, lines, i)
        label          = map_to_generator_label(classification)

        region = {
            "text":       line["text"],
            "bbox":       line["bbox"],
            "label":      label,
            "confidence": 0.9,
        }

        # Add heading level if applicable
        if "heading" in classification:
            region["level"] = get_heading_level(classification)

        regions.append(region)

    return regions


# ── Kept for compatibility ────────────────────────────────────────────────────

def refine_classification(regions, ocr_boxes):
    return regions


def is_monospace(region):
    widths = [b[2] - b[0] for b in region.get("char_boxes", [])]
    if not widths:
        return False
    return (max(widths) - min(widths)) < 3


def has_grid_structure(ocr_boxes, bbox):
    contained = [b for b in ocr_boxes if is_inside(b, bbox)]
    x_positions = sorted(set(round(b[0] / 10) * 10 for b in contained))
    return len(x_positions) >= 2


def is_inside(box, bbox):
    return (box[0] >= bbox[0] and box[1] >= bbox[1] and
            box[2] <= bbox[2] and box[3] <= bbox[3])