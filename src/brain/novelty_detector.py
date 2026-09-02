"""
CEREBRUM
Detector de conocimiento nuevo.

v0.0.5 Alpha - Cognitive Core
"""

from .knowledge import KnowledgeBase, KnowledgeFact


class NoveltyDetector:
    """Determina si un hecho aporta conocimiento nuevo."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def es_nuevo(
        self,
        hecho: KnowledgeFact
    ) -> bool:
        """Indica si el hecho todavía no existe en la base."""

        if hecho is None:
            return False

        return not self.knowledge_base.existe(
            sujeto=hecho.sujeto,
            relacion=hecho.relacion,
            objeto=hecho.objeto
        )

    def filtrar_nuevos(
        self,
        hechos: list[KnowledgeFact]
    ) -> list[KnowledgeFact]:
        """Devuelve únicamente hechos que no estén almacenados."""

        nuevos = []

        for hecho in hechos:
            if self.es_nuevo(hecho):
                nuevos.append(hecho)

        return nuevos