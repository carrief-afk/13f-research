from pathlib import Path
from zipfile import BadZipFile, ZipFile

import polars as pl


INFOTABLE_SCHEMA_OVERRIDES = {
    "ACCESSION_NUMBER": pl.String,
    "NAMEOFISSUER": pl.String,
    "TITLEOFCLASS": pl.String,
    "CUSIP": pl.String,
    "FIGI": pl.String,
    "SSHPRNAMTTYPE": pl.String,
    "PUTCALL": pl.String,
    "INVESTMENTDISCRETION": pl.String,
    "OTHERMANAGER": pl.String,
}


class SECParser:
    """
    Parse SEC Form 13F quarterly ZIP archives.
    """

    def inspect_zip(
        self,
        zip_path: str | Path,
    ) -> list[str]:
        """
        Return sorted file names contained in a ZIP archive.
        """
        path = Path(zip_path)

        if not path.exists():
            raise FileNotFoundError(
                f"ZIP archive does not exist: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"ZIP archive path is not a file: {path}"
            )

        try:
            with ZipFile(path, "r") as zip_file:
                return sorted(zip_file.namelist())

        except BadZipFile as error:
            raise ValueError(
                f"Invalid ZIP archive: {path}"
            ) from error

    def read_tsv(
        self,
        zip_path: str | Path,
        file_name: str,
        n_rows: int | None = None,
    ) -> pl.DataFrame:
        """
        Read one TSV file directly from a SEC ZIP archive.
        """
        path = Path(zip_path)

        if not path.exists():
            raise FileNotFoundError(
                f"ZIP archive does not exist: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"ZIP archive path is not a file: {path}"
            )

        schema_overrides = None

        if file_name == "INFOTABLE.tsv":
            schema_overrides = INFOTABLE_SCHEMA_OVERRIDES

        try:
            with ZipFile(path, "r") as zip_file:
                if file_name not in zip_file.namelist():
                    raise FileNotFoundError(
                        f"{file_name} not found in {path.name}"
                    )

                with zip_file.open(file_name) as file:
                    return pl.read_csv(
                        file,
                        separator="\t",
                        encoding="utf8-lossy",
                        infer_schema_length=1000,
                        schema_overrides=schema_overrides,
                        n_rows=n_rows,
                    )

        except BadZipFile as error:
            raise ValueError(
                f"Invalid ZIP archive: {path}"
            ) from error

    def parse_submission(
        self,
        zip_path: str | Path,
        n_rows: int | None = None,
    ) -> pl.DataFrame:
        """Read SUBMISSION.tsv."""
        return self.read_tsv(
            zip_path=zip_path,
            file_name="SUBMISSION.tsv",
            n_rows=n_rows,
        )

    def parse_coverpage(
        self,
        zip_path: str | Path,
        n_rows: int | None = None,
    ) -> pl.DataFrame:
        """Read COVERPAGE.tsv."""
        return self.read_tsv(
            zip_path=zip_path,
            file_name="COVERPAGE.tsv",
            n_rows=n_rows,
        )

    def parse_summarypage(
        self,
        zip_path: str | Path,
        n_rows: int | None = None,
    ) -> pl.DataFrame:
        """Read SUMMARYPAGE.tsv."""
        return self.read_tsv(
            zip_path=zip_path,
            file_name="SUMMARYPAGE.tsv",
            n_rows=n_rows,
        )

    def parse_infotable(
        self,
        zip_path: str | Path,
        n_rows: int | None = None,
    ) -> pl.DataFrame:
        """Read INFOTABLE.tsv."""
        return self.read_tsv(
            zip_path=zip_path,
            file_name="INFOTABLE.tsv",
            n_rows=n_rows,
        )

    def parse_zip(
        self,
        zip_path: str | Path,
        n_rows: int | None = None,
    ) -> dict[str, pl.DataFrame]:
        """
        Parse all core tables from one SEC ZIP archive.
        """
        return {
            "submission": self.parse_submission(
                zip_path,
                n_rows=n_rows,
            ),
            "coverpage": self.parse_coverpage(
                zip_path,
                n_rows=n_rows,
            ),
            "summarypage": self.parse_summarypage(
                zip_path,
                n_rows=n_rows,
            ),
            "infotable": self.parse_infotable(
                zip_path,
                n_rows=n_rows,
            ),
        }
