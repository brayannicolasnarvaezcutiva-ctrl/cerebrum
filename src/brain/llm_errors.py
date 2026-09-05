"""
CEREBRUM
Errores controlados del LLM Core.

v0.0.6 Alpha - LLM Core
"""


class LLMError(Exception):
    """Error base del sistema LLM."""


class LLMConfigurationError(LLMError):
    """Error en la configuración del LLM."""


class LLMProviderError(LLMError):
    """Error producido por un proveedor LLM."""


class LLMResponseError(LLMError):
    """Error relacionado con una respuesta del LLM."""