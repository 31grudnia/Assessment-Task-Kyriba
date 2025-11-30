import typer
from rich.console import Console

from librarian.src import crud
from librarian.database.database import get_db
from docsli.src.generator import generate_fixed_width_content

app = typer.Typer(help="Librarian File Management CLI")
console = Console()


@app.command("list-files")
def list_files():
    db = next(get_db())
    files = crud.get_all_files(db)

    if not files:
        console.print("[yellow]No files found in database.[/yellow]")
        return

    for file_obj in files:
        generate_fixed_width_content(file_obj)


@app.command("hello")
def cli_hello():
    print("Hello niga ")

if __name__ == "__main__":
    app()
