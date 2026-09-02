"""
CEREBRUM
Puente entre conocimiento estructurado y razonamiento.

v0.0.5 Alpha - Cognitive Core
"""

from .knowledge import KnowledgeBase, KnowledgeFact


class KnowledgeReasoner:
    """Consulta la base de conocimiento y genera evidencia."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def consultar(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> list[KnowledgeFact]:
        """Devuelve hechos que coinciden con la consulta."""

        return self.knowledge_base.buscar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

    def generar_evidencia(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> list[str]:
        """
        Convierte hechos estructurados en frases de evidencia
        utilizables por otros componentes cognitivos.
        """

        hechos = self.consultar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

        evidencia = []

        for fact in hechos:
            evidencia.append(
                f"{fact.sujeto} {fact.relacion} {fact.objeto}"
            )

        return evidencia

    def conoce(
        self,
        sujeto: str,
        relacion: str,
        objeto: str
    ) -> bool:
        """Indica si la base de conocimiento contiene un hecho."""

        return self.knowledge_base.existe(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )