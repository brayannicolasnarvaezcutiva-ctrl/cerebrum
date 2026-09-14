"""
CEREBRUM
Inferencia de conocimiento con explicación y validación.

v0.0.9 Alpha - Reasoning Upgrade
"""

from .knowledge import KnowledgeBase
from .inference_explanation import (
    InferenceExplanation,
    InferenceExplanationBuilder,
)
from .knowledge_inference import KnowledgeInference
from .reasoning_validator import ReasoningValidator


class ExplainedKnowledgeInference:
    """Ejecuta inferencias, conserva su justificación y las valida."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        validator: ReasoningValidator | None = None
    ):
        self.knowledge_base = knowledge_base

        self.inference = KnowledgeInference(
            knowledge_base
        )

        self.explainer = InferenceExplanationBuilder()

        self.validator = (
            validator
            or ReasoningValidator()
        )

    def inferir_es(
        self
    ) -> list[InferenceExplanation]:
        """
        Busca cadenas A es B, B es C y genera
        A es C junto con su explicación.
        """

        hechos = self.knowledge_base.obtener_todo()

        explicaciones = []

        for primero in hechos:
            if primero.relacion != "es":
                continue

            for segundo in hechos:
                if segundo.relacion != "es":
                    continue

                if primero.objeto != segundo.sujeto:
                    continue

                if primero.sujeto == segundo.objeto:
                    continue

                conclusion = self.knowledge_base.agregar(
                    sujeto=primero.sujeto,
                    relacion="es",
                    objeto=segundo.objeto,
                    confianza=min(
                        primero.confianza,
                        segundo.confianza
                    )
                )

                if conclusion is None:
                    continue

                explicacion = (
                    self.explainer.explicar_transitiva(
                        primero=primero,
                        segundo=segundo,
                        conclusion=conclusion
                    )
                )

                validacion = self.validator.validar(
                    conclusion=conclusion,
                    evidencias=[
                        primero,
                        segundo
                    ]
                )

                if not validacion["valida"]:
                    continue

                if not any(
                    existente.conclusion == conclusion
                    and existente.evidencias
                    == explicacion.evidencias
                    for existente in explicaciones
                ):
                    explicaciones.append(
                        explicacion
                    )

        return explicaciones

    def inferir_todo(
        self
    ) -> list[InferenceExplanation]:
        """Ejecuta todas las inferencias disponibles."""

        return self.inferir_es()

    def validar_inferencia(
        self,
        explicacion: InferenceExplanation
    ) -> dict:
        """
        Valida una explicación de inferencia existente.
        """

        if not isinstance(
            explicacion,
            InferenceExplanation
        ):
            return {
                "valida": False,
                "confianza": 0.0,
                "tipo": "invalida"
            }

        return self.validator.validar(
            conclusion=explicacion.conclusion,
            evidencias=explicacion.evidencias
        )

    def formatear_resultados(
        self,
        explicaciones: list[InferenceExplanation]
    ) -> list[str]:
        """Convierte las explicaciones a texto legible."""

        return [
            self.explainer.formatear(
                explicacion
            )
            for explicacion in explicaciones
        ]