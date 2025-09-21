from core.config import TABLE_PREFIX
from pathlib import Path
from typing import List
import re

# ---------- Utility functions ----------
def sanitize_table_name(filename: str) -> str:
    """
    Given a filename (with or without extension), return a deterministic,
    safe table name prefixed with TABLE_PREFIX. Replace special chars/spaces with underscores.
    Example: "My file (v1).csv" -> "Data_Set_My_file_v1"
    """
    base = Path(filename).stem  # drop extension
    s = re.sub(r"[^\w]+", "_", base.strip())  # replace non-word chars with underscore
    s = re.sub(r"_{2,}", "_", s).strip("_")
    if re.match(r"^\d", s):
        s = "t_" + s
    return f"{TABLE_PREFIX}{s}"


def normalize_colname(col: str) -> str:
    """Make a column name safe: lowercase, underscores, remove special chars."""
    if col is None:
        return "col"
    c = str(col).strip()
    if c == "":
        return "col"
    c = re.sub(r"\s+", "_", c)
    c = re.sub(r"[^\w_]", "", c)
    c = c.lower()
    if re.match(r"^\d", c):
        c = "_" + c
    return c

def unique_column_names(cols: List[str]) -> List[str]:
    """
    Normalize and ensure unique column names by appending suffixes when needed.
    """
    out = []
    seen = {}
    for i, c in enumerate(cols):
        nc = normalize_colname(c) or f"col_{i}"
        if nc in seen:
            seen[nc] += 1
            nc = f"{nc}_{seen[nc]}"
        else:
            seen[nc] = 0
        out.append(nc)
    return out