"""
CEREBRUM
Abstracción base para modelos de lenguaje.

v0.0.6 Alpha - LLM Core
"""

from dataclasses import dataclass
from typing import Protocol

from .cognitive_prompt_builder import CognitivePromptBuilder
from .llm_context import LLMContext


@dataclass
class LLMRequest:
    """Representa una solicitud enviada al modelo."""

    contexto: LLMContext
    temperatura: float = 0.7
    prompt: str | None = None

    def construir_prompt(self) -> str:
        """
        Construye el prompt final.

        Si ya existe un prompt explícito, lo reutiliza.
        De lo contrario, utiliza CognitivePromptBuilder.
        """

        if self.prompt is not None:
            return self.prompt

        if self.contexto is None:
            return ""

        builder = CognitivePromptBuilder()

        self.prompt = builder.construir(
            self.contexto
        )

        return self.prompt

    def es_valida(self) -> bool:
        """Indica si la solicitud contiene un prompt utilizable."""

        return bool(
            self.construir_prompt().strip()
        )


@dataclass
class LLMResponse:
    """Representa la respuesta generada por el modelo."""

    contenido: str
    modelo: str = "desconocido"
    confianza: float = 0.0


class LLMProvider(Protocol):
    """Contrato que debe cumplir cualquier proveedor LLM."""

    def generar(
        self,
        request: LLMRequest
    ) -> LLMResponse:
        """Genera una respuesta a partir de una solicitud."""
        ...