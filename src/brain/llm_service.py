"""
CEREBRUM
Servicio de alto nivel para interacción con el LLM.

v0.0.7 Alpha - Cognitive Interaction
"""

from .intent import Intent
from .llm import LLMRequest, LLMResponse
from .llm_config import LLMConfig
from .llm_context_builder import LLMContextBuilder
from .llm_engine import LLMEngine
from .llm_errors import LLMProviderError, LLMResponseError
from .llm_response_formatter import LLMResponseFormatter
from .llm_session import LLMSession
from .mock_llm import MockLLMProvider


class LLMService:
    """Proporciona una interfaz simple para trabajar con el LLM."""

    def __init__(
        self,
        engine: LLMEngine,
        context_builder: LLMContextBuilder | None = None,
        response_formatter: LLMResponseFormatter | None = None,
        session: LLMSession | None = None,
        fallback_enabled: bool = False
    ):
        self.engine = engine

        self.context_builder = (
            context_builder
            or LLMContextBuilder()
        )

        self.response_formatter = (
            response_formatter
            or LLMResponseFormatter()
        )

        self.session = (
            session
            or LLMSession()
        )

        self.fallback_enabled = bool(
            fallback_enabled
        )

    def _crear_fallback(self) -> LLMEngine:
        """Crea un motor Mock para recuperación."""

        config = LLMConfig(
            proveedor="mock",
            modo="local"
        )

        return LLMEngine(
            provider=MockLLMProvider(
                modelo=config.modelo
            ),
            config=config
        )

    def generar(
        self,
        mensaje: str,
        memoria: list[str] | None = None,
        conocimiento: list[str] | None = None,
        razonamiento: list[str] | None = None,
        intencion: Intent | None = None
    ) -> LLMResponse:
        """Genera una respuesta y registra el turno."""

        if not isinstance(mensaje, str):
            raise LLMResponseError(
                "El mensaje debe ser texto."
            )

        mensaje = mensaje.strip()

        if not mensaje:
            raise LLMResponseError(
                "El mensaje no puede estar vacío."
            )

        if not self.session.esta_activa():
            raise LLMResponseError(
                "La sesión LLM no está activa."
            )

        self.session.agregar_usuario(
            mensaje
        )

        contexto_conversacional = (
            self.session.obtener_contexto()
        )

        contexto = self.context_builder.construir(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            conversacion=contexto_conversacional,
            intencion=intencion
        )

        request = LLMRequest(
            contexto=contexto,
            temperatura=self.engine.config.temperatura
        )

        if not request.es_valida():
            raise LLMResponseError(
                "La solicitud LLM no contiene un contexto válido."
            )

        try:
            respuesta = self.engine.generar(
                request
            )

        except LLMProviderError:

            if not self.fallback_enabled:
                raise

            fallback_engine = self._crear_fallback()

            respuesta = fallback_engine.generar(
                request
            )

        self.session.agregar_asistente(
            respuesta.contenido
        )

        return respuesta

    def generar_texto(
        self,
        mensaje: str,
        memoria: list[str] | None = None,
        conocimiento: list[str] | None = None,
        razonamiento: list[str] | None = None,
        intencion: Intent | None = None
    ) -> str:

        respuesta = self.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            intencion=intencion
        )

        return self.response_formatter.formatear(
            respuesta
        )

    def generar_con_metadatos(
        self,
        mensaje: str,
        memoria: list[str] | None = None,
        conocimiento: list[str] | None = None,
        razonamiento: list[str] | None = None,
        intencion: Intent | None = None
    ) -> str:

        respuesta = self.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            intencion=intencion
        )

        return self.response_formatter.formatear_con_metadatos(
            respuesta
        )

    def obtener_ultima_respuesta(self) -> LLMResponse | None:
        return self.engine.obtener_ultima_respuesta()

    def obtener_configuracion(self) -> LLMConfig:
        return self.engine.obtener_configuracion()

    def obtener_sesion(self) -> LLMSession:
        return self.session

    def obtener_conversacion(self) -> LLMSession:
        return self.obtener_sesion()

    def limpiar_conversacion(self):
        self.session.limpiar()

    def cerrar_sesion(self):
        self.session.cerrar()

    def reabrir_sesion(self):
        self.session.reabrir()