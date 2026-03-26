# Edge Cases — Layout Detection

| Document | Page | Misclassified As | Should Be | Notes |
|---|---|---|---|---|
| example.pdf | 1 | paragraph | heading | Font size too small |
## Module Interface

### Input — OCR output format
Each item passed into `run_layout_inference()` should look like:
{
  "text": "Some text",
  "bbox": [x1, y1, x2, y2],
  "char_boxes": [[x1,y1,x2,y2], ...]
}

### Output — Layout result format
Each item returned looks like:
{
  "class": "heading" | "paragraph" | "list" | "table" | "code",
  "text": "Some text",
  "bbox": [x1, y1, x2, y2]
}