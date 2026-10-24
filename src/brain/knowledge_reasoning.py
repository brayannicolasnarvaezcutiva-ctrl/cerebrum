"""
CEREBRUM
Integración entre conocimiento estructurado y razonamiento.

v0.0.9 Alpha — preparación hacia v0.1.0
"""

from .conflict_detector import ConflictDetector
from .explained_knowledge_inference import ExplainedKnowledgeInference
from .knowledge import KnowledgeBase
from .knowledge_reasoner import KnowledgeReasoner
from .reasoning import ReasoningEngine
from .reasoning_result import ReasoningResult
from .reasoning_validator import ReasoningValidator


class KnowledgeReasoning:
    """Integra conocimiento estructurado con el motor de razonamiento."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        reasoning_engine: ReasoningEngine | None = None,
        inference: ExplainedKnowledgeInference | None = None,
        validator: ReasoningValidator | None = None,
        conflict_detector: ConflictDetector | None = None
    ):
        self.knowledge_base = knowledge_base
        self.knowledge_reasoner = KnowledgeReasoner(knowledge_base)
        self.reasoning_engine = reasoning_engine or ReasoningEngine()
        self.inference = inference or ExplainedKnowledgeInference(
            knowledge_base
        )
        self.validator = validator or ReasoningValidator()
        self.conflict_detector = conflict_detector or ConflictDetector(
            knowledge_base
        )
        self.last_result = None

    def consultar(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> list:
        """Consulta hechos almacenados en la base de conocimiento."""

        return self.knowledge_reasoner.consultar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

    def generar_evidencia(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> list[str]:
        """Obtiene los hechos como texto de evidencia."""

        return self.knowledge_reasoner.generar_evidencia(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

    def razonar_sobre(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> ReasoningResult:
        """
        Obtiene conocimiento estructurado y lo entrega
        al motor de razonamiento existente.
        """

        evidencia = self.generar_evidencia(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

        if not evidencia:
            return ReasoningResult(
                conclusion="No hay conocimiento suficiente.",
                evidencia=[],
                confianza=0.0
            )

        texto = " ".join(evidencia)

        # La API real de ReasoningEngine v0.0.4 utiliza analizar().
        resultado = self.reasoning_engine.analizar(texto)

        return resultado

    def razonar(self) -> ReasoningResult:
        """Ejecuta el razonamiento estructurado sobre la base actual.

        El motor textual se conserva en ``razonar_sobre`` para los
        consumidores históricos. Esta operación es la ruta canónica del
        Cognitive Core: infiere, valida, agrega confianza y reporta
        conflictos en un único ``ReasoningResult``.
        """

        explicaciones = self.inference.inferir_todo()
        validaciones = []
        conflictos = []

        for explicacion in explicaciones:
            validacion = self.validator.validar(
                conclusion=explicacion.conclusion,
                evidencias=explicacion.evidencias
            )
            validaciones.append(validacion)

            for conflicto in self.conflict_detector.detectar(
                explicacion.conclusion,
                ignorar=explicacion.evidencias
            ):
                if conflicto not in conflictos:
                    conflictos.append(conflicto)

        confianzas = [
            validacion["confianza"]
            for validacion in validaciones
            if validacion["valida"]
        ]
        confianza = (
            sum(confianzas) / len(confianzas)
            if confianzas
            else 0.0
        )
        valido = bool(explicaciones) and all(
            validacion["valida"]
            for validacion in validaciones
        ) and not conflictos

        resultado = ReasoningResult(
            conclusiones=explicaciones,
            confianza=confianza,
            valido=valido,
            tiene_conflicto=bool(conflictos),
            conflictos=conflictos
        )

        self.last_result = resultado

        return resultado

    def obtener_ultimo_resultado(self) -> ReasoningResult | None:
        """Devuelve el último resultado estructurado generado."""

        return self.last_result
