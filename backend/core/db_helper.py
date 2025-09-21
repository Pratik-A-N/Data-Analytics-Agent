from psycopg2 import sql
from pathlib import Path
from typing import List

# ---------- DB helpers ----------
def create_table_drop_if_exists(conn, table_name: str, columns: List[str]):
    """
    Create table with TEXT columns and id BIGSERIAL PK.
    Uses a psycopg2 connection and psycopg2.sql for safe identifiers.
    """
    cur = conn.cursor()
    # drop if exists
    cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table_name)))
    # build column definitions
    col_defs = []
    for c in columns:
        col_defs.append(sql.SQL("{} TEXT").format(sql.Identifier(c)))
    create_stmt = sql.SQL("CREATE TABLE {} (id BIGSERIAL PRIMARY KEY, {} );").format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(col_defs)
    )
    cur.execute(create_stmt)
    conn.commit()

def copy_csv_into_table(conn, csv_path: Path, table_name: str, columns: List[str]) -> int:
    """
    Use COPY to load CSV into the named table. Returns row count.
    Assumes csv header matches columns exactly.
    """
    cur = conn.cursor()
    cols_ident = sql.SQL(", ").join(map(sql.Identifier, columns))
    copy_stmt = sql.SQL("COPY {} ({}) FROM STDIN WITH CSV HEADER").format(sql.Identifier(table_name), cols_ident)
    with open(csv_path, "r", encoding="utf-8") as f:
        cur.copy_expert(copy_stmt, f)
    conn.commit()
    # get count
    cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table_name)))
    cnt = cur.fetchone()[0]
    return cnt