"""
CEREBRUM
Explicación y procedencia del conocimiento.

v0.0.5 Alpha - Cognitive Core
"""

from dataclasses import dataclass

from .knowledge import KnowledgeFact


@dataclass
class InferenceExplanation:
    """Representa una conclusión junto con su procedencia."""

    conclusion: KnowledgeFact
    evidencias: list[KnowledgeFact]
    regla: str
    tipo: str = "inferido"

    @property
    def es_inferencia(self) -> bool:
        """Indica si la conclusión fue obtenida por inferencia."""

        return self.tipo == "inferido"

    @property
    def es_aprendizaje(self) -> bool:
        """Indica si representa conocimiento aprendido directamente."""

        return self.tipo == "aprendido"


class InferenceExplanationBuilder:
    """Construye explicaciones y registra su procedencia."""

    def explicar_transitiva(
        self,
        primero: KnowledgeFact,
        segundo: KnowledgeFact,
        conclusion: KnowledgeFact
    ) -> InferenceExplanation:
        """
        Explica una inferencia transitiva:

        A es B
        B es C
        -------
        A es C
        """

        return InferenceExplanation(
            conclusion=conclusion,
            evidencias=[primero, segundo],
            regla="inferencia_transitiva",
            tipo="inferido"
        )

    def explicar_aprendizaje(
        self,
        hecho: KnowledgeFact
    ) -> InferenceExplanation:
        """Registra un hecho aprendido directamente."""

        return InferenceExplanation(
            conclusion=hecho,
            evidencias=[],
            regla="aprendizaje_directo",
            tipo="aprendido"
        )

    def formatear(
        self,
        explicacion: InferenceExplanation
    ) -> str:
        """Convierte la explicación en texto legible."""

        conclusion = explicacion.conclusion

        resultado = [
            (
                f"Conclusión: "
                f"{conclusion.sujeto} "
                f"{conclusion.relacion} "
                f"{conclusion.objeto}"
            ),
            f"Tipo: {explicacion.tipo}",
            f"Regla aplicada: {explicacion.regla}"
        ]

        if explicacion.evidencias:
            resultado.append("Evidencias:")

            for evidencia in explicacion.evidencias:
                resultado.append(
                    f"- {evidencia.sujeto} "
                    f"{evidencia.relacion} "
                    f"{evidencia.objeto}"
                )

        return "\n".join(resultado)