"""
CEREBRUM
Validador de conclusiones y resultados de razonamiento.

v0.0.9 Alpha - Reasoning Upgrade
"""

from .confidence_aggregator import ConfidenceAggregator
from .knowledge import KnowledgeFact


class ReasoningValidator:
    """
    Valida conclusiones de conocimiento y resultados
    producidos por el ReasoningEngine.
    """

    def __init__(
        self,
        aggregator: ConfidenceAggregator | None = None
    ):
        self.aggregator = (
            aggregator
            or ConfidenceAggregator()
        )

    def validar(
        self,
        conclusion: KnowledgeFact,
        evidencias: list[KnowledgeFact] | None = None
    ) -> dict:
        """
        Valida una conclusión estructurada.
        """

        if not isinstance(
            conclusion,
            KnowledgeFact
        ):
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "invalida"
            }

        evidencias = (
            evidencias
            if isinstance(
                evidencias,
                list
            )
            else []
        )

        evidencias_validas = [
            evidencia
            for evidencia in evidencias
            if isinstance(
                evidencia,
                KnowledgeFact
            )
        ]

        if not evidencias_validas:
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "sin_evidencia"
            }

        confianza = self.aggregator.desde_recuerdos(
            conclusion,
            evidencias_validas
        )

        if confianza <= 0.0:
            return {
                "valida": False,
                "confianza": confianza,
                "tipo": "baja_confianza"
            }

        return {
            "valida": True,
            "confianza": confianza,
            "tipo": "respaldada"
        }

    def validar_resultado(
        self,
        resultado
    ) -> dict:
        """
        Valida un ReasoningResult del ReasoningEngine.
        """

        if resultado is None:
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "sin_resultado"
            }

        if not hasattr(
            resultado,
            "conclusion"
        ):
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "sin_conclusion"
            }

        if not hasattr(
            resultado,
            "evidencia"
        ):
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "sin_evidencia"
            }

        if not hasattr(
            resultado,
            "confianza"
        ):
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "sin_confianza"
            }

        conclusion = resultado.conclusion
        evidencia = resultado.evidencia

        try:
            confianza = float(
                resultado.confianza
            )
        except (
            TypeError,
            ValueError
        ):
            confianza = 0.0

        confianza = max(
            0.0,
            min(
                1.0,
                confianza
            )
        )

        if not isinstance(
            conclusion,
            str
        ) or not conclusion.strip():
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "conclusion_vacia"
            }

        if not isinstance(
            evidencia,
            list
        ):
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "evidencia_invalida"
            }

        if not evidencia:
            return {
                "valida": False,
                "confianza": confianza,
                "tipo": "sin_evidencia"
            }

        if confianza <= 0.0:
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "baja_confianza"
            }

        return {
            "valida": True,
            "confianza": confianza,
            "tipo": "resultado_valido"
        }