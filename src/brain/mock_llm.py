"""
CEREBRUM
Proveedor LLM simulado para pruebas.

v0.0.6 Alpha - LLM Core
"""

from .llm import LLMProvider, LLMRequest, LLMResponse


class MockLLMProvider:
    """Proveedor local que simula una respuesta de un LLM."""

    def __init__(self, modelo: str = "mock-llm"):
        self.modelo = modelo
        self.ultima_solicitud: LLMRequest | None = None

    def generar(self, request: LLMRequest) -> LLMResponse:
        """Genera una respuesta simulada."""

        self.ultima_solicitud = request

        prompt = request.construir_prompt()

        if not prompt.strip():
            return LLMResponse(
                contenido="No hay información para procesar.",
                modelo=self.modelo,
                confianza=0.0
            )

        return LLMResponse(
            contenido=(
                "Respuesta simulada del LLM.\n\n"
                f"Prompt recibido:\n{prompt}"
            ),
            modelo=self.modelo,
            confianza=1.0
        )