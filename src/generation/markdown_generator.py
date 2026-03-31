# generator/markdown_generator.py

from typing import Optional
import re

from .table_handler import table_to_markdown
from .code_handler import code_to_markdown


# ── Heading level helper ──────────────────────────────────────────────────────

def _infer_heading_level(region: dict, all_regions: list[dict]) -> int:
    """
    Estimate H1–H4 from font size if available, else fall back to position.
    LayoutLMv3 doesn't give font size directly, so we use bbox height as proxy.
    """
    bbox = region.get("bbox", [0, 0, 0, 20])
    height = bbox[3] - bbox[1]  # y2 - y1

    # Collect all heading heights to rank them
    heading_heights = sorted(
        set(
            r["bbox"][3] - r["bbox"][1]
            for r in all_regions
            if r.get("label") == "heading" and "bbox" in r
        ),
        reverse=True  # tallest = H1
    )

    if not heading_heights:
        return 1

    try:
        rank = heading_heights.index(height)
    except ValueError:
        rank = len(heading_heights) - 1

    # Map rank → H1, H2, H3, H4 (cap at 4)
    return min(rank + 1, 4)


# ── Per-region converters ─────────────────────────────────────────────────────

def _convert_heading(region: dict, all_regions: list[dict]) -> str:
    level = _infer_heading_level(region, all_regions)
    text = region.get("text", "").strip()
    return f"{'#' * level} {text}"


def _convert_paragraph(region: dict) -> str:
    text = region.get("text", "").strip()
    return text


def _convert_list_item(region: dict) -> str:
    text = region.get("text", "").strip()
    # Strip any leading bullet characters the OCR may have captured
    for char in ["•", "-", "*", "·", "–"]:
        if text.startswith(char):
            text = text[len(char):].strip()
            break
    return f"- {text}"


def _convert_nested_list(region: dict) -> str:
    """
    Handle nested list regions.
    Expects region to have an 'items' key:
        items: list of str | dict{"text": str, "children": list}
    Falls back to plain list_item conversion if 'items' is absent.
    """
    items = region.get("items")
    if not items:
        return _convert_list_item(region)
    return _render_nested(items, indent=0)


def _render_nested(items: list, indent: int) -> str:
    """Recursively render nested list items with indentation."""
    lines = []
    prefix = "  " * indent + "-"
    for item in items:
        if isinstance(item, str):
            lines.append(f"{prefix} {item.strip()}")
        elif isinstance(item, dict):
            text = item.get("text", "").strip()
            lines.append(f"{prefix} {text}")
            children = item.get("children", [])
            if children:
                lines.append(_render_nested(children, indent + 1))
    return "\n".join(lines)


def _convert_table(region: dict) -> str:
    """
    Convert a table region to a Markdown table.
    Expects region keys:
        headers : list[str]       — column headers
        rows    : list[list[str]] — cell data rows
    Falls back to a warning comment if structure is missing.
    """
    headers = region.get("headers")
    rows = region.get("rows")

    if not headers or rows is None:
        # Graceful fallback — raw text indented as blockquote
        raw = region.get("text", "").strip()
        return f"<!-- table: missing headers/rows -->\n> {raw}" if raw else "<!-- table: empty -->"

    return table_to_markdown(headers, rows, pretty=True)


def _convert_code(region: dict) -> str:
    """
    Convert a code region to a fenced Markdown code block.
    Expects region keys:
        text     : str          — raw code text
        language : str (opt)    — explicit language override
        label    : str (opt)    — layout model label for language hint
    """
    text = region.get("text", "").strip()
    if not text:
        return "<!-- code: empty -->"

    return code_to_markdown(
        text=text,
        language=region.get("language"),   # explicit override if present
        label=region.get("label"),         # layout label as hint
    )


# ── Main generator ────────────────────────────────────────────────────────────

def generate_markdown(regions: list[dict]) -> str:
    """
    Convert a list of layout regions to a Markdown string.

    Supported region labels:
        heading    → H1–H4 inferred from bbox height
        paragraph  → plain text block
        list_item  → flat unordered list item (- text)
        list       → nested list (uses 'items' key)
        table      → Markdown table (uses 'headers' + 'rows' keys)
        code       → fenced code block with language auto-detection

    All other labels fall back to plain paragraph text.
    """
    if not regions:
        return ""

    lines: list[str] = []
    prev_label: Optional[str] = None

    for region in regions:
        label = region.get("label", "paragraph").lower()
        text  = region.get("text", "").strip()

        # Tables and code blocks may have no 'text' key — still process them
        has_content = bool(text) or label in ("table", "code", "list")
        if not has_content:
            continue

        # ── Blank line between different block types ──────────────────
        if prev_label is not None and prev_label != label:
            lines.append("")

        # ── Blank line between consecutive headings ───────────────────
        if label == "heading" and prev_label == "heading":
            lines.append("")

        # ── Dispatch to converter ─────────────────────────────────────
        if label == "heading":
            lines.append(_convert_heading(region, regions))

        elif label == "paragraph":
            lines.append(_convert_paragraph(region))

        elif label == "list_item":
            lines.append(_convert_list_item(region))

        elif label == "list":
            lines.append(_convert_nested_list(region))

        elif label == "table":
            lines.append(_convert_table(region))

        elif label == "code":
            lines.append(_convert_code(region))

        else:
            # Unknown label — treat as paragraph
            lines.append(text)

        prev_label = label

    # ── Join and clean up extra blank lines ───────────────────────────
    markdown = "\n".join(lines)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    return markdown.strip()