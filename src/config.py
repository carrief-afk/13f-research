from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DATABASE_DIR = DATA_DIR / "db"

DEFAULT_DATABASE_PATH = DATABASE_DIR / "holdings.duckdb"
SCHEMA_PATH = PROJECT_ROOT / "src" / "sql" / "schema.sql"
