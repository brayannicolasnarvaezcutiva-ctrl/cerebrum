"""
CEREBRUM
Proveedor OpenAI para el LLM Core.

v0.0.9 Alpha — preparación hacia v0.1.0
"""

import os

from .llm import LLMRequest, LLMResponse
from .llm_errors import LLMConfigurationError


class OpenAIProvider:
    """Proveedor LLM basado en la API de OpenAI."""

    def __init__(
        self,
        modelo: str,
        api_key: str | None = None,
        max_tokens: int = 1000
    ):
        self.modelo = modelo.strip()

        self.api_key = (
            api_key
            or os.getenv("OPENAI_API_KEY")
        )

        self.max_tokens = max(
            1,
            int(max_tokens)
        )

        if not self.api_key:
            raise ValueError(
                "No se encontró OPENAI_API_KEY."
            )

        try:
            from openai import OpenAI
        except ImportError as error:
            raise LLMConfigurationError(
                "El proveedor OpenAI requiere instalar el extra 'openai'."
            ) from error

        self.client = OpenAI(
            api_key=self.api_key
        )

    def generar(
        self,
        request: LLMRequest
    ) -> LLMResponse:
        """Genera una respuesta mediante OpenAI."""

        if request is None:
            raise ValueError(
                "La solicitud LLM no puede ser None."
            )

        prompt = request.construir_prompt()

        if not prompt.strip():
            raise ValueError(
                "El prompt no puede estar vacío."
            )

        try:
            respuesta = self.client.responses.create(
                model=self.modelo,
                input=prompt,
                temperature=request.temperatura,
                max_output_tokens=self.max_tokens
            )
        except Exception as error:
            raise RuntimeError(
                f"Error en OpenAI: {error}"
            ) from error

        contenido = respuesta.output_text.strip()

        if not contenido:
            raise ValueError(
                "OpenAI devolvió una respuesta vacía."
            )

        return LLMResponse(
            contenido=contenido,
            modelo=self.modelo,
            confianza=1.0
        )
