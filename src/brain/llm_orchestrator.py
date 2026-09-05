"""
CEREBRUM
Orquestador entre el núcleo cognitivo y el LLM.

v0.0.6 Alpha - LLM Core
"""

from .cognitive_engine import CognitiveEngine
from .llm import LLMResponse
from .llm_manager import LLMManager
from .llm_service import LLMService


class LLMOrchestrator:
    """
    Coordina una solicitud completa entre Cognitive Core y LLM Core.

    Acepta tanto LLMManager como LLMService para mantener
    compatibilidad con versiones anteriores.
    """

    def __init__(
        self,
        cognitive_engine: CognitiveEngine,
        llm_manager: LLMManager | None = None,
        llm_service: LLMService | None = None
    ):
        self.cognitive_engine = cognitive_engine

        if llm_manager is not None and llm_service is not None:
            raise ValueError(
                "No se puede proporcionar llm_manager y llm_service "
                "al mismo tiempo."
            )

        if llm_manager is not None:
            self.llm_manager = llm_manager
            self.llm_service = llm_manager.service

        elif llm_service is not None:
            self.llm_service = llm_service
            self.llm_manager = None

        else:
            raise ValueError(
                "Debe proporcionarse llm_manager o llm_service."
            )

    @classmethod
    def desde_entorno(
        cls,
        cognitive_engine: CognitiveEngine | None = None
    ) -> "LLMOrchestrator":
        """Construye el orquestador usando configuración del entorno."""

        return cls(
            cognitive_engine=cognitive_engine or CognitiveEngine(),
            llm_manager=LLMManager.desde_entorno()
        )

    def procesar(
        self,
        mensaje: str
    ) -> LLMResponse:
        """Procesa el mensaje mediante Cognitive Core y LLM Core."""

        resultado = self.cognitive_engine.procesar(
            mensaje
        )

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

        memoria = list(
            resultado.evidencia
        )

        if self.llm_manager is not None:
            return self.llm_manager.generar(
                mensaje=mensaje,
                memoria=memoria,
                conocimiento=conocimiento,
                razonamiento=razonamiento
            )

        return self.llm_service.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento
        )

    def procesar_texto(
        self,
        mensaje: str
    ) -> str:
        """Procesa un mensaje y devuelve únicamente el texto."""

        respuesta = self.procesar(
            mensaje
        )

        return respuesta.contenido