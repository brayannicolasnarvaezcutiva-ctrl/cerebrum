"""
CEREBRUM
Coordinador del núcleo cognitivo con trazabilidad e intención.

v0.0.7 Alpha - Cognitive Interaction
"""

from .cognitive_result import CognitiveResult
from .explained_knowledge_inference import ExplainedKnowledgeInference
from .inference_explanation import InferenceExplanationBuilder
from .intent_detector import IntentDetector
from .knowledge import KnowledgeBase
from .knowledge_extractor import KnowledgeExtractor
from .knowledge_reasoner import KnowledgeReasoner
from .knowledge_trace import KnowledgeTrace


class CognitiveEngine:
    """Coordina conocimiento, inferencia, razonamiento, trazabilidad e intención."""

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

        self.intent_detector = IntentDetector()

        self.ultima_intencion = None

    def aprender(self, texto: str):
        """Extrae y almacena conocimiento desde una frase."""

        hecho = self.extractor.extraer(texto)

        if hecho is not None:
            explicacion = self.explainer.explicar_aprendizaje(
                hecho
            )

            self.trace.registrar(
                explicacion
            )

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
            self.trace.registrar(
                explicacion
            )

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

    def detectar_intencion(
        self,
        texto: str
    ):
        """Detecta y guarda la intención de una entrada."""

        intencion = self.intent_detector.detectar(
            texto
        )

        self.ultima_intencion = intencion

        return intencion

    def obtener_ultima_intencion(self):
        """Devuelve la última intención detectada."""

        return self.ultima_intencion

    def procesar(
        self,
        texto: str
    ) -> CognitiveResult:
        """
        Ejecuta una operación cognitiva completa.

        Flujo:

            entrada
              ↓
            detección de intención
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

        intencion = self.detectar_intencion(
            texto
        )

        hechos_aprendidos = []

        hecho = self.aprender(
            texto
        )

        if hecho is not None:
            hechos_aprendidos.append(
                hecho
            )

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

        evidencia = list(
            dict.fromkeys(evidencia)
        )

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
            confianza=confianza,
            intencion=intencion
        )