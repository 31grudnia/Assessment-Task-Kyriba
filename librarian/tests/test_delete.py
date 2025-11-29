import pytest

from librarian.database.models.file import HeaderModel, FooterModel, TransactionModel
from librarian.src.crud import delete_file_by_id, delete_transaction_by_id


def test_delete_file_success(seeded_db):
    file_id = 1
    
    assert seeded_db.get(HeaderModel, file_id) is not None
    assert seeded_db.query(FooterModel).filter_by(header_id=file_id).first() is not None
    assert seeded_db.query(TransactionModel).filter_by(header_id=file_id).count() > 0

    delete_file_by_id(seeded_db, file_id)

    assert seeded_db.get(HeaderModel, file_id) is None
    assert seeded_db.query(FooterModel).filter_by(header_id=file_id).first() is None
    assert seeded_db.query(TransactionModel).filter_by(header_id=file_id).count() == 0

def test_delete_file_not_found(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        delete_file_by_id(seeded_db, file_id=999)
    assert "999 does NOT exist!" in str(excinfo.value)

def test_delete_transaction_success_and_recalc(seeded_db):
    footer = seeded_db.query(FooterModel).filter_by(header_id=1).first()
    assert footer.control_sum == 300
    
    delete_transaction_by_id(seeded_db, file_id=1, transaction_id=1)
    
    deleted_tx = (seeded_db.query(TransactionModel)
                  .filter_by(header_id=1, counter=1)
                  .first())
    assert deleted_tx is None
    
    seeded_db.refresh(footer)
    assert footer.control_sum == 200

def test_delete_transaction_not_found(seeded_db):
    with pytest.raises(ValueError) as excinfo:
        delete_transaction_by_id(seeded_db, file_id=1, transaction_id=999)
    assert "does NOT exist" in str(excinfo.value)