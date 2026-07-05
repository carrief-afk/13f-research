from pathlib import Path
import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "db" / "holdings.duckdb"
SCHEMA_PATH = PROJECT_ROOT / "src" / "sql" / "schema.sql"


def connect(db_path: str | Path = DEFAULT_DB_PATH):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(db_path))


def init_database(db_path: str | Path = DEFAULT_DB_PATH):
    con = connect(db_path)
    schema_sql = SCHEMA_PATH.read_text()
    con.execute(schema_sql)
    return con


def list_tables(con):
    return [row[0] for row in con.execute("SHOW TABLES").fetchall()]
