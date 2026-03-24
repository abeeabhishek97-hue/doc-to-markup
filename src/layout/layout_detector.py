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