"""
CEREBRUM
Formateador de respuestas del LLM.

v0.0.6 Alpha - LLM Core
"""

from .llm import LLMResponse


class LLMResponseFormatter:
    """Convierte respuestas internas del LLM en texto legible."""

    def formatear(
        self,
        respuesta: LLMResponse
    ) -> str:
        """Formatea una respuesta para presentación."""

        if respuesta is None:
            return "No se recibió ninguna respuesta."

        contenido = respuesta.contenido.strip()

        if not contenido:
            return "El LLM no produjo contenido."

        return contenido

    def formatear_con_metadatos(
        self,
        respuesta: LLMResponse
    ) -> str:
        """Incluye información del modelo y confianza."""

        if respuesta is None:
            return "No se recibió ninguna respuesta."

        contenido = self.formatear(
            respuesta
        )

        return (
            f"{contenido}\n\n"
            f"[Modelo: {respuesta.modelo}]\n"
            f"[Confianza: {respuesta.confianza:.2f}]"
        )