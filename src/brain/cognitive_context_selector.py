"""
CEREBRUM
Selección de contexto cognitivo.

v0.0.7 Alpha - Cognitive Interaction
"""

from .intent import Intent


class CognitiveContextSelector:
    """
    Decide qué fuentes de contexto son relevantes
    para una intención determinada.
    """

    def seleccionar(
        self,
        intencion: Intent | None
    ) -> dict[str, bool]:
        """Selecciona las fuentes de contexto."""

        if intencion is None:
            return self._general()

        estrategia = self._estrategia(
            intencion
        )

        estrategias = {
            "explicacion": {
                "memoria": True,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": True
            },
            "memoria": {
                "memoria": True,
                "conocimiento": False,
                "razonamiento": False,
                "conversacion": True
            },
            "busqueda": {
                "memoria": False,
                "conocimiento": True,
                "razonamiento": False,
                "conversacion": True
            },
            "resolucion": {
                "memoria": False,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": False
            },
            "creacion": {
                "memoria": True,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": True
            },
            "aprendizaje": {
                "memoria": True,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": True
            },
            "ejecucion": {
                "memoria": True,
                "conocimiento": True,
                "razonamiento": True,
                "conversacion": True
            }
        }

        return estrategias.get(
            estrategia,
            self._general()
        )

    def _estrategia(
        self,
        intencion: Intent
    ) -> str:
        """Convierte una intención en estrategia."""

        if intencion.tipo == "pregunta":

            if intencion.accion == "explicar":
                return "explicacion"

            if intencion.accion == "recordar":
                return "memoria"

            if intencion.accion == "buscar":
                return "busqueda"

            if intencion.accion == "resolver":
                return "resolucion"

        if intencion.tipo == "comando":

            if intencion.accion == "crear":
                return "creacion"

            if intencion.accion == "resolver":
                return "resolucion"

            if intencion.accion == "buscar":
                return "busqueda"

            return "ejecucion"

        if intencion.tipo == "afirmacion":
            return "aprendizaje"

        return "respuesta_general"

    @staticmethod
    def _general() -> dict[str, bool]:
        """Selección general."""

        return {
            "memoria": True,
            "conocimiento": True,
            "razonamiento": True,
            "conversacion": True
        }
    