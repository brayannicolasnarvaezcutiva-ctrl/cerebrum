"""
CEREBRUM
Resultado unificado del procesamiento cognitivo.

v0.0.5 Alpha - Cognitive Core
"""

from dataclasses import dataclass, field

from .inference_explanation import InferenceExplanation
from .knowledge import KnowledgeFact


@dataclass
class CognitiveResult:
    """Representa el resultado completo de una operación cognitiva."""

    entrada: str
    hechos_aprendidos: list[KnowledgeFact] = field(default_factory=list)
    inferencias: list[InferenceExplanation] = field(default_factory=list)
    evidencia: list[str] = field(default_factory=list)
    confianza: float = 0.0

    @property
    def tuvo_aprendizaje(self) -> bool:
        """Indica si se aprendió conocimiento directamente."""

        return bool(self.hechos_aprendidos)

    @property
    def tuvo_inferencias(self) -> bool:
        """Indica si se generaron inferencias nuevas."""

        return bool(self.inferencias)

    @property
    def conocimientos_nuevos(self) -> list[KnowledgeFact]:
        """Devuelve todo conocimiento nuevo obtenido."""

        resultado = list(self.hechos_aprendidos)

        for explicacion in self.inferencias:
            resultado.append(
                explicacion.conclusion
            )

        return resultado

    @property
    def aprendizajes_directos(self) -> list[KnowledgeFact]:
        """Devuelve únicamente los hechos aprendidos directamente."""

        return list(self.hechos_aprendidos)

    @property
    def conocimientos_inferidos(self) -> list[KnowledgeFact]:
        """Devuelve únicamente las conclusiones inferidas."""

        return [
            explicacion.conclusion
            for explicacion in self.inferencias
        ]

    def resumen(self) -> str:
        """Genera un resumen legible del resultado."""

        partes = [
            f"Entrada: {self.entrada}",
            f"Aprendizajes directos: {len(self.hechos_aprendidos)}",
            f"Conocimientos inferidos: {len(self.inferencias)}",
            f"Conocimientos nuevos: {len(self.conocimientos_nuevos)}",
            f"Confianza: {self.confianza:.2f}",
        ]

        if self.evidencia:
            partes.append(
                "Evidencia: " + "; ".join(self.evidencia)
            )

        return "\n".join(partes)