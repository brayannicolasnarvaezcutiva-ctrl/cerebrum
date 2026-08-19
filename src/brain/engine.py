"""
brain/engine.py

Motor principal de CEREBRUM.
"""

from brain.processor import BrainProcessor


class BrainEngine:
    """Motor principal de IA."""

    def __init__(self):
        self.processor = BrainProcessor()

    def process(self, text: str):
        return self.processor.process(text)