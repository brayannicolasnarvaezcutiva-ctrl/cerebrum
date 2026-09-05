"""
CEREBRUM
Configuración del LLM.

v0.0.6 Alpha - LLM Core
"""

from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuración común para un proveedor LLM."""

    proveedor: str = "mock"
    modelo: str | None = None
    temperatura: float = 0.7
    max_tokens: int = 1000
    api_key: str | None = None
    modo: str = "local"
    fallback_enabled: bool = False

    def __post_init__(self):
        """Valida y normaliza la configuración."""

        self.proveedor = self.proveedor.strip().lower()
        self.modo = self.modo.strip().lower()

        modos_validos = {
            "local",
            "online"
        }

        if self.modo not in modos_validos:
            raise ValueError(
                f"Modo LLM no válido: {self.modo}"
            )

        modelos_por_defecto = {
            "mock": "mock-llm",
            "openai": "modelo-openai"
        }

        if self.modelo is None:
            self.modelo = modelos_por_defecto.get(
                self.proveedor,
                "desconocido"
            )

        self.modelo = self.modelo.strip()

        if self.api_key is not None:
            self.api_key = self.api_key.strip()

        self.temperatura = max(
            0.0,
            min(2.0, float(self.temperatura))
        )

        self.max_tokens = max(
            1,
            int(self.max_tokens)
        )

        self.fallback_enabled = bool(
            self.fallback_enabled
        )