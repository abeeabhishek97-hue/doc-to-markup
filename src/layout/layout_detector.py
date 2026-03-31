# src/layout/layout_detector.py

from PIL import Image
import re

LABEL_MAP = {
    0: "other",
    1: "heading",
    2: "paragraph",
    3: "list",
    4: "table",
    5: "code"
}


# ── Model loader (kept for API compatibility) ─────────────────────────────────

def load_model(model_name: str = "microsoft/layoutlmv3-base"):
    """Kept for API compatibility — rule-based classifier used instead."""
    from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
    processor = LayoutLMv3Processor.from_pretrained(model_name, apply_ocr=False)
    model = LayoutLMv3ForTokenClassification.from_pretrained(
        model_name, num_labels=len(LABEL_MAP)
    )
    model.eval()
    return processor, model


# ── Bbox helpers ──────────────────────────────────────────────────────────────

def flatten_bbox(bbox) -> tuple:
    """Convert any bbox format to (x1, y1, x2, y2)."""
    if isinstance(bbox[0], (list, tuple)):
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        return min(xs), min(ys), max(xs), max(ys)
    return bbox[0], bbox[1], bbox[2], bbox[3]


# ── Line grouping using Tesseract block/line metadata ─────────────────────────

def group_words_into_lines(words: list, bboxes: list,
                           ocr_results: list = None,
                           y_threshold: int = 8) -> list:
    """
    Group words into lines.
    If ocr_results has block_num/line_num, use those for perfect grouping.
    Otherwise fall back to Y-position grouping.
    """
    if not words:
        return []

    # ── Method 1: Use Tesseract block/line numbers (most accurate) ────
    if ocr_results and "block_num" in ocr_results[0]:
        return group_by_tesseract_lines(words, bboxes, ocr_results)

    # ── Method 2: Y-position grouping (fallback) ──────────────────────
    return group_by_y_position(words, bboxes, y_threshold)


def group_by_tesseract_lines(words, bboxes, ocr_results) -> list:
    """Group words using Tesseract's block_num + par_num + line_num."""
    from collections import defaultdict

    lines = defaultdict(list)
    for word, bbox, ocr in zip(words, bboxes, ocr_results):
        key = (
            ocr.get("block_num", 0),
            ocr.get("par_num",   0),
            ocr.get("line_num",  0),
        )
        x1, y1, x2, y2 = flatten_bbox(bbox)
        lines[key].append({
            "text": word,
            "x1": x1, "y1": y1,
            "x2": x2, "y2": y2,
        })

    result = []
    for key in sorted(lines.keys()):
        line_words = sorted(lines[key], key=lambda w: w["x1"])
        text = " ".join(w["text"] for w in line_words)
        x1 = min(w["x1"] for w in line_words)
        y1 = min(w["y1"] for w in line_words)
        x2 = max(w["x2"] for w in line_words)
        y2 = max(w["y2"] for w in line_words)
        result.append({"text": text, "bbox": [x1, y1, x2, y2]})

    return result


def group_by_y_position(words, bboxes, y_threshold=8) -> list:
    """Fallback: group words by Y position."""
    items = []
    for word, bbox in zip(words, bboxes):
        x1, y1, x2, y2 = flatten_bbox(bbox)
        items.append({"text": word, "x1": x1, "y1": y1, "x2": x2, "y2": y2})

    items.sort(key=lambda w: (w["y1"], w["x1"]))

    lines = []
    current = [items[0]]
    for item in items[1:]:
        last_center = (current[-1]["y1"] + current[-1]["y2"]) / 2
        curr_center = (item["y1"] + item["y2"]) / 2
        if abs(curr_center - last_center) <= y_threshold:
            current.append(item)
        else:
            lines.append(current)
            current = [item]
    lines.append(current)

    result = []
    for line in lines:
        line = sorted(line, key=lambda w: w["x1"])
        text = " ".join(w["text"] for w in line)
        x1 = min(w["x1"] for w in line)
        y1 = min(w["y1"] for w in line)
        x2 = max(w["x2"] for w in line)
        y2 = max(w["y2"] for w in line)
        result.append({"text": text, "bbox": [x1, y1, x2, y2]})

    return result


# ── Rule-based classifier ─────────────────────────────────────────────────────

def classify_line(line: dict, all_lines: list, line_idx: int) -> str:
    text    = line["text"].strip()
    bbox    = line["bbox"]
    height  = bbox[3] - bbox[1]
    words   = text.split()
    n_words = len(words)

    if not text:
        return "other"

    # ── Code detection ────────────────────────────────────────────────
    code_patterns = [
        r"^(import |from |def |class |return |if |for |while |with |try:|except)",
        r"^\s*(#|//)",                     # comments
        r"[{};]$",                         # ends with brace/semicolon
        r"=\s*Path\(|\.mkdir\(|\.rglob\(", # pathlib patterns
        r"^\s{2,}[a-z_]+\s*[=\(]",        # indented assignments
        r"json\.|cv2\.|plt\.",             # library calls
        r"f['\"].*{.*}.*['\"]",            # f-strings
        r"^git (add|commit|push|clone)",   # git commands
        r"^python\s+\w+",                  # python commands
        r"^\$\s",                          # shell prompt
        r"^>>>",                           # Python REPL
    ]
    if any(re.search(p, text) for p in code_patterns):
        return "code"

    # ── List item detection ───────────────────────────────────────────
    list_patterns = [
        r"^[\•\-\*\·\–]\s",
        r"^\d+[\.\)]\s",
        r"^[a-zA-Z][\.\)]\s",
    ]
    if any(re.search(p, text) for p in list_patterns):
        return "list_item"

    # ── Table row detection ───────────────────────────────────────────
    num_count = len(re.findall(r"\d+\.?\d*%?", text))
    if num_count >= 2 and n_words >= 2:
        return "table"

    # ── Heading detection ─────────────────────────────────────────────
    is_short     = n_words <= 12
    is_tall      = height > 18
    no_period    = not text.endswith(".")
    is_titlecase = text.istitle() or text.isupper()

    if is_short and is_tall and no_period and is_titlecase:
        if height > 40:   return "heading_1"
        elif height > 30: return "heading_2"
        elif height > 22: return "heading_3"
        else:             return "heading_4"

    if is_short and no_period and height > 20:
        return "heading_2"

    return "paragraph"


def map_to_generator_label(classification: str) -> str:
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
    return {"heading_1": 1, "heading_2": 2,
            "heading_3": 3, "heading_4": 4}.get(classification, 1)


# ── Main detection function ───────────────────────────────────────────────────

def run_layout_detection(image, words, bboxes,
                         processor=None, model=None,
                         ocr_results=None) -> list:
    """
    Rule-based layout detection using Tesseract line metadata.
    processor and model kept for API compatibility.
    """
    if not words:
        return []

    # Group words into lines using Tesseract metadata if available
    lines = group_words_into_lines(words, bboxes, ocr_results)

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

        if "heading" in classification:
            region["level"] = get_heading_level(classification)

        regions.append(region)

    return regions


# ── Compatibility stubs ───────────────────────────────────────────────────────

def normalize_bboxes(bboxes, page_width, page_height):
    return bboxes

def refine_classification(regions, ocr_boxes):
    return regions

def is_monospace(region):
    return False

def has_grid_structure(ocr_boxes, bbox):
    return False

def is_inside(box, bbox):
    return (box[0] >= bbox[0] and box[1] >= bbox[1] and
            box[2] <= bbox[2] and box[3] <= bbox[3])