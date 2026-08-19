"""
brain/processor.py

Procesador principal del motor de IA.
"""

from brain.intents import INTENTS, detect_intent


class BrainProcessor:
    """Procesa las entradas del usuario."""

    def process(self, text: str):
        intent = detect_intent(text)

        if intent is not None:
            return INTENTS[intent]["response"]

        text = text.strip().lower()

        return f"Todavía estoy aprendiendo a procesar: {text}"