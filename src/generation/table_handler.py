# src/generation/table_handler.py

from typing import List, Dict


def normalize_cell(cell: str) -> str:
    """
    Flatten multi-line cell content into a single line.
    Replaces newlines with <br> (GitHub-flavoured Markdown).
    Strips leading/trailing whitespace.
    """
    return cell.strip().replace("\n", "<br>")


def compute_column_widths(rows: List[List[str]]) -> List[int]:
    """
    For pretty-printing: find the max width of each column
    across all rows (header + data).
    """
    if not rows:
        return []
    num_cols = max(len(row) for row in rows)
    widths = [0] * num_cols
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(normalize_cell(cell)))
    return widths


def pad_cell(cell: str, width: int) -> str:
    """Left-align cell content padded to `width` characters."""
    return normalize_cell(cell).ljust(width)


def build_separator(widths: List[int]) -> str:
    """
    Build the Markdown separator row, e.g.:
    | :--- | :--- | :--- |
    Minimum 3 dashes per column for valid Markdown.
    """
    parts = [":---" + "-" * max(0, w - 3) for w in widths]
    return "| " + " | ".join(parts) + " |"


def table_to_markdown(
    headers: List[str],
    rows: List[List[str]],
    pretty: bool = True
) -> str:
    """
    Convert a header list + row matrix into a Markdown table.

    Args:
        headers : Column header strings.
        rows    : List of rows; each row is a list of cell strings.
        pretty  : If True, pad columns to equal width (readable source).
                  If False, emit compact Markdown (smaller output).

    Returns:
        A valid GitHub-flavoured Markdown table string.

    Edge cases handled:
        - Missing cells in a row  → filled with empty string
        - Extra cells in a row    → truncated to header count
        - Multi-line cell content → collapsed with <br>
        - Empty table             → returns empty string
    """
    if not headers:
        return ""

    num_cols = len(headers)

    # Normalise rows — ensure every row has exactly num_cols cells
    normalised_rows = []
    for row in rows:
        padded = list(row) + [""] * num_cols    # extend if short
        normalised_rows.append(padded[:num_cols])  # truncate if long

    if pretty:
        # Include headers in width calculation
        all_rows = [headers] + normalised_rows
        widths = compute_column_widths(all_rows)

        header_line = "| " + " | ".join(
            pad_cell(h, widths[i]) for i, h in enumerate(headers)
        ) + " |"
        separator = build_separator(widths)
        data_lines = [
            "| " + " | ".join(
                pad_cell(cell, widths[i]) for i, cell in enumerate(row)
            ) + " |"
            for row in normalised_rows
        ]

    else:
        header_line = "| " + " | ".join(
            normalize_cell(h) for h in headers
        ) + " |"
        separator = "| " + " | ".join(["---"] * num_cols) + " |"
        data_lines = [
            "| " + " | ".join(normalize_cell(cell) for cell in row) + " |"
            for row in normalised_rows
        ]

    return "\n".join([header_line, separator] + data_lines)
