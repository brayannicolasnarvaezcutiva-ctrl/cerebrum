"""
CEREBRUM
Historial de conversación para el LLM.

v0.0.6 Alpha - LLM Core
"""

from dataclasses import dataclass


@dataclass
class ConversationMessage:
    """Representa un mensaje dentro de la conversación."""

    rol: str
    contenido: str


class LLMConversation:
    """Mantiene el historial reciente de una conversación."""

    ROLES_VALIDOS = {"usuario", "asistente", "sistema"}

    def __init__(self, max_mensajes: int = 20):
        self.max_mensajes = max(
            1,
            int(max_mensajes)
        )

        self.mensajes: list[ConversationMessage] = []

    def agregar(
        self,
        rol: str,
        contenido: str
    ) -> ConversationMessage | None:
        """Agrega un mensaje al historial."""

        if not isinstance(rol, str):
            return None

        if not isinstance(contenido, str):
            return None

        rol = rol.strip().lower()
        contenido = contenido.strip()

        if rol not in self.ROLES_VALIDOS:
            return None

        if not contenido:
            return None

        mensaje = ConversationMessage(
            rol=rol,
            contenido=contenido
        )

        self.mensajes.append(mensaje)

        if len(self.mensajes) > self.max_mensajes:
            exceso = len(self.mensajes) - self.max_mensajes
            del self.mensajes[:exceso]

        return mensaje

    def agregar_usuario(
        self,
        contenido: str
    ) -> ConversationMessage | None:
        """Agrega un mensaje del usuario."""

        return self.agregar(
            rol="usuario",
            contenido=contenido
        )

    def agregar_asistente(
        self,
        contenido: str
    ) -> ConversationMessage | None:
        """Agrega una respuesta del asistente."""

        return self.agregar(
            rol="asistente",
            contenido=contenido
        )

    def agregar_sistema(
        self,
        contenido: str
    ) -> ConversationMessage | None:
        """Agrega un mensaje del sistema."""

        return self.agregar(
            rol="sistema",
            contenido=contenido
        )

    def obtener_todo(self) -> list[ConversationMessage]:
        """Devuelve el historial actual."""

        return list(self.mensajes)

    def limpiar(self):
        """Elimina todo el historial."""

        self.mensajes.clear()

    def construir_contexto(self) -> str:
        """Convierte el historial en texto para el LLM."""

        if not self.mensajes:
            return ""

        return "\n".join(
            f"{mensaje.rol}: {mensaje.contenido}"
            for mensaje in self.mensajes
        )