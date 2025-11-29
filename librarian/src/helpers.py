from sqlalchemy.orm import Session
from librarian.database.models.readonly_columns import ReadonlyColumns


def validate_field_is_mutable(db: Session, field_name: str):
    config = db.query(ReadonlyColumns).first()
    
    if config and getattr(config, field_name, False):
        raise ValueError(f"Field {field_name} IS readonly!")