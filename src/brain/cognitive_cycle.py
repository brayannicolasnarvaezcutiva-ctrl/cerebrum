"""
CEREBRUM
Ciclo cognitivo de alto nivel.

v0.0.5 Alpha - Cognitive Core
"""

from .cognitive_engine import CognitiveEngine
from .cognitive_result import CognitiveResult


class CognitiveCycle:
    """Ejecuta un ciclo cognitivo completo."""

    def __init__(
        self,
        cognitive_engine: CognitiveEngine | None = None
    ):
        self.engine = cognitive_engine or CognitiveEngine()

    def ejecutar(self, texto: str) -> CognitiveResult:
        """
        Ejecuta el ciclo cognitivo completo:

            entrada
              ↓
           aprender
              ↓
           inferir
              ↓
         registrar traza
              ↓
          resultado
        """

        return self.engine.procesar(texto)

    def aprender(self, texto: str):
        """Aprende conocimiento directamente."""

        return self.engine.aprender(texto)

    def inferir(self):
        """Ejecuta las inferencias disponibles."""

        return self.engine.inferir()

    def consultar(
        self,
        sujeto=None,
        relacion=None,
        objeto=None
    ):
        """Consulta conocimiento."""

        return self.engine.consultar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

    def obtener_traza(
        self,
        sujeto=None,
        relacion=None,
        objeto=None
    ):
        """Consulta la procedencia del conocimiento."""

        return self.engine.obtener_traza(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )