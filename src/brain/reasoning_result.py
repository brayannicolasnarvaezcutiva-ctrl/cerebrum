"""
CEREBRUM
Resultado canónico del razonamiento.

v0.0.9 Alpha — preparación hacia v0.1.0
"""

from dataclasses import dataclass, field

from .inference_explanation import InferenceExplanation


@dataclass(init=False)
class ReasoningResult:
    """
    Representa el resultado de una operación de razonamiento.

    ``conclusion`` y ``evidencia`` conservan el contrato textual del
    ReasoningEngine clásico. ``conclusiones`` contiene las conclusiones
    estructuradas producidas por el núcleo cognitivo. Ambos formatos viven
    en el mismo resultado para que los consumidores migren sin dos DTOs
    incompatibles.
    """

    conclusion: str = ""

    evidencia: list[str] = field(
        default_factory=list
    )

    confianza: float = 0.0

    conclusiones: list[InferenceExplanation] = field(
        default_factory=list
    )

    valido: bool = False

    tiene_conflicto: bool = False

    conflictos: list = field(
        default_factory=list
    )

    def __init__(
        self,
        *args,
        conclusion: str = "",
        evidencia: list[str] | None = None,
        confianza: float = 0.0,
        conclusiones: list[InferenceExplanation] | None = None,
        valido: bool = False,
        tiene_conflicto: bool = False,
        conflictos: list | None = None
    ):
        """Acepta las firmas posicionales histórica y estructurada.

        La ruta clásica usaba ``(conclusion, evidencia, confianza)`` y la
        estructurada ``(conclusiones, confianza, valido, tiene_conflicto,
        conflictos)``. La compatibilidad se mantiene mientras los nuevos
        consumidores usan argumentos con nombre.
        """

        if args:
            if isinstance(args[0], list):
                valores = list(args) + [None] * (5 - len(args))
                conclusiones = valores[0]
                confianza = (
                    valores[1]
                    if valores[1] is not None
                    else confianza
                )
                valido = (
                    valores[2]
                    if valores[2] is not None
                    else valido
                )
                tiene_conflicto = (
                    valores[3]
                    if valores[3] is not None
                    else tiene_conflicto
                )
                conflictos = (
                    valores[4]
                    if valores[4] is not None
                    else conflictos
                )
            else:
                valores = list(args) + [None] * (3 - len(args))
                conclusion = valores[0]
                evidencia = (
                    valores[1]
                    if valores[1] is not None
                    else evidencia
                )
                confianza = (
                    valores[2]
                    if valores[2] is not None
                    else confianza
                )

        self.conclusion = conclusion
        self.evidencia = evidencia or []
        self.confianza = confianza
        self.conclusiones = conclusiones or []
        self.valido = bool(valido)
        self.tiene_conflicto = bool(tiene_conflicto)
        self.conflictos = conflictos or []
        self.__post_init__()

    def __post_init__(self):
        """Normaliza los campos compartidos por ambas rutas."""

        self.conclusion = (
            self.conclusion.strip()
            if isinstance(self.conclusion, str)
            else ""
        )
        self.evidencia = (
            list(self.evidencia)
            if isinstance(self.evidencia, list)
            else []
        )
        self.conclusiones = (
            list(self.conclusiones)
            if isinstance(self.conclusiones, list)
            else []
        )
        self.conflictos = (
            list(self.conflictos)
            if isinstance(self.conflictos, list)
            else []
        )

        try:
            self.confianza = float(self.confianza)
        except (TypeError, ValueError):
            self.confianza = 0.0

        self.confianza = max(0.0, min(1.0, self.confianza))

    @property
    def tuvo_resultados(self) -> bool:
        """Indica si existe una conclusión textual o estructurada."""

        return bool(
            self.conclusiones
            or self.conclusion
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
