"""
CEREBRUM
Recuperación de contexto cognitivo relevante.

v0.0.7 Alpha - Cognitive Interaction
"""

from .cognitive_context_selector import CognitiveContextSelector
from .cognitive_engine import CognitiveEngine


class CognitiveContextRetriever:
    """
    Recupera información relevante del Cognitive Core
    y del contexto conversacional.
    """

    def __init__(
        self,
        cognitive_engine: CognitiveEngine,
        selector: CognitiveContextSelector | None = None,
        limite: int = 10
    ):
        self.cognitive_engine = cognitive_engine

        self.selector = (
            selector
            or CognitiveContextSelector()
        )

        self.limite = max(
            1,
            int(limite)
        )

    def recuperar(
        self,
        intencion,
        conversacion: str = ""
    ) -> dict:
        """
        Recupera contexto según la intención.

        Devuelve:

        {
            "memoria": [],
            "conocimiento": [],
            "razonamiento": [],
            "conversacion": ""
        }
        """

        seleccion = self.selector.seleccionar(
            intencion
        )

        resultado = {
            "memoria": [],
            "conocimiento": [],
            "razonamiento": [],
            "conversacion": ""
        }

        if intencion is None:
            return resultado

        tema = (
            intencion.tema.strip()
            if isinstance(
                intencion.tema,
                str
            )
            else ""
        )

        # -------------------------
        # CONVERSACIÓN
        # -------------------------

        if seleccion.get(
            "conversacion",
            False
        ):
            if isinstance(
                conversacion,
                str
            ):
                resultado["conversacion"] = (
                    conversacion.strip()
                )

        # -------------------------
        # CONOCIMIENTO
        # -------------------------

        if (
            seleccion.get(
                "conocimiento",
                False
            )
            and tema
        ):
            hechos = (
                self.cognitive_engine
                .knowledge_base
                .buscar_relevante(
                    tema,
                    limite=self.limite
                )
            )

            resultado["conocimiento"] = [
                f"{hecho.sujeto} "
                f"{hecho.relacion} "
                f"{hecho.objeto}"
                for hecho in hechos
            ]

        # -------------------------
        # RAZONAMIENTO
        # -------------------------

        if seleccion.get(
            "razonamiento",
            False
        ):
            inferencias = (
                self.cognitive_engine
                .inference
                .inferir_todo()
            )

            resultado["razonamiento"] = [
                f"{inferencia.conclusion.sujeto} "
                f"{inferencia.conclusion.relacion} "
                f"{inferencia.conclusion.objeto}"
                for inferencia in inferencias
            ]

        return resultado