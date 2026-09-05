"""
CEREBRUM
Administrador del sistema LLM.

v0.0.6 Alpha - LLM Core
"""

from .llm import LLMResponse
from .llm_config import LLMConfig
from .llm_engine import LLMEngine
from .llm_environment import LLMEnvironment
from .llm_service import LLMService


class LLMManager:
    """Administra la configuración y el servicio LLM activo."""

    def __init__(
        self,
        config: LLMConfig | None = None
    ):
        self.config = config or LLMConfig()

        self.engine = LLMEngine.desde_config(
            self.config
        )

        self.service = LLMService(
            self.engine,
            fallback_enabled=self.config.fallback_enabled
        )

    @classmethod
    def desde_entorno(cls):
        """Construye el administrador desde variables de entorno."""

        return cls(
            LLMEnvironment.cargar()
        )

    def generar(
        self,
        mensaje: str,
        memoria: list[str] | None = None,
        conocimiento: list[str] | None = None,
        razonamiento: list[str] | None = None
    ) -> LLMResponse:
        """Genera una respuesta usando el servicio activo."""

        return self.service.generar(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento
        )

    def generar_texto(
        self,
        mensaje: str,
        memoria: list[str] | None = None,
        conocimiento: list[str] | None = None,
        razonamiento: list[str] | None = None
    ) -> str:
        """Genera únicamente el texto de la respuesta."""

        return self.service.generar_texto(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento
        )

    def conversar(
        self,
        mensaje: str
    ) -> str:
        """Ejecuta un turno de conversación."""

        return self.generar_texto(
            mensaje=mensaje
        )

    def diagnostico(self) -> dict:
        """Devuelve el estado del LLM sin llamar al proveedor."""

        return {
            "proveedor": self.config.proveedor,
            "modelo": self.config.modelo,
            "modo": self.config.modo,
            "temperatura": self.config.temperatura,
            "max_tokens": self.config.max_tokens,
            "api_key_configurada": bool(
                self.config.api_key
            ),
            "fallback_enabled": self.config.fallback_enabled,
            "proveedor_activo": type(
                self.engine.provider
            ).__name__,
            "sesion_activa": (
                self.service
                .obtener_sesion()
                .esta_activa()
            )
        }

    def obtener_proveedor(self):
        """Devuelve el proveedor activo."""

        return self.engine.provider

    def obtener_nombre_proveedor(self) -> str:
        """Devuelve el nombre de la clase del proveedor."""

        return type(
            self.engine.provider
        ).__name__

    def obtener_configuracion(self) -> LLMConfig:
        """Devuelve la configuración actual."""

        return self.config

    def obtener_sesion(self):
        """Devuelve la sesión conversacional activa."""

        return self.service.obtener_sesion()

    def limpiar_conversacion(self):
        """Limpia el historial conversacional."""

        self.service.limpiar_conversacion()

    def cerrar_sesion(self):
        """Cierra la sesión actual."""

        self.service.cerrar_sesion()

    def reabrir_sesion(self):
        """Reabre la sesión actual."""

        self.service.reabrir_sesion()

    def cambiar_configuracion(
        self,
        config: LLMConfig
    ):
        """Cambia la configuración y reconstruye el servicio."""

        if config is None:
            raise ValueError(
                "La configuración no puede ser None."
            )

        self.config = config

        self.engine = LLMEngine.desde_config(
            self.config
        )

        self.service = LLMService(
            self.engine,
            fallback_enabled=self.config.fallback_enabled
        )