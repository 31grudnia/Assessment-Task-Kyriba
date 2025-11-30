from sqlalchemy.orm import Session
from librarian.database.models.readonly_columns import ReadonlyColumns
from librarian.database.models.currency import Currency


def validate_field_is_mutable(db: Session, field_name: str):
    config = db.query(ReadonlyColumns).first()
    
    if config and getattr(config, field_name, False):
        raise ValueError(f"Field {field_name} IS readonly!")

def validate_amount_data(amount: int):
    if not isinstance(amount, int):
         raise ValueError("Amount must be an integer.")
    if amount < 0:
        raise ValueError("Amount cannot be negative!")


def validate_currency_data(currency_str: str):
    try:
       return Currency(currency_str) 
    except ValueError:
        valid_currencies = ", ".join([c.value for c in Currency])
        raise ValueError(f"Invalid currency '{currency_str}'. Allowed values are: {valid_currencies}")