from fastapi import FastAPI
from routers.ingest import router as ingest_router
from routers.analyze import router as analyze_router
from workflow.workflow import Workflow

app = FastAPI()

# for deployment on langgraph cloud
graph = Workflow().returnGraph()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# mount the ingestion router under /ingest
app.include_router(ingest_router, prefix="/ingest", tags=["ingest"])

# mount the analyze router under /analyze
app.include_router(analyze_router, prefix="/analyze", tags=["analyze"])