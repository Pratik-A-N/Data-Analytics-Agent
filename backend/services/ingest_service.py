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
    Top-level function to process an UploadFile:
    - validate extension
    - save to temp file
    - read into pandas, normalize columns
    - create table (drop if exists), write normalized csv and COPY into table
    - cleanup and return {"table_name":..., "rows_loaded":...}
    """
    filename = upload_file.filename
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Incompatible File. Please Upload file .csv/.xlsx")

    # save upload to a temp file (async read)
    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    try:
        # read bytes (UploadFile provides async interface)
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
        columns = unique_column_names(orig_cols)
        df.columns = columns

        # prepare a normalized CSV with header matching sanitized column names
        tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8", newline="")
        tmp_out_path = Path(tmp_out.name)
        writer = csv.writer(tmp_out)
        writer.writerow(columns)
        for row in df.itertuples(index=False, name=None):
            # convert NaN to empty
            row_fixed = [("" if (pd.isna(v)) else v) for v in row]
            writer.writerow(row_fixed)
        tmp_out.close()

        # compute table name
        table_name = sanitize_table_name(filename)

        # open a raw psycopg2 connection for DDL + COPY
        conn = get_raw_psycopg_conn()
        try:
            # create table (drop if exists)
            create_table_drop_if_exists(conn, table_name, columns)
            # COPY CSV into table
            rows_loaded = copy_csv_into_table(conn, tmp_out_path, table_name, columns)
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