from pathlib import Path
from zipfile import ZipFile

import polars as pl
import pytest

from src.importer import Importer
from src.parser import SECParser


def test_parser_creation() -> None:
    parser = SECParser()

    assert isinstance(parser, SECParser)


def test_importer_creation() -> None:
    importer = Importer()

    assert isinstance(importer.parser, SECParser)


def test_inspect_zip_returns_sorted_file_names(
    tmp_path: Path,
) -> None:
    zip_path = tmp_path / "sample.zip"

    with ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr("SUBMISSION.tsv", "A\tB\n")
        zip_file.writestr("INFOTABLE.tsv", "C\tD\n")

    parser = SECParser()
    result = parser.inspect_zip(zip_path)

    assert result == [
        "INFOTABLE.tsv",
        "SUBMISSION.tsv",
    ]


def test_inspect_zip_missing_file(
    tmp_path: Path,
) -> None:
    parser = SECParser()
    missing_path = tmp_path / "missing.zip"

    with pytest.raises(FileNotFoundError):
        parser.inspect_zip(missing_path)


def test_inspect_zip_rejects_directory(
    tmp_path: Path,
) -> None:
    parser = SECParser()

    with pytest.raises(
        ValueError,
        match="not a file",
    ):
        parser.inspect_zip(tmp_path)


def test_inspect_zip_invalid_zip(
    tmp_path: Path,
) -> None:
    invalid_path = tmp_path / "invalid.zip"
    invalid_path.write_text(
        "This is not a ZIP archive.",
        encoding="utf-8",
    )

    parser = SECParser()

    with pytest.raises(
        ValueError,
        match="Invalid ZIP archive",
    ):
        parser.inspect_zip(invalid_path)


def test_read_tsv_returns_polars_dataframe(
    tmp_path: Path,
) -> None:
    zip_path = tmp_path / "sample.zip"

    content = (
        "ACCESSION_NUMBER\tNAMEOFISSUER\tCUSIP\tOTHERMANAGER\n"
        "0001\tAPPLE INC\t037833100\t1, 2\n"
    )

    with ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr(
            "INFOTABLE.tsv",
            content,
        )

    parser = SECParser()

    result = parser.read_tsv(
        zip_path=zip_path,
        file_name="INFOTABLE.tsv",
    )

    assert isinstance(result, pl.DataFrame)
    assert result.height == 1
    assert result.width == 4
    assert result["NAMEOFISSUER"][0] == "APPLE INC"


def test_read_tsv_preserves_string_columns(
    tmp_path: Path,
) -> None:
    zip_path = tmp_path / "sample.zip"

    content = (
        "ACCESSION_NUMBER\tNAMEOFISSUER\tCUSIP\tOTHERMANAGER\n"
        "0001\tAPPLE INC\t037833100\t1, 2\n"
    )

    with ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr(
            "INFOTABLE.tsv",
            content,
        )

    parser = SECParser()

    result = parser.read_tsv(
        zip_path=zip_path,
        file_name="INFOTABLE.tsv",
    )

    assert result.schema["ACCESSION_NUMBER"] == pl.String
    assert result.schema["CUSIP"] == pl.String
    assert result.schema["OTHERMANAGER"] == pl.String

    assert result["ACCESSION_NUMBER"][0] == "0001"
    assert result["CUSIP"][0] == "037833100"
    assert result["OTHERMANAGER"][0] == "1, 2"


def test_read_tsv_missing_internal_file(
    tmp_path: Path,
) -> None:
    zip_path = tmp_path / "sample.zip"

    with ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr(
            "SUBMISSION.tsv",
            "A\tB\n1\t2\n",
        )

    parser = SECParser()

    with pytest.raises(
        FileNotFoundError,
        match="INFOTABLE.tsv not found",
    ):
        parser.read_tsv(
            zip_path=zip_path,
            file_name="INFOTABLE.tsv",
        )


def test_parse_zip_returns_core_tables(
    tmp_path: Path,
) -> None:
    zip_path = tmp_path / "sample.zip"

    with ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr(
            "SUBMISSION.tsv",
            "ACCESSION_NUMBER\tFILINGMANAGER_NAME\n"
            "0001\tTEST MANAGER\n",
        )

        zip_file.writestr(
            "COVERPAGE.tsv",
            "ACCESSION_NUMBER\tREPORTCALENDARORQUARTER\n"
            "0001\t2025-12-31\n",
        )

        zip_file.writestr(
            "SUMMARYPAGE.tsv",
            "ACCESSION_NUMBER\tTABLEENTRYTOTAL\n"
            "0001\t1\n",
        )

        zip_file.writestr(
            "INFOTABLE.tsv",
            "ACCESSION_NUMBER\tNAMEOFISSUER\tCUSIP\tOTHERMANAGER\n"
            "0001\tAPPLE INC\t037833100\t1, 2\n",
        )

    parser = SECParser()

    result = parser.parse_zip(zip_path)

    assert isinstance(result, dict)

    assert set(result.keys()) == {
        "submission",
        "coverpage",
        "summarypage",
        "infotable",
    }

    assert result["submission"].height == 1
    assert result["coverpage"].height == 1
    assert result["summarypage"].height == 1
    assert result["infotable"].height == 1
