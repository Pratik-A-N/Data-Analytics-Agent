from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

# ---------------- CONFIG ----------------
PG_USER = os.getenv("PG_USER", "")
PG_PASS = os.getenv("PG_PASS", "")
PG_HOST = os.getenv("PG_HOST", "")
PG_PORT = os.getenv("PG_PORT", "")
PG_DB   = os.getenv("PG_DB", "")

DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    return _engine

def get_raw_psycopg_conn():
    """Return a new psycopg2 connection (caller must close)."""
    import psycopg2
    return psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASS, dbname=PG_DB)


ALLOWED_EXT = {".csv", ".xlsx"}  # allowed extensions (xlsx included)
TABLE_PREFIX = "Data_Set_"       # prefix required
REQUEST_TIMEOUT_SECONDS = float(os.getenv("QUERY_TIMEOUT", "60"))
MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "4000"))
MAX_ROWS_SERVER = int(os.getenv("MAX_ROWS_RETURN", "5000"))
ALLOWED_VIZ = {"bar", "line", "scatter", "table"}