"""
CEREBRUM
Selector de contexto cognitivo según la intención.

v0.0.7 Alpha - Cognitive Interaction
"""

from .intent import Intent


class CognitiveContextSelector:
    """
    Decide qué tipos de información cognitiva son relevantes
    para una intención determinada.
    """

    def seleccionar(
        self,
        intencion: Intent | None
    ) -> dict[str, bool]:
        """Determina qué fuentes de contexto deben utilizarse."""

        if intencion is None:
            return {
                "memoria": True,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": True
            }

        if intencion.tipo == "pregunta":

            if intencion.accion == "explicar":
                return {
                    "memoria": False,
                    "conocimiento": True,
                    "razonamiento": True,
                    "conversacion": True
                }

            if intencion.accion == "recordar":
                return {
                    "memoria": True,
                    "conocimiento": False,
                    "razonamiento": False,
                    "conversacion": True
                }

            if intencion.accion == "buscar":
                return {
                    "memoria": False,
                    "conocimiento": True,
                    "razonamiento": False,
                    "conversacion": True
                }

            return {
                "memoria": True,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": True
            }

        if intencion.tipo == "comando":

            if intencion.accion == "crear":
                return {
                    "memoria": True,
                    "conocimiento": True,
                    "razonamiento": True,
                    "conversacion": True
                }

            if intencion.accion == "resolver":
                return {
                    "memoria": False,
                    "conocimiento": True,
                    "razonamiento": True,
                    "conversacion": False
                }

            if intencion.accion == "buscar":
                return {
                    "memoria": False,
                    "conocimiento": True,
                    "razonamiento": False,
                    "conversacion": True
                }

        if intencion.tipo == "afirmacion":
            return {
                "memoria": True,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": True
            }

        return {
            "memoria": True,
            "conocimiento": True,
            "razonamiento": True,
            "conversacion": True
        }