"""
CEREBRUM
Puente entre el núcleo cognitivo y el LLM.

v0.0.7 Alpha - Cognitive Interaction
"""

from .cognitive_engine import CognitiveEngine
from .llm import LLMResponse
from .llm_service import LLMService


class CognitiveLLMBridge:
    """Conecta el contexto cognitivo con el servicio LLM."""

    def __init__(
        self,
        cognitive_engine: CognitiveEngine,
        llm_service: LLMService
    ):
        self.cognitive_engine = cognitive_engine
        self.llm_service = llm_service

    def generar(
        self,
        mensaje: str
    ) -> LLMResponse:
        """Genera una respuesta usando contexto cognitivo."""

        resultado = self.cognitive_engine.procesar(
            mensaje
        )

        conocimiento = [
            f"{hecho.sujeto} "
            f"{hecho.relacion} "
            f"{hecho.objeto}"
            for hecho in resultado.hechos_aprendidos
        ]

        razonamiento = [
            f"{inferencia.conclusion.sujeto} "
            f"{inferencia.conclusion.relacion} "
            f"{inferencia.conclusion.objeto}"
            for inferencia in resultado.inferencias
        ]

        memoria = list(
            resultado.evidencia
        )

        return self.llm_service.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            intencion=resultado.intencion
        )

    def generar_texto(
        self,
        mensaje: str
    ) -> str:
        """Genera únicamente el texto de la respuesta."""

        return self.llm_service.response_formatter.formatear(
            self.generar(
                mensaje
            )
        )