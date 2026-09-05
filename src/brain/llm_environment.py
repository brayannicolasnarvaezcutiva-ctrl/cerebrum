"""
CEREBRUM
Carga de configuración LLM desde variables de entorno.

v0.0.6 Alpha - LLM Core
"""

import os

from .llm_config import LLMConfig


class LLMEnvironment:
    """Construye configuración LLM desde el entorno."""

    @staticmethod
    def cargar() -> LLMConfig:
        """Carga toda la configuración disponible."""

        return LLMConfig(
            proveedor=LLMEnvironment.proveedor(),
            modelo=LLMEnvironment.modelo(),
            temperatura=LLMEnvironment.temperatura(),
            max_tokens=LLMEnvironment.max_tokens(),
            api_key=LLMEnvironment.api_key(),
            modo=LLMEnvironment.modo(),
            fallback_enabled=LLMEnvironment.fallback_enabled()
        )

    @staticmethod
    def proveedor() -> str:
        return os.getenv(
            "CEREBRUM_LLM_PROVIDER",
            "mock"
        ).strip().lower()

    @staticmethod
    def modelo() -> str | None:
        modelo = os.getenv(
            "CEREBRUM_LLM_MODEL"
        )

        if modelo is None:
            return None

        modelo = modelo.strip()

        return modelo or None

    @staticmethod
    def temperatura() -> float:
        return float(
            os.getenv(
                "CEREBRUM_LLM_TEMPERATURE",
                "0.7"
            )
        )

    @staticmethod
    def max_tokens() -> int:
        return int(
            os.getenv(
                "CEREBRUM_LLM_MAX_TOKENS",
                "1000"
            )
        )

    @staticmethod
    def modo() -> str:
        return os.getenv(
            "CEREBRUM_LLM_MODE",
            "local"
        ).strip().lower()

    @staticmethod
    def api_key() -> str | None:
        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if api_key is None:
            return None

        api_key = api_key.strip()

        return api_key or None

    @staticmethod
    def fallback_enabled() -> bool:
        valor = os.getenv(
            "CEREBRUM_LLM_FALLBACK",
            "false"
        ).strip().lower()

        return valor in {
            "1",
            "true",
            "yes",
            "on"
        }

    @staticmethod
    def tiene_api_key() -> bool:
        return bool(
            LLMEnvironment.api_key()
        )