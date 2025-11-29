import pytest

from librarian.database.models.file import HeaderModel
from librarian.src.crud import add_file, add_transaction_to_file


def test_add_file_creates_full_structure(seeded_db):
    header_data = {
        "name": "John",
        "surname": "Doe",
        "patronymic": "Smith",
        "address": "123 Main St"
    }
    transaction_data = {"amount": 100, "currency": "USD"}

    header = add_file(seeded_db, header_data, transaction_data)

    assert header.id is not None
    assert header.name == "John"
    
    assert header.footer is not None
    assert header.footer.total_counter == 1
    assert header.footer.control_sum == 100

    assert len(header.transactions) == 1
    assert header.transactions[0].amount == 100
    assert header.transactions[0].counter == 1

def test_add_transaction_updates_footer_and_counters(seeded_db):
    file_id = 1
    new_data = {"amount": 50, "currency": "USD"}

    header = seeded_db.get(HeaderModel, file_id)
    initial_sum = header.footer.control_sum
    initial_count = header.footer.total_counter

    new_transaction = add_transaction_to_file(seeded_db, file_id, new_data)
    
    seeded_db.refresh(header.footer)

    assert new_transaction.id is not None
    assert new_transaction.header_id == file_id
    assert new_transaction.counter == initial_count + 1
    
    assert header.footer.total_counter == initial_count + 1
    assert header.footer.control_sum == initial_sum + 50

def test_add_transaction_to_non_existent_file(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        add_transaction_to_file(seeded_db, 999, {"amount": 100, "currency": "USD"})
    
    assert "999 does NOT exist" in str(excinfo.value)