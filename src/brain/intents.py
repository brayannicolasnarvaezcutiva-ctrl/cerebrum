"""
brain/intents.py

Intenciones básicas de CEREBRUM.
"""


INTENTS = {
    "greeting": {
        "phrases": (
            "hola",
            "hola cerebrum",
            "buenas",
        ),
        "response": "Hola. ¿En qué puedo ayudarte?",
    },

    "status": {
        "phrases": (
            "como estas",
            "cómo estás",
            "como te encuentras",
        ),
        "response": "Estoy funcionando correctamente. ¿En qué puedo ayudarte?",
    },
}


def detect_intent(text: str):
    """Detecta una intención básica a partir del texto."""

    text = text.strip().lower()

    for intent, data in INTENTS.items():
        if text in data["phrases"]:
            return intent

    return None