"""
CEREBRUM
Constructor de contexto para el LLM.

v0.0.6 Alpha - LLM Core
"""

from .llm_context import LLMContext
from .llm_context_limits import LLMContextLimits


class LLMContextBuilder:
    """Construye contextos estructurados y controlados para el LLM."""

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
        mensaje: str,
        memoria: list[str] | None = None,
        conocimiento: list[str] | None = None,
        razonamiento: list[str] | None = None,
        conversacion: str = ""
    ) -> LLMContext:
        """Construye un contexto normalizado y limitado."""

        mensaje = (
            mensaje.strip()
            if isinstance(mensaje, str)
            else ""
        )

        conversacion = (
            conversacion.strip()
            if isinstance(conversacion, str)
            else ""
        )

        memoria = self.limits.limitar_lista(
            list(memoria or []),
            self.limits.max_memory_items
        )

        conocimiento = self.limits.limitar_lista(
            list(conocimiento or []),
            self.limits.max_knowledge_items
        )

        razonamiento = self.limits.limitar_lista(
            list(razonamiento or []),
            self.limits.max_reasoning_items
        )

        if conversacion:
            razonamiento = [
                f"Historial de conversación:\n{conversacion}"
            ] + razonamiento

        contexto = LLMContext(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            instrucciones=self.instrucciones
        )

        return contexto

    def construir_texto(
        self,
        mensaje: str,
        memoria: list[str] | None = None,
        conocimiento: list[str] | None = None,
        razonamiento: list[str] | None = None,
        conversacion: str = ""
    ) -> str:
        """Construye y limita directamente el texto de contexto."""

        contexto = self.construir(
            mensaje=mensaje,
            memoria=memoria,
            conocimiento=conocimiento,
            razonamiento=razonamiento,
            conversacion=conversacion
        )

        texto = contexto.construir()

        return self.limits.limitar_contexto(
            texto
        )