from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from PIL import Image
import torch

LABEL_MAP = {
    0: "other",
    1: "heading",
    2: "paragraph",
    3: "list",
    4: "table",
    5: "code"
}

def load_model(model_name: str = "microsoft/layoutlmv3-base"):
    processor = LayoutLMv3Processor.from_pretrained(model_name, apply_ocr=False)
    model = LayoutLMv3ForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(LABEL_MAP)
    )
    model.eval()
    return processor, model


def normalize_bboxes(bboxes: list, page_width: int, page_height: int) -> list:
    normalized = []
    for x1, y1, x2, y2 in bboxes:
        normalized.append([
            int(1000 * x1 / page_width),
            int(1000 * y1 / page_height),
            int(1000 * x2 / page_width),
            int(1000 * y2 / page_height),
        ])
    return normalized


def run_layout_detection(image, words, bboxes, processor, model):
    w, h = image.size
    norm_bboxes = normalize_bboxes(bboxes, w, h)

    encoding = processor(
        image,
        words,
        boxes=norm_bboxes,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**encoding)

    logits = outputs.logits
    predictions = logits.argmax(-1).squeeze().tolist()

    word_ids = encoding.word_ids()
    results = []
    seen_word_ids = set()

    for token_idx, word_id in enumerate(word_ids):
        if word_id is None or word_id in seen_word_ids:
            continue
        seen_word_ids.add(word_id)
        label_id = predictions[token_idx]
        results.append({
            "text": words[word_id],
            "bbox": bboxes[word_id],
            "label": LABEL_MAP.get(label_id, "other")
        })

    return results
def refine_classification(regions, ocr_boxes):
    for region in regions:
        text   = region.get("text", "")
        bbox   = region["bbox"]
        height = bbox[3] - bbox[1]

        # Rule 1: Short tall lines are likely headings
        if region["class"] == "paragraph":
            if height > 40 and len(text.split()) < 10:
                region["class"] = "heading"

        # Rule 2: Monospace font regions are code
        if region["class"] == "paragraph":
            if is_monospace(region):
                region["class"] = "code"

        # Rule 3: Single-column tables misread as lists
        if region["class"] == "list":
            if has_grid_structure(ocr_boxes, bbox):
                region["class"] = "table"

    return regions


def is_monospace(region):
    widths = [b[2] - b[0] for b in region.get("char_boxes", [])]
    if not widths:
        return False
    return (max(widths) - min(widths)) < 3


def has_grid_structure(ocr_boxes, bbox):
    contained = [b for b in ocr_boxes if is_inside(b, bbox)]
    x_positions = sorted(
        set(round(b[0] / 10) * 10 for b in contained)
    )
    return len(x_positions) >= 2