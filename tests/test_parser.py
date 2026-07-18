import pytest

from src.parser import SECParser
from src.importer import Importer


def test_parser_creation():
    parser = SECParser()
    assert parser is not None


def test_importer_creation():
    importer = Importer()
    assert importer is not None


def test_parser_not_implemented():
    parser = SECParser()

    with pytest.raises(NotImplementedError):
        parser.parse_zip("dummy.zip")
