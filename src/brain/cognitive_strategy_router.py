"""
CEREBRUM
Enrutador de estrategias cognitivas.

v0.0.7 Alpha - Cognitive Interaction
"""

from .intent import Intent


class CognitiveStrategyRouter:
    """Selecciona la estrategia de procesamiento."""

    def enrutar(
        self,
        intencion: Intent | None
    ) -> str:
        """Devuelve la estrategia adecuada."""

        if intencion is None:
            return "respuesta_general"

        if intencion.tipo == "pregunta":

            estrategias = {
                "explicar": "explicacion",
                "buscar": "busqueda",
                "recordar": "memoria",
                "resolver": "resolucion"
            }

            return estrategias.get(
                intencion.accion,
                "respuesta_directa"
            )

        if intencion.tipo == "comando":

            estrategias = {
                "crear": "creacion",
                "buscar": "busqueda",
                "resolver": "resolucion"
            }

            return estrategias.get(
                intencion.accion,
                "ejecucion"
            )

        if intencion.tipo == "afirmacion":
            return "aprendizaje"

        return "respuesta_general"

    def instrucciones(
        self,
        estrategia: str
    ) -> str:
        """Convierte una estrategia en instrucciones para el LLM."""

        instrucciones = {
            "explicacion":
                "Explica el tema de forma clara y comprensible.",

            "busqueda":
                "Prioriza información relevante y verificable.",

            "memoria":
                "Utiliza primero la memoria y el historial relevante.",

            "resolucion":
                "Analiza el problema paso a paso y verifica la conclusión.",

            "creacion":
                "Construye el resultado solicitado siguiendo el contexto disponible.",

            "aprendizaje":
                "Analiza la afirmación y conserva el conocimiento relevante.",

            "ejecucion":
                "Interpreta la solicitud como una acción que debe procesarse.",

            "respuesta_directa":
                "Responde directamente a la solicitud.",

            "respuesta_general":
                "Procesa la entrada de forma general."
        }

        return instrucciones.get(
            estrategia,
            instrucciones["respuesta_general"]
        )