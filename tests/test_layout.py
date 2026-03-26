from layout.layout_detector import normalize_bboxes, LABEL_MAP
from src.layout.layout_detector import (
    refine_classification,
    is_monospace,
    has_grid_structure,
)

def test_normalize_bboxes_basic():
    bboxes = [[100, 200, 300, 400]]
    result = normalize_bboxes(bboxes, page_width=1000, page_height=1000)
    assert result == [[100, 200, 300, 400]]

def test_normalize_bboxes_scales_correctly():
    bboxes = [[500, 500, 1000, 1000]]
    result = normalize_bboxes(bboxes, page_width=2000, page_height=2000)
    assert result == [[250, 250, 500, 500]]

def test_label_map_has_all_classes():
    expected = {"heading", "paragraph", "list", "table", "code", "other"}
    assert set(LABEL_MAP.values()) == expected

# ── NEW Day 6 tests ──────────────────────────────────────────────────────────

def test_short_tall_region_becomes_heading():
    regions = [{"class": "paragraph", "text": "Introduction",
                "bbox": [0, 0, 300, 50], "char_boxes": []}]
    result = refine_classification(regions, [])
    assert result[0]["class"] == "heading"

def test_long_paragraph_stays_paragraph():
    regions = [{"class": "paragraph",
                "text": "This is a long paragraph with many words that should not be a heading.",
                "bbox": [0, 0, 300, 50], "char_boxes": []}]
    result = refine_classification(regions, [])
    assert result[0]["class"] == "paragraph"

def test_monospace_region_becomes_code():
    regions = [{"class": "paragraph", "text": "print('hello')",
                "bbox": [0, 0, 200, 30],
                "char_boxes": [[0,0,10,20],[10,0,20,20],[20,0,30,20]]}]
    result = refine_classification(regions, [])
    assert result[0]["class"] == "code"

def test_list_with_grid_becomes_table():
    ocr_boxes = [[10,10,80,30],[110,10,180,30],[10,40,80,60],[110,40,180,60]]
    regions = [{"class": "list", "text": "item",
                "bbox": [0, 0, 200, 80], "char_boxes": []}]
    result = refine_classification(regions, ocr_boxes)
    assert result[0]["class"] == "table"

def test_empty_regions_returns_empty():
    assert refine_classification([], []) == []

def test_is_monospace_true():
    region = {"char_boxes": [[0,0,10,20],[10,0,20,20],[20,0,30,20]]}
    assert is_monospace(region) == True

def test_is_monospace_false():
    region = {"char_boxes": [[0,0,5,20],[5,0,20,20],[20,0,40,20]]}
    assert is_monospace(region) == False

def test_is_monospace_no_char_boxes():
    assert is_monospace({"char_boxes": []}) == False

def test_has_grid_structure_true():
    ocr_boxes = [[10,10,80,30],[110,10,180,30]]
    assert has_grid_structure(ocr_boxes, [0,0,200,80]) == True

def test_has_grid_structure_single_column():
    ocr_boxes = [[10,10,80,30],[12,40,80,60]]
    assert has_grid_structure(ocr_boxes, [0,0,200,80]) == False

def test_has_grid_structure_empty():
    assert has_grid_structure([], [0,0,200,80]) == False
def is_inside(box, bbox):
    """Check if a box lies within a bounding region."""
    return (box[0] >= bbox[0] and box[1] >= bbox[1] and
            box[2] <= bbox[2] and box[3] <= bbox[3])