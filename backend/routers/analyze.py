from fastapi import APIRouter, Depends, HTTPException
from core.config import ALLOWED_VIZ, MAX_ROWS_SERVER, MAX_QUERY_LENGTH, REQUEST_TIMEOUT_SECONDS
from models.WorkflowModels import *
from workflow.workflow import Workflow
import logging
import httpx
import asyncio

logger = logging.getLogger("api_router_query_noauth")

router = APIRouter()

@router.post("/query")
async def run_query(req: QueryRequest):
    # Basic validation
    q = (req.user_query or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="query cannot be empty")
    if len(q) > MAX_QUERY_LENGTH:
        raise HTTPException(status_code=400, detail=f"query exceeds max length {MAX_QUERY_LENGTH}")
    ds = (req.table_id or "").strip()
    if not ds:
        raise HTTPException(status_code=400, detail="dataset_id cannot be empty")

    # Call LangGraph worker
    try:
        result = Workflow().execute_workflow(user_query=q, table_id=ds)
        return result
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.exception("Failed to reach LangGraph worker: %s", e)
        raise HTTPException(status_code=502, detail="Failed to reach LangGraph worker")
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="LangGraph worker timed out")
    except Exception as e:
        logger.exception("Unexpected error calling LangGraph: %s", e)
        raise HTTPException(status_code=500, detail="Internal error while calling LangGraph")