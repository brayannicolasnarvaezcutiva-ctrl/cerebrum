"""
CEREBRUM
Integración entre memoria y núcleo cognitivo.

v0.0.5 Alpha - Cognitive Core
"""

from .knowledge import KnowledgeFact
from .memory_knowledge_bridge import MemoryKnowledgeBridge


class CognitiveMemory:
    """Coordina la incorporación de recuerdos al conocimiento."""

    def __init__(self, memory_service, cognitive_engine):
        self.memory_service = memory_service
        self.cognitive_engine = cognitive_engine

        self.bridge = MemoryKnowledgeBridge(
            memory_service=memory_service,
            knowledge_base=cognitive_engine.knowledge_base
        )

    def aprender_desde_memoria(
        self,
        consulta: str
    ) -> list[KnowledgeFact]:
        """Recupera recuerdos y los incorpora al conocimiento."""

        hechos = self.bridge.aprender_desde_memoria(
            consulta
        )

        return hechos

    def aprender_recuerdo(
        self,
        texto: str
    ) -> KnowledgeFact | None:
        """Convierte directamente un recuerdo en conocimiento."""

        return self.cognitive_engine.aprender(texto)

    def consultar(
        self,
        sujeto=None,
        relacion=None,
        objeto=None
    ) -> list[KnowledgeFact]:
        """Consulta el conocimiento acumulado."""

        return self.cognitive_engine.consultar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )