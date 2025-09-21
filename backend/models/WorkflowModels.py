from typing import Optional, Dict, Any, List
from pydantic import BaseModel

# ---------- Request / Response models ----------
class QueryRequest(BaseModel):
    user_query: str
    table_id: str
