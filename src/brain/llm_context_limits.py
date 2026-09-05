"""
CEREBRUM
Control de tamaño y límites del contexto LLM.

v0.0.6 Alpha - LLM Core
"""


class LLMContextLimits:
    """Valida y limita el tamaño del contexto enviado al LLM."""

    def __init__(
        self,
        max_characters: int = 12000,
        max_memory_items: int = 10,
        max_knowledge_items: int = 10,
        max_reasoning_items: int = 10
    ):
        self.max_characters = max(
            1,
            int(max_characters)
        )

        self.max_memory_items = max(
            0,
            int(max_memory_items)
        )

        self.max_knowledge_items = max(
            0,
            int(max_knowledge_items)
        )

        self.max_reasoning_items = max(
            0,
            int(max_reasoning_items)
        )

    def limitar_lista(
        self,
        elementos: list[str] | None,
        max_items: int
    ) -> list[str]:
        """Limita una lista conservando los primeros elementos válidos."""

        if not elementos or max_items <= 0:
            return []

        resultado = []

        for elemento in elementos:
            if not isinstance(elemento, str):
                continue

            elemento = elemento.strip()

            if not elemento:
                continue

            if elemento in resultado:
                continue

            resultado.append(elemento)

            if len(resultado) >= max_items:
                break

        return resultado

    def limitar_contexto(
        self,
        texto: str
    ) -> str:
        """Limita el contexto final por número de caracteres."""

        if not isinstance(texto, str):
            return ""

        texto = texto.strip()

        if len(texto) <= self.max_characters:
            return texto

        return texto[:self.max_characters].rstrip()