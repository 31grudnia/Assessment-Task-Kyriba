from typing import Optional

import typer
from rich.console import Console

from librarian.src import crud
from librarian.database.database import get_db
from docsli.src.generator import generate_fixed_width_content
from logger.logger import setup_logger

app = typer.Typer(help="Librarian File Management CLI")
console = Console()
logger = setup_logger("cli")


@app.command("list-files")
def list_files():
    db = next(get_db())
    try:
        files = crud.get_all_files(db)
        if not files:
            logger.warning("No files found in database.")
            return

        logger.info(f"Listing {len(files)} files.")
        for f in files:
            generate_fixed_width_content(f)
            
    except Exception as e:
        logger.error(f"Failed to list files: {e}")


@app.command()
def create_file(
    name: str, surname: str, patronymic: str, address: str, 
    amount: int, currency: str
):
    db = next(get_db())
    header_data = {
        "name": name, "surname": surname, 
        "patronymic": patronymic, "address": address
    }
    transaction_data = {"amount": amount, "currency": currency}
    
    try:
        new_header = crud.add_file(db, header_data, transaction_data)
        logger.info(f"File created successfully with ID: {new_header.id}")
    except Exception as e:
        logger.error(f"Failed to create file: {e}")


@app.command()
def get_value(file_id: int, field_name: str):
    db = next(get_db())
    try:
        val = crud.get_file_field(db, file_id, field_name)
        logger.info(f"File {file_id} - {field_name}: {val}")
    except Exception as e:
        logger.error(f"Error getting value: {e}")


@app.command()
def update_value(
    file_id: int, 
    field_name: str, 
    new_value: str, 
    transaction_id: Optional[int] = typer.Option(None, "--tx-id")
):
    db = next(get_db())

    val_to_save = new_value
    if field_name in ["amount", "counter"]:
        if not new_value.isdigit():
            logger.error(f"Field '{field_name}' requires an integer value.")
            return
        val_to_save = int(new_value)

    try:
        crud.update_file_field(db, file_id, field_name, val_to_save, transaction_id)
        logger.info(f"File {file_id} updated. Field '{field_name}' set to '{val_to_save}'.")
    except Exception as e:
        logger.error(f"Update failed: {e}")


@app.command()
def add_transaction(file_id: int, amount: int, currency: str):
    db = next(get_db())

    tx_data = {"amount": amount, "currency": currency}
    try:
        crud.add_transaction_to_file(db, file_id, tx_data)
        logger.info(f"Transaction added to File {file_id} (Amount: {amount}, Currency: {currency}).")
    except Exception as e:
        logger.error(f"Failed to add transaction: {e}")


@app.command()
def lock_field(field_name: str, locked: bool = True):
    db = next(get_db())
    try:
        crud.set_field_readonly(db, field_name, locked)
        state = "LOCKED" if locked else "UNLOCKED"
        logger.info(f"Field configuration updated: '{field_name}' is now {state}.")
    except Exception as e:
        logger.error(f"Failed to lock/unlock field: {e}")


@app.command()
def delete_file(file_id: int):
    db = next(get_db())
    try:
        crud.delete_file_by_id(db, file_id)
        logger.info(f"File {file_id} deleted successfully.")
    except Exception as e:
        logger.error(f"Failed to delete file {file_id}: {e}")


@app.command()
def delete_transaction(file_id: int, transaction_id: int):
    db = next(get_db())
    try:
        crud.delete_transaction_by_id(db, file_id, transaction_id)
        logger.info(f"Transaction {transaction_id} deleted from File {file_id}.")
    except Exception as e:
        logger.error(f"Failed to delete transaction: {e}")


if __name__ == "__main__":
    app()
