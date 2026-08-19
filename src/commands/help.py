"""
commands/help.py

Comando help.
"""

from rich.console import Console

console = Console()


def execute(commands):
    """Muestra los comandos disponibles."""

    console.print("[bold cyan]Comandos disponibles:[/bold cyan]")

    for command in commands:
        console.print(f" • {command}")

    console.print(" • exit")