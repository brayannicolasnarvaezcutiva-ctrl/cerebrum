"""
core/app.py

Núcleo principal de CEREBRUM.
"""

from rich.console import Console
from commands.manager import CommandManager
from core.startup import (
    banner,
    startup_animation,
    system_info,
    welcome,
)

console = Console()


class App:
    """Clase principal de la aplicación."""

    def run(self):
        console.clear()

        banner()
        startup_animation()
        system_info()
        welcome()

        manager = CommandManager()
        manager.start()
