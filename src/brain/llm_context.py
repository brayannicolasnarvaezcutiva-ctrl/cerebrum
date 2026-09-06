"""
CEREBRUM
Contexto estructurado para el LLM.

v0.0.7 Alpha - Cognitive Interaction
"""

from dataclasses import dataclass, field

from .intent import Intent


@dataclass
class LLMContext:
    """Contiene toda la información disponible para una generación."""

    mensaje: str
    memoria: list[str] = field(default_factory=list)
    conocimiento: list[str] = field(default_factory=list)
    razonamiento: list[str] = field(default_factory=list)
    instrucciones: str = ""
    intencion: Intent | None = None

    def construir(self) -> str:
        """Construye una representación textual del contexto."""

        partes = []

        if self.instrucciones:
            partes.append(
                f"Instrucciones:\n{self.instrucciones}"
            )

        if self.intencion is not None:
            partes.append(
                "Intención:\n"
                f"- Tipo: {self.intencion.tipo}\n"
                f"- Acción: {self.intencion.accion}\n"
                f"- Tema: {self.intencion.tema}\n"
                f"- Confianza: {self.intencion.confianza:.2f}"
            )

        if self.memoria:
            partes.append(
                "Memoria relevante:\n"
                + "\n".join(
                    f"- {item}"
                    for item in self.memoria
                )
            )

        if self.conocimiento:
            partes.append(
                "Conocimiento relevante:\n"
                + "\n".join(
                    f"- {item}"
                    for item in self.conocimiento
                )
            )

        if self.razonamiento:
            partes.append(
                "Razonamiento:\n"
                + "\n".join(
                    f"- {item}"
                    for item in self.razonamiento
                )
            )

        partes.append(
            f"Mensaje del usuario:\n{self.mensaje}"
        )

        return "\n\n".join(partes)