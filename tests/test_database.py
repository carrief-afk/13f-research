from pathlib import Path

from src.database import Database


EXPECTED_TABLES = {
    "managers",
    "stocks",
    "filings",
    "holdings",
}


def test_database_initialization(tmp_path: Path) -> None:
    db_path = tmp_path / "test_holdings.duckdb"

    with Database(db_path=db_path) as db:
        db.initialize()

        assert set(db.list_tables()) == EXPECTED_TABLES

        for table_name in EXPECTED_TABLES:
            assert db.table_exists(table_name)


def test_database_file_persists(tmp_path: Path) -> None:
    db_path = tmp_path / "persistent.duckdb"

    with Database(db_path=db_path) as db:
        db.initialize()

    assert db_path.exists()

    with Database(db_path=db_path) as db:
        assert set(db.list_tables()) == EXPECTED_TABLES
