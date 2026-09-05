"""
CEREBRUM
Fachada de alto nivel para Cognitive Core + LLM Core.

v0.0.6 Alpha - LLM Core
"""

from .cognitive_engine import CognitiveEngine
from .llm import LLMResponse
from .llm_manager import LLMManager


class CerebrumLLM:
    """Punto de entrada de alto nivel para interacción con CEREBRUM."""

    def __init__(
        self,
        cognitive_engine: CognitiveEngine | None = None,
        llm_manager: LLMManager | None = None
    ):
        self.cognitive_engine = (
            cognitive_engine
            or CognitiveEngine()
        )

        self.llm_manager = (
            llm_manager
            or LLMManager.desde_entorno()
        )

    def procesar(
        self,
        mensaje: str
    ) -> LLMResponse:
        """Procesa un mensaje usando cognición + LLM."""

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

        return self.llm_manager.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento
        )

    def responder(
        self,
        mensaje: str
    ) -> str:
        """Procesa un mensaje y devuelve texto limpio."""

        respuesta = self.procesar(
            mensaje
        )

        return respuesta.contenido

    def limpiar_conversacion(self):
        """Limpia la conversación del LLM."""

        self.llm_manager.limpiar_conversacion()