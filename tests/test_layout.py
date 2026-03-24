from layout.layout_detector import normalize_bboxes, LABEL_MAP

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