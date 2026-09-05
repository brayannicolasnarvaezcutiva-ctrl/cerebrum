"""
CEREBRUM
Fábrica de proveedores LLM.

v0.0.6 Alpha - LLM Core
"""

from .llm import LLMProvider
from .llm_config import LLMConfig
from .mock_llm import MockLLMProvider
from .openai_provider import OpenAIProvider


class LLMFactory:
    """Construye proveedores LLM según la configuración."""

    @staticmethod
    def crear(
        config: LLMConfig
    ) -> LLMProvider:
        """Crea el proveedor correspondiente."""

        if config is None:
            config = LLMConfig()

        proveedor = config.proveedor.lower()
        modo = config.modo.lower()

        if proveedor == "mock":
            return MockLLMProvider(
                modelo=config.modelo
            )

        if proveedor == "openai":
            if modo != "online":
                raise ValueError(
                    "OpenAI requiere modo='online'."
                )

            return OpenAIProvider(
                modelo=config.modelo,
                api_key=config.api_key,
                max_tokens=config.max_tokens
            )

        raise ValueError(
            f"Proveedor LLM no soportado: {config.proveedor}"
        )