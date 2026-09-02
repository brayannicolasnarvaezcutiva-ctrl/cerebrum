"""
CEREBRUM
Coordinador del núcleo cognitivo con trazabilidad.

v0.0.5 Alpha - Cognitive Core
"""

from .cognitive_result import CognitiveResult
from .explained_knowledge_inference import ExplainedKnowledgeInference
from .inference_explanation import InferenceExplanationBuilder
from .knowledge import KnowledgeBase
from .knowledge_extractor import KnowledgeExtractor
from .knowledge_reasoner import KnowledgeReasoner
from .knowledge_trace import KnowledgeTrace


class CognitiveEngine:
    """Coordina conocimiento, inferencia, razonamiento y trazabilidad."""

    def __init__(self):
        self.knowledge_base = KnowledgeBase()

        self.extractor = KnowledgeExtractor(
            self.knowledge_base
        )

        self.reasoner = KnowledgeReasoner(
            self.knowledge_base
        )

        self.inference = ExplainedKnowledgeInference(
            self.knowledge_base
        )

        self.trace = KnowledgeTrace()

        self.explainer = InferenceExplanationBuilder()

    def aprender(self, texto: str):
        """Extrae y almacena conocimiento desde una frase."""

        hecho = self.extractor.extraer(texto)

        if hecho is not None:
            explicacion = self.explainer.explicar_aprendizaje(
                hecho
            )

            self.trace.registrar(explicacion)

        return hecho

    def consultar(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ):
        """Consulta conocimiento existente."""

        return self.reasoner.consultar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

    def inferir(self):
        """Genera nuevas conclusiones y registra su trazabilidad."""

        explicaciones = self.inference.inferir_todo()

        for explicacion in explicaciones:
            self.trace.registrar(explicacion)

        return explicaciones

    def explicar_inferencias(self):
        """Devuelve las inferencias en formato legible."""

        explicaciones = self.inferir()

        return self.inference.formatear_resultados(
            explicaciones
        )

    def obtener_traza(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ):
        """Consulta la procedencia de un conocimiento."""

        return self.trace.buscar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

    def procesar(self, texto: str) -> CognitiveResult:
        """
        Ejecuta una operación cognitiva completa.

        Flujo:

            entrada
              ↓
            aprendizaje
              ↓
            inferencia
              ↓
            evidencia
              ↓
            CognitiveResult
        """

        if not isinstance(texto, str):
            return CognitiveResult(
                entrada="",
                confianza=0.0
            )

        texto = texto.strip()

        if not texto:
            return CognitiveResult(
                entrada="",
                confianza=0.0
            )

        hechos_aprendidos = []

        hecho = self.aprender(texto)

        if hecho is not None:
            hechos_aprendidos.append(hecho)

        inferencias = self.inferir()

        evidencia = []

        for hecho in hechos_aprendidos:
            evidencia.append(
                f"{hecho.sujeto} "
                f"{hecho.relacion} "
                f"{hecho.objeto}"
            )

        for explicacion in inferencias:
            for hecho in explicacion.evidencias:
                evidencia.append(
                    f"{hecho.sujeto} "
                    f"{hecho.relacion} "
                    f"{hecho.objeto}"
                )

        evidencia = list(dict.fromkeys(evidencia))

        if hechos_aprendidos:
            confianza = max(
                hecho.confianza
                for hecho in hechos_aprendidos
            )

        elif inferencias:
            confianza = max(
                explicacion.conclusion.confianza
                for explicacion in inferencias
            )

        else:
            confianza = 0.0

        return CognitiveResult(
            entrada=texto,
            hechos_aprendidos=hechos_aprendidos,
            inferencias=inferencias,
            evidencia=evidencia,
            confianza=confianza
        )