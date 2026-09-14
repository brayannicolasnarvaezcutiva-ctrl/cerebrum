"""
CEREBRUM
Resultado estructurado del razonamiento.

v0.0.9 Alpha - Reasoning Upgrade
"""

from dataclasses import dataclass, field

from .inference_explanation import InferenceExplanation


@dataclass
class ReasoningResult:
    """
    Representa el resultado de una operación de razonamiento.
    """

    conclusiones: list[InferenceExplanation] = field(
        default_factory=list
    )

    confianza: float = 0.0

    valido: bool = False

    tiene_conflicto: bool = False

    conflictos: list = field(
        default_factory=list
    )

    @property
    def tuvo_resultados(self) -> bool:
        """Indica si existen conclusiones."""

        return bool(
            self.conclusiones
        )

    @property
    def cantidad_conclusiones(self) -> int:
        """Devuelve la cantidad de conclusiones."""

        return len(
            self.conclusiones
        )

    @property
    def cantidad_conflictos(self) -> int:
        """Devuelve la cantidad de conflictos."""

        return len(
            self.conflictos
        )

    def resumen(self) -> str:
        """Genera un resumen legible."""

        partes = [
            f"Conclusiones: {self.cantidad_conclusiones}",
            f"Confianza: {self.confianza:.2f}",
            f"Válido: {self.valido}",
            f"Conflictos: {self.cantidad_conflictos}",
        ]

        return "\n".join(
            partes
        )