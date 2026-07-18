from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import duckdb

from src.config import DEFAULT_DATABASE_PATH, SCHEMA_PATH


class Database:
    """Central interface for accessing the DuckDB database."""

    def __init__(
        self,
        db_path: str | Path = DEFAULT_DATABASE_PATH,
        schema_path: str | Path = SCHEMA_PATH,
    ) -> None:
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)
        self._connection: duckdb.DuckDBPyConnection | None = None

    def connect(self) -> duckdb.DuckDBPyConnection:
        """Open the database connection if it is not already open."""
        if self._connection is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._connection = duckdb.connect(str(self.db_path))

        return self._connection

    def close(self) -> None:
        """Close the active database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def initialize(self) -> None:
        """Create all tables defined in schema.sql."""
        if not self.schema_path.exists():
            raise FileNotFoundError(
                f"Schema file does not exist: {self.schema_path}"
            )

        schema_sql = self.schema_path.read_text(encoding="utf-8")
        self.connect().execute(schema_sql)

    def execute(
        self,
        sql: str,
        parameters: Iterable[Any] | None = None,
    ) -> duckdb.DuckDBPyConnection:
        """Execute SQL with optional parameter binding."""
        connection = self.connect()

        if parameters is None:
            return connection.execute(sql)

        return connection.execute(sql, list(parameters))

    def fetch_all(
        self,
        sql: str,
        parameters: Iterable[Any] | None = None,
    ) -> list[tuple[Any, ...]]:
        """Execute a query and return all rows."""
        return self.execute(sql, parameters).fetchall()

    def list_tables(self) -> list[str]:
        """Return the names of all database tables."""
        rows = self.fetch_all("SHOW TABLES")
        return sorted(row[0] for row in rows)

    def table_exists(self, table_name: str) -> bool:
        """Check whether a table exists."""
        result = self.fetch_all(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'main'
              AND table_name = ?
            """,
            [table_name],
        )

        return result[0][0] > 0

    def __enter__(self) -> Database:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
