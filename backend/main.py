from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.ingest import router as ingest_router
from routers.analyze import router as analyze_router
from workflow.workflow import Workflow
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get CORS allowed origins from environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# for deployment on langgraph cloud
graph = Workflow().returnGraph()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# mount the ingestion router under /ingest
app.include_router(ingest_router, prefix="/ingest", tags=["ingest"])

# mount the analyze router under /analyze
app.include_router(analyze_router, prefix="/analyze", tags=["analyze"])