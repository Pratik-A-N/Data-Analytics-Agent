# app/routers/ingest.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict
from services.ingest_service import process_upload_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict:
    """
    Upload endpoint that accepts .csv or .xlsx files.
    Delegates processing to the ingest service.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # delegate the heavy lifting to the service (which uses temp files internally)
    result = await process_upload_file(file)  # returns dict with table_name and rows_loaded
    return result
