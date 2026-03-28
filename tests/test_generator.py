import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.generation.markdown_generator import generate_markdown

def test_heading_levels():
    regions = [
        {"label": "heading", "text": "Main Title",   "bbox": [0, 0, 400, 40]},
        {"label": "heading", "text": "Subtitle",     "bbox": [0, 50, 400, 28]},
        {"label": "paragraph", "text": "Some body text here."},
    ]
    md = generate_markdown(regions)
    assert md.startswith("# Main Title")
    assert "## Subtitle" in md
    assert "Some body text here." in md
    print("✅ test_heading_levels passed")

def test_list_items():
    regions = [
        {"label": "heading",   "text": "My List", "bbox": [0, 0, 200, 30]},
        {"label": "list_item", "text": "• First item"},
        {"label": "list_item", "text": "Second item"},
        {"label": "list_item", "text": "- Third item"},
    ]
    md = generate_markdown(regions)
    assert "- First item" in md
    assert "- Second item" in md
    assert "- Third item" in md
    print("✅ test_list_items passed")

def test_empty_input():
    assert generate_markdown([]) == ""
    print("✅ test_empty_input passed")

def test_skips_empty_text():
    regions = [
        {"label": "paragraph", "text": "  "},
        {"label": "paragraph", "text": "Real content"},
    ]
    md = generate_markdown(regions)
    assert md == "Real content"
    print("✅ test_skips_empty_text passed")

if __name__ == "__main__":
    test_heading_levels()
    test_list_items()
    test_empty_input()
    test_skips_empty_text()
    print("\n✅ All Day 10 tests passed")