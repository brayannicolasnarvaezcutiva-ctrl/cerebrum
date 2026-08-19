"""
commands/version.py

Comando version.
"""

from rich.console import Console

console = Console()


def execute():
    """Muestra la versión de CEREBRUM."""

    console.print("[green]CEREBRUM[/green]")
    console.print("Versión: 0.0.2 Alpha")