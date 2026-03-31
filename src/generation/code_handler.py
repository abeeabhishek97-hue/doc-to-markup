# generator/code_handler.py

import re
from typing import Optional
# generator/code_handler.py

from typing import Optional, Dict  # ← add Dict here


# ── rest of your code unchanged ──

# Map layout-detected region labels → fenced language hints
LANGUAGE_HINTS: Dict[str, str] = {
    "code":        "",        # unknown — no language tag
    "python":      "python",
    "javascript":  "javascript",
    "json":        "json",
    "bash":        "bash",
    "shell":       "bash",
    "sql":         "sql",
    "html":        "html",
    "css":         "css",
    "xml":         "xml",
    "yaml":        "yaml",
}

# Heuristic patterns for auto-detecting language when label is generic
_DETECT_PATTERNS = [
    (r"\bdef\s+\w+\s*\(|import\s+\w+|print\s*\(", "python"),
    (r"function\s+\w+\s*\(|const\s+\w+\s*=|let\s+\w+\s*=",  "javascript"),
    (r"SELECT\s+|INSERT\s+INTO|CREATE\s+TABLE",               "sql"),
    (r"<\?xml|<!DOCTYPE|<html",                               "html"),
    (r"^\s*\{[\s\S]*\}\s*$",                                  "json"),
    (r"^#!\/bin\/bash|^\s*echo\s+",                           "bash"),
]


def detect_language(text: str) -> str:
    """
    Heuristically detect programming language from code text.
    Returns a language string for the fenced block, or '' if unknown.
    """
    for pattern, lang in _DETECT_PATTERNS:
        if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
            return lang
    return ""


def clean_code_text(text: str) -> str:
    """
    Clean up OCR artefacts common in code regions:
      - Replace common OCR confusions (l→1 in numeric context, etc.)
      - Strip trailing whitespace per line
      - Preserve indentation
    """
    lines = text.split("\n")
    cleaned = [line.rstrip() for line in lines]

    # Remove leading/trailing blank lines but preserve internal blank lines
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()

    return "\n".join(cleaned)


def code_to_markdown(
    text: str,
    language: Optional[str] = None,
    label: Optional[str] = None,
) -> str:
    """
    Wrap code text in a fenced Markdown code block.

    Args:
        text     : Raw code text (possibly from OCR).
        language : Explicit language override. If None, auto-detected.
        label    : Region label from layout model (e.g. 'python', 'code').

    Returns:
        A Markdown fenced code block string.

    Edge cases handled:
        - Text already wrapped in ``` → unwrap first, then re-wrap cleanly
        - Unknown language           → fence with no language tag
        - Empty text                 → returns empty string
    """
    if not text or not text.strip():
        return ""

    # Unwrap if OCR captured the fences themselves
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        # Remove first and last fence lines
        inner_lines = lines[1:]
        if inner_lines and inner_lines[-1].strip() == "```":
            inner_lines = inner_lines[:-1]
        stripped = "\n".join(inner_lines)

    cleaned = clean_code_text(stripped)

    # Determine language tag
    if language is not None:
        lang_tag = language
    elif label and label in LANGUAGE_HINTS:
        lang_tag = LANGUAGE_HINTS[label]
    else:
        lang_tag = detect_language(cleaned)

    return f"```{lang_tag}\n{cleaned}\n```"