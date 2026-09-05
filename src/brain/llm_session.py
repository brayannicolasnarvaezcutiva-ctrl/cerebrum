"""
CEREBRUM
Gestión de sesión conversacional del LLM.

v0.0.6 Alpha - LLM Core
"""

from .llm_conversation import LLMConversation


class LLMSession:
    """Administra una sesión conversacional del LLM."""

    def __init__(
        self,
        conversation: LLMConversation | None = None
    ):
        self.conversation = (
            conversation
            or LLMConversation()
        )

        self.activa = True

    def agregar_usuario(
        self,
        contenido: str
    ):
        """Agrega un mensaje del usuario."""

        return self.conversation.agregar_usuario(
            contenido
        )

    def agregar_asistente(
        self,
        contenido: str
    ):
        """Agrega una respuesta del asistente."""

        return self.conversation.agregar_asistente(
            contenido
        )

    def obtener_historial(self):
        """Devuelve todos los mensajes de la sesión."""

        return self.conversation.obtener_todo()

    def obtener_todo(self):
        """
        Alias compatible con LLMConversation.

        Permite acceder al historial usando la API anterior.
        """

        return self.obtener_historial()

    def obtener_contexto(self) -> str:
        """Devuelve el historial en formato textual."""

        return self.conversation.construir_contexto()

    def construir_contexto(self) -> str:
        """
        Alias compatible con LLMConversation.

        Permite construir el contexto usando la API anterior.
        """

        return self.obtener_contexto()

    def cantidad_mensajes(self) -> int:
        """Devuelve la cantidad actual de mensajes."""

        return len(
            self.obtener_historial()
        )

    def limpiar(self):
        """Limpia la conversación actual."""

        self.conversation.limpiar()

    def cerrar(self):
        """Cierra la sesión."""

        self.activa = False

    def reabrir(self):
        """Reabre la sesión."""

        self.activa = True

    def esta_activa(self) -> bool:
        """Indica si la sesión está activa."""

        return self.activa