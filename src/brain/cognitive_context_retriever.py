"""
CEREBRUM
Recuperación de contexto cognitivo relevante.

v0.0.8 Alpha - Memory Bridge
"""

from .cognitive_context_selector import CognitiveContextSelector
from .cognitive_engine import CognitiveEngine
from .memory_bridge import MemoryBridge


class CognitiveContextRetriever:
    """
    Recupera información relevante del Cognitive Core
    y del sistema de memoria.
    """

    def __init__(
        self,
        cognitive_engine: CognitiveEngine,
        selector: CognitiveContextSelector | None = None,
        memory_bridge: MemoryBridge | None = None,
        limite: int = 10
    ):
        self.cognitive_engine = cognitive_engine

        self.selector = (
            selector
            or CognitiveContextSelector()
        )

        self.memory_bridge = (
            memory_bridge
            or MemoryBridge()
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
        # MEMORIA PERSISTENTE
        # -------------------------

        if (
            seleccion.get(
                "memoria",
                False
            )
            and tema
        ):
            resultado["memoria"] = (
                self.memory_bridge.contexto_para(
                    tema,
                    limite=self.limite
                )
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
                conversacion = (
                    conversacion.strip()
                )

                resultado["conversacion"] = (
                    conversacion
                )

                if conversacion:
                    memoria_conversacional = (
                        self._recuperar_memoria_conversacional(
                            conversacion,
                            tema
                        )
                    )

                    resultado["memoria"].extend(
                        memoria_conversacional
                    )

                    resultado["memoria"] = list(
                        dict.fromkeys(
                            resultado["memoria"]
                        )
                    )[-self.limite:]

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

    def _recuperar_memoria_conversacional(
        self,
        conversacion: str,
        tema: str
    ) -> list[str]:
        """
        Recupera fragmentos relevantes de la conversación actual.
        """

        lineas = [
            linea.strip()
            for linea in conversacion.splitlines()
            if linea.strip()
        ]

        if not lineas:
            return []

        if not tema:
            return lineas[-self.limite:]

        palabras_tema = {
            palabra.lower().strip(
                ".,;:!?¿¡()[]{}\"'"
            )
            for palabra in tema.split()
            if palabra.strip(
                ".,;:!?¿¡()[]{}\"'"
            )
        }

        relevantes = []

        for linea in lineas:
            palabras_linea = {
                palabra.lower().strip(
                    ".,;:!?¿¡()[]{}\"'"
                )
                for palabra in linea.split()
            }

            if palabras_tema.intersection(
                palabras_linea
            ):
                relevantes.append(
                    linea
                )

        if relevantes:
            return relevantes[-self.limite:]

        return lineas[-self.limite:]