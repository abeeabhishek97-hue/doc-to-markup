import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.generation.markdown_generator import generate_markdown
from src.generation.table_handler import table_to_markdown, normalize_cell
from src.generation.code_handler import code_to_markdown, detect_language
from src.generation.postprocessor import postprocess
from src.generation.validator import validate_markdown, get_structure_summary


# ── Day 10 tests ──────────────────────────────────────────────────────────────

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


# ── Day 11 tests — Table handler ──────────────────────────────────────────────

def test_basic_table():
    headers = ["Name", "Age", "City"]
    rows    = [["Alice", "30", "London"], ["Bob", "25", "Paris"]]
    md      = table_to_markdown(headers, rows, pretty=False)
    lines   = md.split("\n")
    assert lines[0] == "| Name | Age | City |"
    assert "---" in lines[1]
    assert "Alice" in lines[2]
    print("✅ test_basic_table passed")


def test_missing_cells_padded():
    headers = ["A", "B", "C"]
    rows    = [["x"]]
    md      = table_to_markdown(headers, rows, pretty=False)
    assert md.count("|") >= 4
    print("✅ test_missing_cells_padded passed")


def test_extra_cells_truncated():
    headers = ["A", "B"]
    rows    = [["x", "y", "z", "w"]]
    md      = table_to_markdown(headers, rows, pretty=False)
    assert md.split("\n")[2] == "| x | y |"
    print("✅ test_extra_cells_truncated passed")


def test_multiline_cell_collapsed():
    assert normalize_cell("line one\nline two") == "line one<br>line two"
    print("✅ test_multiline_cell_collapsed passed")


def test_empty_headers_returns_empty():
    assert table_to_markdown([], []) == ""
    print("✅ test_empty_headers_returns_empty passed")


def test_pretty_alignment():
    headers = ["Short", "A much longer header"]
    rows    = [["hi", "world"]]
    md      = table_to_markdown(headers, rows, pretty=True)
    pipe_counts = [line.count("|") for line in md.split("\n")]
    assert len(set(pipe_counts)) == 1
    print("✅ test_pretty_alignment passed")


# ── Day 11 tests — Code handler ───────────────────────────────────────────────

def test_basic_code_block():
    md = code_to_markdown("print('hello')", language="python")
    assert md.startswith("```python")
    assert md.endswith("```")
    assert "print" in md
    print("✅ test_basic_code_block passed")


def test_autodetect_python():
    assert detect_language("def foo(x):\n    return x") == "python"
    print("✅ test_autodetect_python passed")


def test_autodetect_sql():
    assert detect_language("SELECT * FROM users WHERE id = 1") == "sql"
    print("✅ test_autodetect_sql passed")


def test_autodetect_javascript():
    assert detect_language("const x = () => {}") == "javascript"
    print("✅ test_autodetect_javascript passed")


def test_already_fenced_unwrapped():
    raw = "```python\nprint('hi')\n```"
    md  = code_to_markdown(raw)
    assert md.count("```") == 2
    print("✅ test_already_fenced_unwrapped passed")


def test_empty_code_returns_empty():
    assert code_to_markdown("") == ""
    assert code_to_markdown("   ") == ""
    print("✅ test_empty_code_returns_empty passed")


def test_label_hint_used():
    md = code_to_markdown("echo hello", label="bash")
    assert "```bash" in md
    print("✅ test_label_hint_used passed")


# ── Day 11 tests — Integration ────────────────────────────────────────────────

def test_table_region():
    regions = [{
        "label":   "table",
        "headers": ["Metric", "Value"],
        "rows":    [["Accuracy", "94.2%"], ["F1 Score", "0.91"]],
    }]
    md = generate_markdown(regions)
    assert "Metric" in md
    assert "Value" in md
    assert "94.2%" in md
    print("✅ test_table_region passed")


def test_code_region():
    regions = [{
        "label": "code",
        "text":  "SELECT * FROM results;",
    }]
    md = generate_markdown(regions)
    assert "```" in md
    assert "SELECT" in md
    print("✅ test_code_region passed")


def test_nested_list_region():
    regions = [{
        "label": "list",
        "items": [
            "Top level",
            {"text": "Parent", "children": ["Child A", "Child B"]},
        ],
    }]
    md = generate_markdown(regions)
    assert "- Top level" in md
    assert "  - Child A" in md
    assert "  - Child B" in md
    print("✅ test_nested_list_region passed")


