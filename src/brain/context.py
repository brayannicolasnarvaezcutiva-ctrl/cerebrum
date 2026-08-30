"""
CEREBRUM
Sistema de contexto conversacional.

v0.0.3 Alpha - Memory Seed
"""

from collections import Counter, deque


class Context:
    """Gestiona los mensajes recientes de una conversación."""

    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.messages = deque(
            maxlen=max_messages
        )

    def agregar(self, mensaje):
        """Añade un mensaje al contexto."""

        mensaje = mensaje.strip()

        if mensaje:
            self.messages.append(mensaje)

    def ultimo(self):
        """Devuelve el último mensaje."""

        if not self.messages:
            return None

        return self.messages[-1]

    def anteriores(self, cantidad=3):
        """Devuelve los últimos mensajes."""

        if cantidad <= 0:
            return []

        return list(self.messages)[-cantidad:]

    def contiene(self, termino):
        """Comprueba si el contexto contiene un término."""

        termino = termino.lower().strip()

        if not termino:
            return False

        return any(
            termino in mensaje.lower()
            for mensaje in self.messages
        )

    def tema_principal(self):
        """Devuelve una palabra frecuente del contexto."""

        palabras = []

        ignorar = {
            "que", "como", "para", "esta",
            "este", "esto", "desde", "porque",
            "cuando", "donde", "quiero", "mi",
            "mis", "me", "muy", "una", "uno",
            "las", "los", "del", "con", "por",
            "sobre", "estoy", "es", "soy"
        }

        for mensaje in self.messages:
            for palabra in mensaje.lower().split():
                palabra = palabra.strip(
                    ".,!?¿¡:;()[]{}\"'"
                )

                if (
                    len(palabra) >= 4
                    and palabra not in ignorar
                ):
                    palabras.append(palabra)

        if not palabras:
            return None

        contador = Counter(palabras)

        return contador.most_common(1)[0][0]

    def limpiar(self):
        """Limpia el contexto actual."""

        self.messages.clear()

    def obtener_todo(self):
        """Devuelve todos los mensajes."""

        return list(self.messages)

    def __len__(self):
        """Devuelve la cantidad de mensajes."""

        return len(self.messages)