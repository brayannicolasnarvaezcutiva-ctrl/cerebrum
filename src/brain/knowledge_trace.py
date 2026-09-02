"""
CEREBRUM
Registro de trazabilidad del conocimiento.

v0.0.5 Alpha - Cognitive Core
"""

from .inference_explanation import InferenceExplanation
from .knowledge import KnowledgeFact


class KnowledgeTrace:
    """Conserva el origen y las explicaciones del conocimiento."""

    def __init__(self):
        self.registros: list[InferenceExplanation] = []

    def registrar(
        self,
        explicacion: InferenceExplanation
    ) -> InferenceExplanation:
        """Registra una explicación evitando duplicados."""

        if explicacion is None:
            return None

        for registro in self.registros:
            if (
                registro.conclusion == explicacion.conclusion
                and registro.tipo == explicacion.tipo
                and registro.regla == explicacion.regla
                and registro.evidencias == explicacion.evidencias
            ):
                return registro

        self.registros.append(explicacion)

        return explicacion

    def buscar(
        self,
        sujeto: str | None = None,
        relacion: str | None = None,
        objeto: str | None = None
    ) -> list[InferenceExplanation]:
        """Busca explicaciones asociadas a una conclusión."""

        sujeto = sujeto.strip().lower() if sujeto else None
        relacion = relacion.strip().lower() if relacion else None
        objeto = objeto.strip().lower() if objeto else None

        resultados = []

        for registro in self.registros:
            fact = registro.conclusion

            if sujeto is not None and fact.sujeto != sujeto:
                continue

            if relacion is not None and fact.relacion != relacion:
                continue

            if objeto is not None and fact.objeto != objeto:
                continue

            resultados.append(registro)

        return list(resultados)

    def obtener_para(
        self,
        hecho: KnowledgeFact
    ) -> list[InferenceExplanation]:
        """Obtiene toda la trazabilidad de un hecho."""

        if hecho is None:
            return []

        return self.buscar(
            sujeto=hecho.sujeto,
            relacion=hecho.relacion,
            objeto=hecho.objeto
        )

    def obtener_todo(self) -> list[InferenceExplanation]:
        """Devuelve todos los registros."""

        return list(self.registros)

    def limpiar(self):
        """Elimina toda la trazabilidad."""

        self.registros.clear()