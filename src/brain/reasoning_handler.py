"""
CEREBRUM
Manejador de solicitudes de razonamiento.

v0.0.4 Alpha - Reasoning Core
"""

from dataclasses import dataclass

from brain.memory_service import MemoryService
from brain.reasoning import ReasoningEngine


@dataclass
class ReasoningRequestResult:
    """Resultado estructurado de una solicitud de razonamiento."""

    resultado: object = None
    mensaje: str = None


class ReasoningRequestHandler:
    """Prepara solicitudes de razonamiento y su evidencia."""

    def __init__(self, memory_service=None, reasoning=None):
        self.memory_service = (
            memory_service
            if memory_service is not None
            else MemoryService()
        )
        self.reasoning = (
            reasoning
            if reasoning is not None
            else ReasoningEngine()
        )

    def manejar(self, text: str):
        """Procesa una solicitud de análisis o comparación."""

        if text.startswith("analiza "):
            return self.analizar(text)

        if text.startswith("compara "):
            return self.comparar(text)

        return None

    def analizar(self, text: str):
        """Prepara y ejecuta una solicitud de análisis."""

        contenido = text[8:].strip()

        if not contenido:
            return ReasoningRequestResult(
                mensaje="No hay nada que analizar."
            )

        recuerdos = self.memory_service.obtener_recuerdos_para_texto(
            contenido
        )
        resultado = self.reasoning.analizar(
            contenido,
            recuerdos=recuerdos
        )

        return ReasoningRequestResult(resultado=resultado)

    def comparar(self, text: str):
        """Prepara y ejecuta una solicitud de comparación."""

        contenido = text[8:].strip()
        partes = contenido.split(
            " vs ",
            1
        )

        if len(partes) != 2:
            return ReasoningRequestResult(
                mensaje=(
                    "Usa el formato: "
                    "compara opción A vs opción B"
                )
            )

        opcion_a = partes[0].strip()
        opcion_b = partes[1].strip()
        recuerdos = self.memory_service.obtener_recuerdos_para_texto(
            f"{opcion_a} {opcion_b}"
        )
        resultado = self.reasoning.comparar(
            opcion_a,
            opcion_b,
            recuerdos=recuerdos
        )

        return ReasoningRequestResult(resultado=resultado)
