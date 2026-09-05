"""
CEREBRUM
Constructor de prompts cognitivos.

v0.0.6 Alpha - LLM Core
"""

from .llm_context import LLMContext
from .llm_context_limits import LLMContextLimits


class CognitivePromptBuilder:
    """
    Construye el prompt final a partir del contexto cognitivo.

    No llama al LLM ni modifica memoria.
    """

    def __init__(
        self,
        instrucciones: str = "",
        limits: LLMContextLimits | None = None
    ):
        self.instrucciones = instrucciones.strip()

        self.limits = (
            limits
            or LLMContextLimits()
        )

    def construir(
        self,
        contexto: LLMContext
    ) -> str:
        """Construye y limita el prompt final."""

        if contexto is None:
            return ""

        partes = []

        instrucciones = (
            contexto.instrucciones.strip()
            if isinstance(
                contexto.instrucciones,
                str
            )
            else ""
        )

        if not instrucciones:
            instrucciones = self.instrucciones

        if instrucciones:
            partes.append(
                "=== INSTRUCCIONES ===\n"
                + instrucciones
            )

        if contexto.memoria:
            partes.append(
                "=== MEMORIA RELEVANTE ===\n"
                + self._formatear_lista(
                    contexto.memoria
                )
            )

        if contexto.conocimiento:
            partes.append(
                "=== CONOCIMIENTO RELEVANTE ===\n"
                + self._formatear_lista(
                    contexto.conocimiento
                )
            )

        if contexto.razonamiento:
            partes.append(
                "=== RAZONAMIENTO ===\n"
                + self._formatear_lista(
                    contexto.razonamiento
                )
            )

        partes.append(
            "=== MENSAJE DEL USUARIO ===\n"
            + contexto.mensaje.strip()
        )

        prompt = "\n\n".join(partes)

        return self.limits.limitar_contexto(
            prompt
        )

    @staticmethod
    def _formatear_lista(
        elementos: list[str]
    ) -> str:
        """Convierte una lista en líneas numeradas."""

        resultado = []

        for indice, elemento in enumerate(
            elementos,
            start=1
        ):
            if not isinstance(elemento, str):
                continue

            elemento = elemento.strip()

            if not elemento:
                continue

            resultado.append(
                f"{indice}. {elemento}"
            )

        return "\n".join(
            resultado
        )