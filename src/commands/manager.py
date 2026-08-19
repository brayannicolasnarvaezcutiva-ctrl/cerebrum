"""
commands/manager.py

Administrador de comandos de CEREBRUM.
"""

from rich.console import Console

from commands.help import execute as help_execute
from commands.version import execute as version_execute
from commands.status import execute as status_execute
from commands.clear import execute as clear_execute

from brain.engine import BrainEngine


console = Console()


class CommandManager:
    """Administrador principal de comandos."""

    def __init__(self):
        self.commands = {}
        self.engine = BrainEngine()

        self.register(
            "help",
            lambda: help_execute(self.commands)
        )
        self.register("version", version_execute)
        self.register("status", status_execute)
        self.register("clear", clear_execute)

    def register(self, name: str, callback):
        """Registra un comando."""
        self.commands[name] = callback

    def start(self):
        """Inicia el bucle de comandos."""

        while True:
            command = input("CEREBRUM > ").strip().lower()

            if not command:
                continue

            if command == "exit":
                console.print(
                    "[bold yellow]Apagando CEREBRUM...[/bold yellow]"
                )
                break

            if command in self.commands:
                self.commands[command]()
                continue

            response = self.engine.process(command)
            console.print(response)