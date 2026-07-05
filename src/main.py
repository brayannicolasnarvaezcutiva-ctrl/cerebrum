from datetime import datetime
import platform
import time

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

# ============================================================
# CEREBRUM
# Archivo principal
# Versión: 0.0.1 Alpha - "The Spark"
# ============================================================

console = Console()

AI_NAME = "CEREBRUM"
VERSION = "0.0.1 Alpha"


def banner():
    """Muestra el logo principal."""

    logo = Text(
        r"""
 ██████╗███████╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗
██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║
██║     █████╗  ██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║
██║     ██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║
╚██████╗███████╗██║  ██║███████╗██████╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝
""",
        style="bold cyan",
    )

    console.print(Align.center(logo))
    console.rule("[bold bright_cyan]CEREBRUM AI CORE[/bold bright_cyan]")


def startup_animation():
    """Animación de carga inicial."""

    modules = [
        "Core Engine",
        "Memory",
        "Learning",
        "System",
        "Plugins",
        "Interface",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        for module in modules:
            task = progress.add_task(f"Cargando {module}...", total=None)
            time.sleep(0.45)
            progress.remove_task(task)


def system_info():
    """Muestra información del sistema."""

    table = Table(title="Estado del Sistema")

    table.add_column("Parámetro", style="cyan", no_wrap=True)
    table.add_column("Valor", style="green")

    table.add_row("IA", AI_NAME)
    table.add_row("Versión", VERSION)
    table.add_row("Estado", "🟢 Operativo")
    table.add_row("Fecha", datetime.now().strftime("%d/%m/%Y"))
    table.add_row("Hora", datetime.now().strftime("%H:%M:%S"))
    table.add_row("Sistema", platform.system())
    table.add_row("Release", platform.release())
    table.add_row("Arquitectura", platform.machine())
    table.add_row("Python", platform.python_version())

    console.print(table)


def welcome():
    """Mensaje de bienvenida."""

    console.print()

    console.print(
        Panel.fit(
            "[bold green]Sistema iniciado correctamente[/bold green]\n\n"
            "Bienvenido al núcleo de CEREBRUM.\n"
            "Esperando instrucciones...",
            title="Inicio",
            border_style="green",
        )
    )


def shutdown():
    """Mensaje de cierre."""

    console.print()
    console.rule("[bold red]Cierre[/bold red]")
    console.print("CEREBRUM finalizado correctamente.", style="bold red")


def main():
    """Función principal."""

    console.clear()

    banner()
    startup_animation()
    system_info()
    welcome()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Interrupción detectada.[/bold yellow]")
        shutdown()

    except Exception as error:
        console.print(
            f"\n[bold red]Error inesperado:[/bold red] {error}"
        )