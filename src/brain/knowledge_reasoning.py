"""
CEREBRUM
Integración entre conocimiento estructurado y razonamiento.

v0.0.5 Alpha - Cognitive Core
"""

from .knowledge import KnowledgeBase
from .knowledge_reasoner import KnowledgeReasoner
from .reasoning import ReasoningEngine, ReasoningResult


class KnowledgeReasoning:
    """Integra conocimiento estructurado con el motor de razonamiento."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        reasoning_engine: ReasoningEngine | None = None
    ):
        self.knowledge_base = knowledge_base
        self.knowledge_reasoner = KnowledgeReasoner(knowledge_base)
        self.reasoning_engine = reasoning_engine or ReasoningEngine()

    def consultar(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> list:
        """Consulta hechos almacenados en la base de conocimiento."""

        return self.knowledge_reasoner.consultar(
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
        """Obtiene los hechos como texto de evidencia."""

        return self.knowledge_reasoner.generar_evidencia(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

    def razonar_sobre(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> ReasoningResult:
        """
        Obtiene conocimiento estructurado y lo entrega
        al motor de razonamiento existente.
        """

        evidencia = self.generar_evidencia(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

        if not evidencia:
            return ReasoningResult(
                conclusion="No hay conocimiento suficiente.",
                evidencia=[],
                confianza=0.0
            )

        texto = " ".join(evidencia)

        # La API real de ReasoningEngine v0.0.4 utiliza analizar().
        resultado = self.reasoning_engine.analizar(texto)

        return resultado