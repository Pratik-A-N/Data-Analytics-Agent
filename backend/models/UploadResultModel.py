from pydantic import BaseModel

class UploadResult(BaseModel):
    table_name: str
    rows_loaded: int