import pytest

from librarian.database.models.file import HeaderModel, FooterModel, TransactionModel
from librarian.src.crud import get_file_section, get_file_field


def test_get_file_section_header(seeded_db):
    result = get_file_section(db=seeded_db, file_id=1, section_id=1)
    assert isinstance(result, HeaderModel)
    assert result.name == "John"

def test_get_file_section_transactions(seeded_db):
    result = get_file_section(seeded_db, file_id=1, section_id=2)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].amount == 100
    assert result[1].amount == 200

def test_get_file_section_footer(seeded_db):
    result = get_file_section(seeded_db, file_id=1, section_id=3)
    assert isinstance(result, FooterModel)
    assert result.total_counter == 2

def test_get_file_section_invalid_id(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        get_file_section(seeded_db, file_id=1, section_id=99)
    assert "Invalid section" in str(excinfo.value)