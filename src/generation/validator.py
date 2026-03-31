# src/generation/validator.py

from markdown_it import MarkdownIt
from typing import Tuple


# Single shared parser instance
_md = MarkdownIt()


def validate_markdown(text: str) -> Tuple[bool, str]:
    """
    Validate that a Markdown string parses without errors.

    Uses markdown-it-py to render the Markdown to HTML.
    If rendering succeeds, the Markdown is considered valid.

    Args:
        text: Markdown string to validate.

    Returns:
        (is_valid, message) tuple.
        is_valid : True if Markdown parsed successfully.
        message  : 'ok' if valid, or a description of the issue.
    """
    if not text or not text.strip():
        return False, "Empty Markdown output"

    try:
        html = _md.render(text)

        # Basic sanity checks on the rendered HTML
        if not html or not html.strip():
            return False, "Markdown rendered to empty HTML"

        return True, "ok"

    except Exception as e:
        return False, f"Markdown parse error: {str(e)}"


def get_structure_summary(text: str) -> dict:
    """
    Parse Markdown tokens and return a summary of the document structure.
    Useful for debugging and evaluation on Day 13.

    Returns a dict with counts of each block type found.
    """
    if not text:
        return {}

    tokens = _md.parse(text)
    summary = {
        "headings":   0,
        "paragraphs": 0,
        "lists":      0,
        "tables":     0,
        "code_blocks": 0,
    }

    for token in tokens:
        if token.type == "heading_open":
            summary["headings"] += 1
        elif token.type == "paragraph_open":
            summary["paragraphs"] += 1
        elif token.type == "bullet_list_open":
            summary["lists"] += 1
        elif token.type == "table_open":
            summary["tables"] += 1
        elif token.type == "fence":
            summary["code_blocks"] += 1

    return summary