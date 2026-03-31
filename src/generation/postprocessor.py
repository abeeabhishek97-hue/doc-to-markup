# src/generation/postprocessor.py

import re


def remove_stray_characters(text: str) -> str:
    """
    Remove common OCR noise:
    - Lone special characters on their own line
    - Repeated punctuation (e.g. ....., -----)
    - Zero-width spaces and non-breaking spaces
    """
    # Remove zero-width and non-breaking spaces
    text = text.replace("\u200b", "").replace("\u00a0", " ")

    # Remove lines that are only punctuation/symbols (OCR noise)
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Keep line if it has at least one alphanumeric character
        if stripped == "" or re.search(r"[a-zA-Z0-9]", stripped):
            cleaned.append(line)
    return "\n".join(cleaned)


def fix_broken_words(text: str) -> str:
    """
    Fix hyphenated line breaks introduced by OCR.
    e.g. 'docu-\nment' → 'document'
    """
    # Join words broken across lines with a hyphen
    text = re.sub(r"-\n(\s*)", "", text)
    return text


def normalize_whitespace(text: str) -> str:
    """
    - Collapse multiple spaces into one
    - Collapse 3+ newlines into 2
    - Strip trailing whitespace from each line
    """
    # Strip trailing whitespace per line
    lines = [line.rstrip() for line in text.split("\n")]
    text = "\n".join(lines)

    # Collapse multiple spaces (but not newlines)
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Collapse 3+ blank lines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def fix_heading_spacing(text: str) -> str:
    """
    Ensure every heading has a blank line before and after it.
    e.g.
        Some paragraph
        # Heading       ← missing blank line before
        Next paragraph
    becomes:
        Some paragraph

        # Heading

        Next paragraph
    """
    # Add blank line before headings if missing
    text = re.sub(r"([^\n])\n(#{1,4} )", r"\1\n\n\2", text)
    # Add blank line after headings if missing
    text = re.sub(r"(#{1,4} .+)\n([^\n#])", r"\1\n\n\2", text)
    return text


def fix_list_spacing(text: str) -> str:
    """
    Ensure list items are not separated by blank lines
    (which would make them loose lists in Markdown).
    Collapses blank lines between consecutive list items.
    """
    text = re.sub(r"(^- .+)\n\n(- )", r"\1\n\2", text, flags=re.MULTILINE)
    return text


def postprocess(markdown: str) -> str:
    """
    Run all post-processing steps in order on a Markdown string.

    Pipeline:
        1. Remove stray OCR characters
        2. Fix broken hyphenated words
        3. Normalize whitespace
        4. Fix heading spacing
        5. Fix list spacing

    Args:
        markdown: Raw Markdown string from the generator.

    Returns:
        Cleaned Markdown string.
    """
    if not markdown:
        return ""

    markdown = remove_stray_characters(markdown)
    markdown = fix_broken_words(markdown)
    markdown = normalize_whitespace(markdown)
    markdown = fix_heading_spacing(markdown)
    markdown = fix_list_spacing(markdown)

    return markdown.strip()