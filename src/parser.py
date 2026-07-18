from pathlib import Path

import polars as pl


class SECParser:
    """
    Parse SEC 13F filing files.

    Current version:
        framework only
    """

    def __init__(self):
        pass

    def parse_zip(self, zip_path: str | Path) -> pl.DataFrame:
        """
        Parse one SEC ZIP archive.

        Parameters
        ----------
        zip_path
            Path to a SEC quarterly ZIP.

        Returns
        -------
        Polars DataFrame
        """

        raise NotImplementedError(
            "ZIP parsing will be implemented in Task 5."
        )
