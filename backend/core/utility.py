from core.config import TABLE_PREFIX
from pathlib import Path
from typing import List, Dict
import re
import pandas as pd
import psycopg2
from psycopg2 import sql

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

# Helper: infer SQL type for a pandas Series
def infer_sql_type(sr: pd.Series) -> str:
    non_null = sr.dropna()
    if non_null.empty:
        return "TEXT"

    # Work with string representations for some checks
    sample = non_null.astype(str).sample(min(len(non_null), 500), random_state=0) if len(non_null) > 500 else non_null.astype(str)

    # 1) Datetime detection
    parsed_dt = pd.to_datetime(sample, errors="coerce", infer_datetime_format=True)
    valid_dt_frac = parsed_dt.notna().mean()
    if valid_dt_frac >= 0.9:
        # if all values lack time part we could choose DATE, but default to TIMESTAMP
        return "TIMESTAMP"

    # 2) Boolean detection (common textual booleans)
    bool_like = sample.str.lower().isin({"true", "false", "t", "f", "yes", "no", "1", "0"})
    if bool_like.mean() >= 0.95:
        return "BOOLEAN"

    # 3) Numeric detection
    numeric = pd.to_numeric(sample, errors="coerce")
    valid_num_frac = numeric.notna().mean()
    if valid_num_frac >= 0.9:
        return "DOUBLE PRECISION"

    # 4) Fallback to text/varchar with length heuristics
    max_len = int(sample.str.len().max())
    # if very long, use TEXT
    if max_len > 1000:
        return "TEXT"
    # otherwise use VARCHAR with some margin
    # round up to nearest 25
    
    return "TEXT"

def create_table_with_types(conn: psycopg2.extensions.connection, table_name: str, columns: list, types_map: Dict[str, str]):
    """
    Drop table if exists and create with inferred column types.
    """
    with conn.cursor() as cur:
        # drop if exists
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table_name)))
        # build column definitions
        col_defs = []
        for col in columns:
            col_type = types_map.get(col, "TEXT")
            # safe identifier and type insertion
            col_defs.append(sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(col_type)))
        create_stmt = sql.SQL("CREATE TABLE {} ( {} )").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(col_defs),
        )
        cur.execute(create_stmt)
    conn.commit()