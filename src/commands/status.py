"""
commands/status.py

Comando status.
"""

from rich.console import Console

console = Console()


def execute():
    """Muestra el estado del sistema."""

    console.print("[green]Estado:[/green] Operativo")