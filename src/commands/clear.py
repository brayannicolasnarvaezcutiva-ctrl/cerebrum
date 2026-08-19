"""
commands/clear.py

Comando clear.
"""

from rich.console import Console

console = Console()


def execute():
    """Limpia la consola."""

    console.clear()