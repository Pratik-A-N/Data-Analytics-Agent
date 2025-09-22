from pathlib import Path
from fastapi import UploadFile, HTTPException
import csv
from typing import List, Dict, Any
from core.config import ALLOWED_EXT, get_raw_psycopg_conn
from core.utility import *
from core.db_helper import *
import tempfile
import pandas as pd
import os

async def process_upload_file(upload_file: UploadFile) -> Dict[str, Any]:
    """
    Process UploadFile, infer column types and create table with typed columns,
    normalize TIMESTAMP-like columns to Postgres-friendly format, then COPY CSV into table.
    Returns {"table_name":..., "rows_loaded":...}
    NOTE: this function relies on these helpers you already have:
      - unique_column_names(orig_cols) -> list[str]
      - infer_sql_type(series) -> str
      - sanitize_table_name(filename) -> str
      - get_raw_psycopg_conn() -> psycopg2 connection
      - create_table_with_types(conn, table_name, columns, types_map)
      - copy_csv_into_table(conn, tmp_out_path, table_name, columns)
    """
    print(f"Processing upload file: {upload_file.filename}, content_type={upload_file.content_type}")
    filename = upload_file.filename
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Incompatible File. Please Upload file .csv/.xlsx")

    # save upload to a temp file (async read)
    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    # compute table name
    table_name = sanitize_table_name(filename)  # you already have this function

    # Check master_data_repository for existing table
    conn = get_raw_psycopg_conn()
    try:
        with conn.cursor() as cur:
            # First ensure the master_data_repository table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS master_data_repository (
                file_name VARCHAR(255) PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                row_count INTEGER
                )
            """)
            # Check if table exists in master_data_repository
            cur.execute("""
                SELECT created_at 
                FROM master_data_repository 
                WHERE file_name = %s
                LIMIT 1
            """, (table_name,))
            
            result = cur.fetchone()
            
            if result:
                created_at = result[0]
                created_ts = pd.to_datetime(created_at, utc=True)   # makes it tz-aware (UTC)
                current_time = pd.Timestamp.now(tz="UTC")   
                time_diff = current_time - created_ts 
                
                # If time difference is more than 6 hours
                if time_diff.total_seconds() > 6 * 3600:
                    # Delete the entry from master_data_repository
                    cur.execute("""
                        DELETE FROM master_data_repository 
                        WHERE file_name = %s
                    """, (table_name,))
                    conn.commit()
                else:
                    # If table exists and time difference is less than 6 hours
                    # Get the row count and return early
                    cur.execute("""
                        SELECT row_count 
                        FROM master_data_repository 
                        WHERE file_name = %s
                    """, (table_name,))
                    row_count = cur.fetchone()[0]
                    return {"table_name": table_name, "rows_loaded": int(row_count)}
    finally:
        conn.close()

    try:
        content = await upload_file.read()
        tmp_in.write(content)
        tmp_in.flush()
        tmp_in.close()
        tmp_path = Path(tmp_in.name)

        # load to pandas
        if ext == ".csv":
            df = pd.read_csv(tmp_path, low_memory=False)
        else:
            df = pd.read_excel(tmp_path)

        if df.shape[1] == 0:
            raise HTTPException(status_code=400, detail="Uploaded file has no columns")

        orig_cols = list(df.columns)
        columns = unique_column_names(orig_cols)  # you already have this function
        df.columns = columns

        # infer types for each column
        types_map = {}
        for col in columns:
            try:
                types_map[col] = infer_sql_type(df[col])
            except Exception:
                types_map[col] = "TEXT"

        # --- NORMALIZE TIMESTAMP COLUMNS ---
        # For any column inferred as TIMESTAMP, coerce using pandas and format to
        # 'YYYY-MM-DD HH:MM:SS' so Postgres COPY into TIMESTAMP succeeds.
        for col, col_type in types_map.items():
            if col_type == "TIMESTAMP":
                # Attempt to parse common timestamp formats (including MM/DD/YYYY hh:mm:ss AM/PM)
                try:
                    parsed = pd.to_datetime(df[col], errors="coerce", infer_datetime_format=True)
                except Exception:
                    # Fallback: treat everything as NaT (will be emptied)
                    parsed = pd.Series([pd.NaT] * len(df), index=df.index)

                # Log a few unparseable samples for debugging (optional)
                bad_mask = parsed.isna() & df[col].notna()
                if bad_mask.any():
                    bad_samples = df.loc[bad_mask, col].head(5).tolist()
                    if bad_samples:
                        print(f"[warn] Unparseable values in column '{col}': {bad_samples}")

                # Format parsed datetimes to Postgres-friendly 'YYYY-MM-DD HH:MM:SS'
                # NaT -> NaN -> replaced with empty string
                df[col] = parsed.dt.strftime("%Y-%m-%d %H:%M:%S")
                df[col] = df[col].fillna("")

        # prepare a normalized CSV with header matching sanitized column names
        tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8", newline="")
        tmp_out_path = Path(tmp_out.name)
        writer = csv.writer(tmp_out)
        writer.writerow(columns)
        for row in df.itertuples(index=False, name=None):
            # convert NaN/NaT to empty
            row_fixed = [("" if (pd.isna(v) or v is pd.NaT) else v) for v in row]
            writer.writerow(row_fixed)
        tmp_out.close()

        # open a raw psycopg2 connection for DDL + COPY
        conn = get_raw_psycopg_conn()
        try:
            # create table with inferred types (drop if exists)
            create_table_with_types(conn, table_name, columns, types_map)

            # COPY CSV into table (reuse your existing function)
            rows_loaded = copy_csv_into_table(conn, tmp_out_path, table_name, columns)
        finally:
            conn.close()

        # Update master_data_repository with the new table entry
        conn = get_raw_psycopg_conn()
        try:
            with conn.cursor() as cur:
                # First ensure the master_data_repository table exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS master_data_repository (
                        file_name VARCHAR(255) PRIMARY KEY,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        row_count INTEGER
                    )
                """)
                
                # Simple insert since we handle existing entries earlier
                cur.execute("""
                    INSERT INTO master_data_repository (file_name, row_count, created_at)
                    VALUES (%s, %s, CURRENT_TIMESTAMP)
                """, (table_name, rows_loaded))
                conn.commit()
        finally:
            conn.close()

        return {"table_name": table_name, "rows_loaded": int(rows_loaded)}

    finally:
        # cleanup temp files
        try:
            if tmp_in:
                os.unlink(tmp_in.name)
        except Exception:
            pass
        try:
            if 'tmp_out_path' in locals() and tmp_out_path.exists():
                os.unlink(tmp_out_path)
        except Exception:
            pass
