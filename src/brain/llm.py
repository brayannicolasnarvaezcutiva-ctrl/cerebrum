"""
CEREBRUM
Abstracción base para modelos de lenguaje.

v0.0.6 Alpha - LLM Core
"""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class LLMRequest:
    """Representa una solicitud enviada al modelo."""

    prompt: str
    contexto: str = ""
    temperatura: float = 0.7


@dataclass
class LLMResponse:
    """Representa la respuesta generada por el modelo."""

    contenido: str
    modelo: str = "desconocido"
    confianza: float = 0.0


class LLMProvider(Protocol):
    """Contrato que debe cumplir cualquier proveedor LLM."""

    def generar(self, request: LLMRequest) -> LLMResponse:
        """Genera una respuesta a partir de una solicitud."""
        ...