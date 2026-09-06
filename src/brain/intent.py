"""
CEREBRUM
Representación estructurada de intención.

v0.0.7 Alpha - Cognitive Interaction
"""

from dataclasses import dataclass


@dataclass
class Intent:
    """Representa la intención detectada en una entrada."""

    tipo: str
    accion: str
    tema: str = ""
    prioridad: str = "normal"
    confianza: float = 0.0

    def __post_init__(self):
        """Normaliza los valores de la intención."""

        self.tipo = self.tipo.strip().lower()
        self.accion = self.accion.strip().lower()
        self.tema = self.tema.strip()
        self.prioridad = self.prioridad.strip().lower()

        self.confianza = max(
            0.0,
            min(1.0, float(self.confianza))
        )

    def es_pregunta(self) -> bool:
        """Indica si la intención corresponde a una pregunta."""

        return self.tipo == "pregunta"

    def requiere_accion(self) -> bool:
        """Indica si la intención requiere realizar una acción."""

        return self.accion not in {
            "",
            "ninguna"
        }