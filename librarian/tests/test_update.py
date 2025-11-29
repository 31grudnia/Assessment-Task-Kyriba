import pytest

from librarian.database.models.file import HeaderModel, FooterModel
from librarian.database.models.readonly_columns import ReadonlyColumns
from librarian.src.crud import update_file_field


def test_update_header_field(seeded_db):
    update_file_field(seeded_db, file_id=1, field_value="name", new_value="Mike", transaction_id=None)
    updated_header = seeded_db.get(HeaderModel, 1)

    assert updated_header.name == "Mike"

def test_update_footer_field(seeded_db):
    config = seeded_db.query(ReadonlyColumns).first()
    config.total_counter = False
    seeded_db.commit()

    update_file_field(seeded_db, file_id=1, field_value="total_counter", new_value=99, transaction_id=None)
    
    updated_footer = seeded_db.query(FooterModel).filter_by(header_id=1).first()
    assert updated_footer.total_counter == 99

def test_update_transaction_amount_recalculates_footer(seeded_db):
    footer = seeded_db.query(FooterModel).filter_by(header_id=1).first()
    assert footer.control_sum == 300

    update_file_field(
        db=seeded_db, 
        file_id=1, 
        field_value="amount", 
        new_value=500, 
        transaction_id=1
    )

    seeded_db.refresh(footer)
    assert footer.control_sum == 700

def test_update_file_not_found(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        update_file_field(seeded_db, file_id=999, field_value="name", new_value="X", transaction_id=None)
    assert "999 does NOT exist" in str(excinfo.value)

def test_update_transaction_not_found(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        update_file_field(seeded_db, file_id=1, field_value="amount", new_value=10, transaction_id=999)
    assert "999 does NOT exist" in str(excinfo.value)

def test_update_field_not_exist(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        update_file_field(seeded_db, file_id=1, field_value="potato", new_value="X", transaction_id=None)
    assert "potato does NOT exist" in str(excinfo.value)

def test_update_fails_when_field_is_readonly(seeded_db):
    config = seeded_db.query(ReadonlyColumns).first()
    config.name = True
    seeded_db.commit()

    with pytest.raises(ValueError) as excinfo:
        update_file_field(seeded_db, file_id=1, field_value="name", new_value="Locked", transaction_id=None)
    
    assert "IS readonly" in str(excinfo.value)

def test_update_fails_on_default_readonly_fields(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        update_file_field(seeded_db, file_id=1, field_value="control_sum", new_value=9999, transaction_id=None)
    
    assert "IS readonly" in str(excinfo.value)

def test_can_unlock_and_update_field(seeded_db):
    config = seeded_db.query(ReadonlyColumns).first()
    config.address = True 
    seeded_db.commit()

    with pytest.raises(ValueError):
         update_file_field(seeded_db, 1, "address", "New Addr", None)

    config.address = False
    seeded_db.commit()

    update_file_field(seeded_db, 1, "address", "New Addr", None)
    header = seeded_db.get(HeaderModel, 1)
    assert header.address == "New Addr"
