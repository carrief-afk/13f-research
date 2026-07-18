from pathlib import Path

from src.database import Database
from src.parser import SECParser


class Importer:
    """
    Import SEC filings into DuckDB.
    """

    def __init__(self):
        self.database = Database()
        self.parser = SECParser()

    def import_zip(self, zip_path: str | Path):
        """
        Parse one ZIP file and write to database.

        Implementation will be added later.
        """
        raise NotImplementedError(
            "Importer will be implemented in Task 5."
        )