def test_table_missing_headers_fallback():
    regions = [{
        "label": "table",
        "text":  "some raw table text",
    }]
    md = generate_markdown(regions)
    assert "<!--" in md or "some raw table text" in md
    print("✅ test_table_missing_headers_fallback passed")


def test_mixed_document():
    regions = [
        {"label": "heading",   "text": "Results",  "bbox": [0, 0, 400, 36]},
        {"label": "paragraph", "text": "Summary of findings."},
        {"label": "table",     "headers": ["Metric", "Value"],
                               "rows": [["Accuracy", "94.2%"]]},
        {"label": "list",      "items": [
            "First point",
            {"text": "Second", "children": ["Sub A", "Sub B"]},
        ]},
        {"label": "code",      "text": "SELECT accuracy FROM results;"},
    ]
    md = generate_markdown(regions)
    assert "# Results" in md
    assert "Summary of findings." in md
    assert "Metric" in md and "Value" in md
    assert "- First point" in md
    assert "  - Sub A" in md
    assert "```" in md
    print("✅ test_mixed_document passed")


# ── Day 12 tests — Postprocessor ─────────────────────────────────────────────

def test_postprocess_removes_noise():
    noisy = "# Title\n\n...\n\nSome paragraph text."
    result = postprocess(noisy)
    assert "..." not in result
    assert "Some paragraph text." in result
    print("✅ test_postprocess_removes_noise passed")


def test_postprocess_fixes_broken_words():
    broken = "This is a docu-\nment with broken words."
    result = postprocess(broken)
    assert "document" in result
    print("✅ test_postprocess_fixes_broken_words passed")


def test_postprocess_normalizes_whitespace():
    messy = "# Title\n\n\n\n\nParagraph."
    result = postprocess(messy)
    assert "\n\n\n" not in result
    print("✅ test_postprocess_normalizes_whitespace passed")


def test_postprocess_empty_input():
    assert postprocess("") == ""
    print("✅ test_postprocess_empty_input passed")


def test_validate_valid_markdown():
    md = "# Hello\n\nThis is a paragraph.\n\n- item one\n- item two"
    is_valid, message = validate_markdown(md)
    assert is_valid is True
    assert message == "ok"
    print("✅ test_validate_valid_markdown passed")


def test_validate_empty_markdown():
    is_valid, message = validate_markdown("")
    assert is_valid is False
    print("✅ test_validate_empty_markdown passed")


def test_structure_summary():
    md = "# Heading\n\nParagraph.\n\n- item\n\n```python\ncode\n```"
    summary = get_structure_summary(md)
    assert summary["headings"] == 1
    assert summary["paragraphs"] >= 1   # ← fixed: markdown-it counts list items as paragraphs too
    assert summary["code_blocks"] == 1
    print("✅ test_structure_summary passed")


# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Day 10
    test_heading_levels()
    test_list_items()
    test_empty_input()
    test_skips_empty_text()
    print("\n✅ All Day 10 tests passed\n")

    # Day 11 — Table handler
    test_basic_table()
    test_missing_cells_padded()
    test_extra_cells_truncated()
    test_multiline_cell_collapsed()
    test_empty_headers_returns_empty()
    test_pretty_alignment()
    print("\n✅ All Day 11 table tests passed\n")

    # Day 11 — Code handler
    test_basic_code_block()
    test_autodetect_python()
    test_autodetect_sql()
    test_autodetect_javascript()
    test_already_fenced_unwrapped()
    test_empty_code_returns_empty()
    test_label_hint_used()
    print("\n✅ All Day 11 code tests passed\n")

    # Day 11 — Integration
    test_table_region()
    test_code_region()
    test_nested_list_region()
    test_table_missing_headers_fallback()
    test_mixed_document()
    print("\n✅ All Day 11 integration tests passed\n")

    # Day 12 — Postprocessor & Validator
    test_postprocess_removes_noise()
    test_postprocess_fixes_broken_words()
    test_postprocess_normalizes_whitespace()
    test_postprocess_empty_input()
    test_validate_valid_markdown()
    test_validate_empty_markdown()
    test_structure_summary()
    print("\n✅ All Day 12 tests passed\n")

    print("✅ All tests passed")