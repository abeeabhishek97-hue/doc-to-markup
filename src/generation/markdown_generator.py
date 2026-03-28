from typing import Optional


# ── Heading level helper ─────────────────────────────────────────────────────

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
    return text  # plain paragraph, blank lines added by the joiner


def _convert_list_item(region: dict) -> str:
    text = region.get("text", "").strip()
    # Strip any leading bullet characters the OCR may have captured
    for char in ["•", "-", "*", "·", "–"]:
        if text.startswith(char):
            text = text[len(char):].strip()
            break
    return f"- {text}"


# ── Main generator ────────────────────────────────────────────────────────────

def generate_markdown(regions: list[dict]) -> str:
    """
    Convert a list of layout regions to a Markdown string.
    Handles: headings (H1–H4), paragraphs, list items.
    Tables and code blocks added on Day 11.
    """
    if not regions:
        return ""

    lines = []
    prev_label: Optional[str] = None

    for region in regions:
        label = region.get("label", "paragraph").lower()
        text = region.get("text", "").strip()

        if not text:
            continue  # skip empty regions

        # ── Add spacing between different block types ──
        if prev_label and prev_label != label:
            lines.append("")  # blank line between blocks

        # ── Convert based on label ──
        if label == "heading":
            if prev_label == "heading":
                lines.append("")  # blank line between consecutive headings
            lines.append(_convert_heading(region, regions))

        elif label == "paragraph":
            lines.append(_convert_paragraph(region))

        elif label == "list_item":
            lines.append(_convert_list_item(region))

        elif label in ("table", "code"):
            # Placeholder — handled properly on Day 11
            lines.append(f"<!-- {label} block: Day 11 -->")
            lines.append(f"> {text}")

        else:
            # Unknown label — treat as paragraph
            lines.append(text)

        prev_label = label

    # Join and clean up extra blank lines
    markdown = "\n".join(lines)
    # Collapse 3+ consecutive newlines into 2
    import re
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    return markdown.strip()