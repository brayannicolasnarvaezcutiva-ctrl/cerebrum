"""
CEREBRUM
Motor de ejecución del LLM.

v0.0.6 Alpha - LLM Core
"""

from .llm import LLMProvider, LLMRequest, LLMResponse
from .llm_config import LLMConfig
from .llm_errors import LLMProviderError, LLMResponseError
from .llm_factory import LLMFactory


class LLMEngine:
    """Coordina las solicitudes hacia un proveedor LLM."""

    def __init__(
        self,
        provider: LLMProvider,
        config: LLMConfig | None = None
    ):
        self.provider = provider
        self.config = config or LLMConfig()
        self.ultima_respuesta: LLMResponse | None = None

    @classmethod
    def desde_config(
        cls,
        config: LLMConfig | None = None
    ) -> "LLMEngine":
        """Construye un motor usando una configuración."""

        config = config or LLMConfig()

        provider = LLMFactory.crear(
            config
        )

        return cls(
            provider=provider,
            config=config
        )

    def generar(
        self,
        request: LLMRequest
    ) -> LLMResponse:
        """Envía una solicitud al proveedor."""

        if request is None:
            raise ValueError(
                "La solicitud LLM no puede ser None."
            )

        try:
            request.temperatura = self.config.temperatura

            respuesta = self.provider.generar(
                request
            )

        except Exception as error:
            raise LLMProviderError(
                f"Error al generar respuesta: {error}"
            ) from error

        if respuesta is None:
            raise LLMResponseError(
                "El proveedor no devolvió una respuesta."
            )

        if not isinstance(
            respuesta,
            LLMResponse
        ):
            raise LLMResponseError(
                "El proveedor devolvió un tipo de respuesta inválido."
            )

        self.ultima_respuesta = respuesta

        return respuesta

    def obtener_ultima_respuesta(
        self
    ) -> LLMResponse | None:
        """Devuelve la última respuesta generada."""

        return self.ultima_respuesta

    def obtener_configuracion(
        self
    ) -> LLMConfig:
        """Devuelve la configuración actual."""

        return self.config