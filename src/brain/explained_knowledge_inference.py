"""
CEREBRUM
Inferencia de conocimiento con explicación.

v0.0.5 Alpha - Cognitive Core
"""

from .knowledge import KnowledgeBase, KnowledgeFact
from .knowledge_inference import KnowledgeInference
from .inference_explanation import (
    InferenceExplanation,
    InferenceExplanationBuilder,
)


class ExplainedKnowledgeInference:
    """Ejecuta inferencias y conserva su justificación."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.inference = KnowledgeInference(knowledge_base)
        self.explainer = InferenceExplanationBuilder()

    def inferir_es(
        self
    ) -> list[InferenceExplanation]:
        """
        Busca cadenas A es B, B es C y genera A es C
        junto con la explicación correspondiente.
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

                explicacion = self.explainer.explicar_transitiva(
                    primero=primero,
                    segundo=segundo,
                    conclusion=conclusion
                )

                if not any(
                    existente.conclusion == conclusion
                    and existente.evidencias == explicacion.evidencias
                    for existente in explicaciones
                ):
                    explicaciones.append(explicacion)

        return explicaciones

    def inferir_todo(
        self
    ) -> list[InferenceExplanation]:
        """Ejecuta todas las inferencias disponibles."""

        return self.inferir_es()

    def formatear_resultados(
        self,
        explicaciones: list[InferenceExplanation]
    ) -> list[str]:
        """Convierte las explicaciones a texto legible."""

        return [
            self.explainer.formatear(explicacion)
            for explicacion in explicaciones
        ]