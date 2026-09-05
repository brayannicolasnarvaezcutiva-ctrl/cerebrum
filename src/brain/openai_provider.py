"""
CEREBRUM
Proveedor OpenAI para el LLM Core.

v0.0.6 Alpha - LLM Core
"""

import os

from openai import OpenAI

from .llm import LLMRequest, LLMResponse


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