"""
CEREBRUM
Controlador de conversación para la interfaz de chat.

v0.0.7 Alpha - Cognitive Interaction
"""

from .cerebrum_llm import CerebrumLLM


class ChatController:
    """
    Punto de entrada del sistema de chat.

    La interfaz gráfica no necesita conocer Cognitive Core,
    LLM Core ni los proveedores. Solo interactúa con esta clase.
    """

    def __init__(
        self,
        cerebrum: CerebrumLLM | None = None
    ):
        self.cerebrum = (
            cerebrum
            or CerebrumLLM()
        )

        self.conectado = True

    def enviar(
        self,
        mensaje: str
    ) -> str:
        """Envía un mensaje y devuelve la respuesta de CEREBRUM."""

        if not self.conectado:
            return "El chat no está conectado."

        if not isinstance(mensaje, str):
            return "El mensaje debe ser texto."

        mensaje = mensaje.strip()

        if not mensaje:
            return "Escribe un mensaje antes de enviarlo."

        return self.cerebrum.responder(
            mensaje
        )

    def obtener_intencion(
        self,
        mensaje: str
    ):
        """Permite a la interfaz consultar la intención detectada."""

        return self.cerebrum.detectar_intencion(
            mensaje
        )

    def limpiar_chat(self):
        """Limpia la conversación actual."""

        self.cerebrum.limpiar_conversacion()

    def desconectar(self):
        """Desconecta el controlador."""

        self.conectado = False

    def conectar(self):
        """Vuelve a conectar el controlador."""

        self.conectado = True

    def esta_conectado(self) -> bool:
        """Indica si el chat está conectado."""

        return self.conectado