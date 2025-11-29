from typing import Optional, Any

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload
from librarian.database.models.file import HeaderModel, TransactionModel, FooterModel

# GET
def get_all_files(db: Session):
    query = (db.query(HeaderModel)
             .options(joinedload(HeaderModel.footer))
             .options(selectinload(HeaderModel.transactions))
             .order_by(HeaderModel.id)
             .all())
    
    return query


def get_file_by_id(db: Session, file_id: int):
    query = (db.query(HeaderModel)
             .options(joinedload(HeaderModel.footer))
             .options(selectinload(HeaderModel.transactions))
             .filter(HeaderModel.id == file_id)
             .first())
    
    return query


def get_file_section(db: Session, file_id: int, section_id: int):
    if section_id not in range(1, 4):
        raise ValueError(f"Invalid section {section_id}. Must be 1 (Header), 2 (Transactions), or 3 (Footer).")
    
    if section_id == 1:
        return db.query(HeaderModel).filter(HeaderModel.id == file_id).first()
    
    if section_id == 2:
        return db.query(TransactionModel).filter(TransactionModel.header_id == file_id).all()
    
    if section_id == 3:
        return db.query(FooterModel).filter(FooterModel.header_id == file_id).first()
    
# UPDATE
def get_file_field(db: Session, file_id: int, field_value: str):
    models = [HeaderModel, FooterModel, TransactionModel]
    field_exists = any(hasattr(m, field_value) for m in models)
    if not field_exists:
        raise ValueError(f"Field '{field_value}' does NOT exist!")
    
    header_obj = db.get(HeaderModel, file_id)
    if not header_obj:
        raise ValueError(f"File with id:{file_id} does NOT exist!")
    
    if hasattr(header_obj, field_value):
        return getattr(header_obj, field_value)

    if hasattr(header_obj.footer, field_value):
        return getattr(header_obj.footer, field_value)
    
    if hasattr(TransactionModel, field_value):
        return [getattr(t, field_value) for t in header_obj.transactions]

    raise ValueError(f"Field {field_value} does NOT exist!")


def update_file_field(db: Session, file_id: int, field_value: str, new_value: Any, transaction_id: Optional[int]):
    header_obj = db.get(HeaderModel, file_id)
    if not header_obj:
        raise ValueError(f"File with id:{file_id} does NOT exist!")
    
    if (transaction_id is not None and 
        hasattr(TransactionModel, field_value)):
        transaction_obj = (db.query(TransactionModel)
                           .filter_by(counter=transaction_id, header_id=file_id)
                           .first())
        
        if not transaction_obj:
            raise ValueError(f"Transaction with id:{transaction_id} does NOT exist!")
        
        setattr(transaction_obj, field_value, new_value)
        db.flush()

        if field_value == "amount":
            transactions_amount = (db.query(func.sum(TransactionModel.amount))
                                   .filter(TransactionModel.header_id==file_id)
                                   .scalar())
            db.query(FooterModel).filter_by(header_id=file_id).update({"control_sum": transactions_amount})
        
        db.commit()
        return transaction_obj

    if hasattr(header_obj, field_value):
        setattr(header_obj, field_value, new_value)
        db.commit()
        return header_obj
    
    if hasattr(header_obj.footer, field_value):
        setattr(header_obj.footer, field_value, new_value)
        db.commit()
        return header_obj.footer

    if transaction_id is not None:
        raise ValueError(f"Transaction with id:{transaction_id} does NOT exist!")
    raise ValueError(f"Field {field_value} does NOT exist!")

# DELETE
def delete_file_by_id(db: Session, file_id: int):
    file_obj = db.get(HeaderModel, file_id)
    if not file_obj:
        raise ValueError(f"File with id:{file_id} does NOT exist!")
    
    db.delete(file_obj)
    db.commit()


def delete_transaction_by_id(db: Session, file_id: int, transaction_id: int):
    transaction_obj = (db.query(TransactionModel)
                       .filter_by(counter=transaction_id, header_id=file_id)
                       .first())
        
    if not transaction_obj:
        raise ValueError(f"Transaction with id:{transaction_id} does NOT exist!")
    
    db.delete(transaction_obj)
    db.flush()

    transactions_amount = (db.query(func.sum(TransactionModel.amount))
                                   .filter(TransactionModel.header_id==file_id)
                                   .scalar())
    db.query(FooterModel).filter_by(header_id=file_id).update({"control_sum": transactions_amount})
    db.commit()