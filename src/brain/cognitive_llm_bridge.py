"""
CEREBRUM
Puente entre el núcleo cognitivo y el LLM.

v0.0.6 Alpha - LLM Core
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
        """
        Procesa el mensaje cognitivamente y utiliza
        el resultado para generar una respuesta LLM.
        """

        resultado = self.cognitive_engine.procesar(
            mensaje
        )

        memoria = list(resultado.evidencia)
        conocimiento = []

        for hecho in resultado.hechos_aprendidos:
            conocimiento.append(
                f"{hecho.sujeto} "
                f"{hecho.relacion} "
                f"{hecho.objeto}"
            )

        razonamiento = []

        for inferencia in resultado.inferencias:
            conclusion = inferencia.conclusion

            razonamiento.append(
                f"{conclusion.sujeto} "
                f"{conclusion.relacion} "
                f"{conclusion.objeto}"
            )

        return self.llm_service.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento
        )

    def generar_texto(
        self,
        mensaje: str
    ) -> str:
        """Genera únicamente el texto de la respuesta."""

        resultado = self.generar(
            mensaje
        )

        return self.llm_service.response_formatter.formatear(
            resultado
        )