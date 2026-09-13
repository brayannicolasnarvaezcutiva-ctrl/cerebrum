"""
CEREBRUM
Fachada de alto nivel para Cognitive Core + LLM Core.

v0.0.8 Alpha - Memory Bridge
"""

from .cognitive_context_retriever import CognitiveContextRetriever
from .cognitive_context_selector import CognitiveContextSelector
from .cognitive_engine import CognitiveEngine
from .cognitive_strategy_router import CognitiveStrategyRouter
from .llm import LLMResponse
from .llm_manager import LLMManager
from .memory_bridge import MemoryBridge
from src.brain.intent import Intent


class CerebrumLLM:
    """
    Punto de entrada de alto nivel para interacción con CEREBRUM.

    Coordina:

        Cognitive Core
        Memory Bridge
        Context Retrieval
        Strategy Routing
        LLM Core
    """

    def __init__(
        self,
        cognitive_engine: CognitiveEngine | None = None,
        llm_manager: LLMManager | None = None,
        context_selector: CognitiveContextSelector | None = None,
        context_retriever: CognitiveContextRetriever | None = None,
        strategy_router: CognitiveStrategyRouter | None = None,
        memory_bridge: MemoryBridge | None = None
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

        self.memory_bridge = (
            memory_bridge
            or MemoryBridge()
        )

        self.context_retriever = (
            context_retriever
            or CognitiveContextRetriever(
                cognitive_engine=self.cognitive_engine,
                selector=self.context_selector,
                memory_bridge=self.memory_bridge
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
        """
        Procesa una entrada mediante el flujo cognitivo completo.

        La memoria persistente se guarda únicamente después
        de obtener una respuesta válida del LLM.
        """

        if not isinstance(
            mensaje,
            str
        ):
            raise TypeError(
                "mensaje debe ser un texto"
            )

        mensaje = mensaje.strip()

        if not mensaje:
            raise ValueError(
                "mensaje no puede estar vacío"
            )

        resultado = (
            self.cognitive_engine
            .procesar(
                mensaje
            )
        )

        intencion = resultado.intencion

        conversacion = (
            self.llm_manager
            .obtener_sesion()
            .obtener_contexto()
        )

        contexto = (
            self.context_retriever
            .recuperar(
                intencion,
                conversacion=conversacion
            )
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

        estrategia = (
            self.strategy_router
            .enrutar(
                intencion
            )
        )

        instrucciones = (
            self.strategy_router
            .instrucciones(
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

        respuesta = self.llm_manager.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            intencion=intencion
        )

        self._guardar_memoria_si_corresponde(
            mensaje
        )

        return respuesta

    def _guardar_memoria_si_corresponde(
        self,
        mensaje: str
    ):
        """
        Intenta conservar el mensaje como memoria persistente
        cuando MemoryPolicy lo considera importante.

        Los errores de almacenamiento no invalidan una respuesta
        LLM ya generada.
        """

        try:
            self.memory_bridge.guardar(
                mensaje
            )
        except (
            OSError,
            RuntimeError,
            TypeError,
            ValueError
        ):
            return None

        return None

    def guardar_memoria(
        self,
        contenido: str
    ):
        """Guarda memoria automáticamente según la política."""

        return self.memory_bridge.guardar(
            contenido
        )

    def guardar_memoria_manual(
        self,
        contenido: str
    ):
        """Guarda una memoria de forma explícita."""

        return self.memory_bridge.guardar_manual(
            contenido
        )

    def recordar(
        self,
        termino: str
    ):
        """Recupera un recuerdo concreto."""

        return self.memory_bridge.recordar(
            termino
        )

    def obtener_memorias_relevantes(
        self,
        texto: str
    ):
        """Recupera recuerdos relevantes."""

        return self.memory_bridge.recuperar_relevante(
            texto
        )

    def obtener_contexto_de_memoria(
        self,
        texto: str,
        limite: int = 10
    ):
        """Devuelve memoria lista para contexto."""

        return self.memory_bridge.contexto_para(
            texto,
            limite=limite
        )

    def detectar_intencion(
        self,
        mensaje: str
    ):
        """Detecta la intención de un mensaje."""

        return (
            self.cognitive_engine
            .detectar_intencion(
                mensaje
            )
        )

    def obtener_seleccion_contexto(
        self,
        valor
    ) -> dict[str, bool]:
        """Devuelve la selección de contexto."""

        intencion = self._obtener_intencion(
            valor
        )

        return (
            self.context_selector
            .seleccionar(
                intencion
            )
        )

    def obtener_contexto_recuperado(
        self,
        valor,
        conversacion: str = ""
    ) -> dict:
        """Devuelve el contexto recuperado."""

        intencion = self._obtener_intencion(
            valor
        )

        if (
            not conversacion
            and isinstance(
                valor,
                str
            )
        ):
            conversacion = (
                self.llm_manager
                .obtener_sesion()
                .obtener_contexto()
            )

        return (
            self.context_retriever
            .recuperar(
                intencion,
                conversacion=conversacion
            )
        )

    def obtener_estrategia(
        self,
        valor
    ) -> str:
        """Devuelve la estrategia seleccionada."""

        intencion = self._obtener_intencion(
            valor
        )

        return (
            self.strategy_router
            .enrutar(
                intencion
            )
        )

    def _obtener_intencion(
        self,
        valor
    ):
        """Convierte texto a Intent cuando es necesario."""

        if valor is None:
            return None

        if (
            hasattr(valor, "tipo")
            and hasattr(valor, "accion")
        ):
            return valor

        if isinstance(
            valor,
            str
        ):
            return (
                self.cognitive_engine
                .detectar_intencion(
                    valor
                )
            )

        return None

    def responder(
        self,
        mensaje: str
    ) -> str:
        """Procesa un mensaje y devuelve texto."""

        respuesta = self.procesar(
            mensaje
        )

        return respuesta.contenido

    def limpiar_memoria(self):
        """Elimina toda la memoria persistente."""

        return self.memory_bridge.limpiar()

    def limpiar_conversacion(self):
        """Limpia la conversación actual."""

        self.llm_manager.limpiar_conversacion()

    def limpiar_conversacion(self):
        """Limpia la conversación actual."""

        self.llm_manager.limpiar_conversacion()