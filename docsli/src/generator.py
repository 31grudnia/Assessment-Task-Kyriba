from librarian.database.models.file import HeaderModel

from rich.console import Console

console = Console()


def _format_text(value: str, length: int) -> str:
    val = str(value) if value else ""
    return val[:length].ljust(length)

def _format_number(value: int, length: int) -> str:
    return str(value).zfill(length)

def generate_fixed_width_content(header: HeaderModel):
    console.print(
        f"[bold red]01[/]"
        f"[green]{_format_text(header.name, 28)}[/]"
        f"[green]{_format_text(header.surname, 30)}[/]"
        f"[green]{_format_text(header.patronymic, 30)}[/]"
        f"[white]{_format_text(header.address, 30)}[/]"
    )

    for tx in header.transactions:
        console.print(
            f"[bold red]02[/]"
            f"[cyan]{_format_number(tx.counter, 6)}[/]"
            f"[magenta]{_format_number(tx.amount, 12)}[/]"
            f"[yellow]{_format_text(tx.currency.value, 3)}[/]"
            f"[dim]{_format_text('', 97)}[/]"
        )

    console.print(
        f"[bold red]03[/]"
        f"[cyan]{_format_number(header.footer.total_counter, 6)}[/]"
        f"[magenta]{_format_number(header.footer.control_sum, 12)}[/]"
        f"[dim]{_format_text('', 100)}[/]"
    )
    
    console.print("-" * 120, style="dim")
