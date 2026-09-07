"""
CEREBRUM
Fachada de alto nivel para Cognitive Core + LLM Core.

v0.0.7 Alpha - Cognitive Interaction
"""

from .cognitive_context_retriever import CognitiveContextRetriever
from .cognitive_context_selector import CognitiveContextSelector
from .cognitive_engine import CognitiveEngine
from .cognitive_strategy_router import CognitiveStrategyRouter
from .llm import LLMResponse
from .llm_manager import LLMManager


class CerebrumLLM:
    """
    Punto de entrada de alto nivel para interacción con CEREBRUM.
    """

    def __init__(
        self,
        cognitive_engine: CognitiveEngine | None = None,
        llm_manager: LLMManager | None = None,
        context_selector: CognitiveContextSelector | None = None,
        context_retriever: CognitiveContextRetriever | None = None,
        strategy_router: CognitiveStrategyRouter | None = None
    ):
        self.cognitive_engine = (
            cognitive_engine
            or CognitiveEngine()
        )

        self.llm_manager = (
            llm_manager
            or LLMManager.desde_entorno()
        )

        self.context_selector = (
            context_selector
            or CognitiveContextSelector()
        )

        self.context_retriever = (
            context_retriever
            or CognitiveContextRetriever(
                self.cognitive_engine,
                self.context_selector
            )
        )

        self.strategy_router = (
            strategy_router
            or CognitiveStrategyRouter()
        )

    def procesar(
        self,
        mensaje: str
    ) -> LLMResponse:
        """Ejecuta el flujo cognitivo completo."""

        resultado = self.cognitive_engine.procesar(
            mensaje
        )

        intencion = resultado.intencion

        conversacion = (
            self.llm_manager
            .obtener_sesion()
            .obtener_contexto()
        )

        contexto = self.context_retriever.recuperar(
            intencion,
            conversacion=conversacion
        )

        memoria = list(
            contexto.get(
                "memoria",
                []
            )
        )

        conocimiento = list(
            contexto.get(
                "conocimiento",
                []
            )
        )

        razonamiento = list(
            contexto.get(
                "razonamiento",
                []
            )
        )

        estrategia = self.strategy_router.enrutar(
            intencion
        )

        instrucciones = (
            self.strategy_router.instrucciones(
                estrategia
            )
        )

        razonamiento.insert(
            0,
            f"Estrategia de procesamiento: {estrategia}"
        )

        razonamiento.insert(
            1,
            f"Instrucciones: {instrucciones}"
        )

        return self.llm_manager.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            intencion=intencion
        )

    def detectar_intencion(
        self,
        mensaje: str
    ):
        """Expone la intención detectada."""

        return self.cognitive_engine.detectar_intencion(
            mensaje
        )

    def obtener_seleccion_contexto(
        self,
        mensaje: str
    ) -> dict[str, bool]:
        """Devuelve qué fuentes son relevantes."""

        intencion = self.cognitive_engine.detectar_intencion(
            mensaje
        )

        return self.context_selector.seleccionar(
            intencion
        )

    def obtener_contexto_recuperado(
        self,
        mensaje: str
    ) -> dict:
        """Devuelve el contexto recuperado."""

        intencion = self.cognitive_engine.detectar_intencion(
            mensaje
        )

        conversacion = (
            self.llm_manager
            .obtener_sesion()
            .obtener_contexto()
        )

        return self.context_retriever.recuperar(
            intencion,
            conversacion=conversacion
        )

    def obtener_estrategia(
        self,
        mensaje: str
    ) -> str:
        """Devuelve la estrategia seleccionada."""

        intencion = self.cognitive_engine.detectar_intencion(
            mensaje
        )

        return self.strategy_router.enrutar(
            intencion
        )

    def responder(
        self,
        mensaje: str
    ) -> str:
        """Procesa un mensaje y devuelve texto."""

        respuesta = self.procesar(
            mensaje
        )

        return respuesta.contenido

    def limpiar_conversacion(self):
        """Limpia la conversación del LLM."""

        self.llm_manager.limpiar_conversacion()