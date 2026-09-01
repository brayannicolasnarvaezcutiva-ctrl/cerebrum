"""
CEREBRUM
Sistema de contexto conversacional.

v0.0.4 Alpha - Reasoning Core
"""

from collections import Counter, deque


class Context:
    """Gestiona los mensajes recientes de una conversación."""

    PALABRAS_IGNORADAS = {
        "que",
        "como",
        "para",
        "esta",
        "este",
        "esto",
        "desde",
        "porque",
        "cuando",
        "donde",
        "quiero",
        "mi",
        "mis",
        "me",
        "muy",
        "una",
        "uno",
        "las",
        "los",
        "del",
        "con",
        "por",
        "sobre",
        "estoy",
        "estás",
        "estamos",
        "es",
        "soy",
        "si",
        "entonces",
        "analiza",
        "analizar",
        "compara",
        "compara",
        "recuerda",
        "memoria",
        "contexto",
        "tema",
        "muestra",
        "muestra",
        "muéstrame",
        "mis",
        "qué"
    }

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
        """Devuelve la palabra relevante más frecuente."""

        palabras = []

        for mensaje in self.messages:
            for palabra in mensaje.lower().split():
                palabra = palabra.strip(
                    ".,!?¿¡:;()[]{}\"'"
                )

                if (
                    len(palabra) >= 4
                    and palabra not in self.PALABRAS_IGNORADAS
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