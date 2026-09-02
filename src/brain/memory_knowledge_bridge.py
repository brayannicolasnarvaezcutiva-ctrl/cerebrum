"""
CEREBRUM
Puente entre memoria y conocimiento estructurado.

v0.0.5 Alpha - Cognitive Core
"""

from .knowledge import KnowledgeBase, KnowledgeFact
from .knowledge_extractor import KnowledgeExtractor


class MemoryKnowledgeBridge:
    """Convierte recuerdos recuperados en conocimiento estructurado."""

    def __init__(
        self,
        memory_service,
        knowledge_base: KnowledgeBase
    ):
        self.memory_service = memory_service
        self.knowledge_base = knowledge_base
        self.extractor = KnowledgeExtractor(knowledge_base)

    def recuperar(
        self,
        consulta: str
    ) -> list[str]:
        """
        Recupera recuerdos relevantes mediante MemoryService.

        MemoryService ya dispone de la operación
        obtener_recuerdos_para_texto().
        """

        if not isinstance(consulta, str):
            return []

        consulta = consulta.strip()

        if not consulta:
            return []

        recuerdos = self.memory_service.obtener_recuerdos_para_texto(
            consulta
        )

        if recuerdos is None:
            return []

        if isinstance(recuerdos, str):
            return [recuerdos]

        return list(recuerdos)

    def aprender_desde_memoria(
        self,
        consulta: str
    ) -> list[KnowledgeFact]:
        """
        Recupera recuerdos y trata de convertirlos
        en hechos estructurados.
        """

        recuerdos = self.recuperar(consulta)

        hechos = []

        for recuerdo in recuerdos:
            fact = self.extractor.extraer(recuerdo)

            if fact is not None and fact not in hechos:
                hechos.append(fact)

        return hechos

    def consultar_conocimiento(
        self,
        sujeto=None,
        relacion=None,
        objeto=None
    ) -> list[KnowledgeFact]:
        """Consulta directamente el conocimiento generado."""

        return self.knowledge_base.buscar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )