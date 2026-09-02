"""
CEREBRUM
Motor de razonamiento.

v0.0.4 Alpha - Reasoning Core
"""

from dataclasses import dataclass

from .inference import InferenceEngine


@dataclass
class ReasoningResult:
    """Resultado de un proceso de razonamiento."""

    conclusion: str
    evidencia: list[str]
    confianza: float


class ReasoningEngine:
    """Motor de razonamiento de CEREBRUM."""

    def __init__(self):
        self.last_result = None
        self.inference = InferenceEngine()

    def analizar(self, texto: str, recuerdos=None):
        """Analiza texto y utiliza recuerdos como evidencia."""

        texto = texto.strip().lower()

        if not texto:
            resultado = ReasoningResult(
                conclusion="No hay información suficiente.",
                evidencia=[],
                confianza=0.0
            )

            self.last_result = resultado
            return resultado

        evidencia = []
        premisas = []

        # --------------------------------------------
        # Entrada actual
        # --------------------------------------------

        premisas.append(texto)

        palabras = texto.split()

        if len(palabras) >= 3:
            evidencia.append(
                f"La entrada contiene {len(palabras)} palabras."
            )

        if "porque" in texto:
            evidencia.append(
                "Se detectó una posible justificación."
            )

        if "pero" in texto:
            evidencia.append(
                "Se detectó una posible contradicción."
            )

        if texto.startswith("si "):
            evidencia.append(
                "Se detectó una posible regla condicional."
            )

        # --------------------------------------------
        # Memoria
        # --------------------------------------------

        if recuerdos:
            for recuerdo in recuerdos:

                contenido = recuerdo.get(
                    "contenido",
                    ""
                )

                tipo = recuerdo.get(
                    "tipo",
                    "general"
                )

                importancia = recuerdo.get(
                    "importancia",
                    1
                )

                if contenido:
                    premisas.append(
                        contenido.lower()
                    )

                    evidencia.append(
                        "Memoria utilizada como evidencia: "
                        f"{contenido} "
                        f"(tipo: {tipo}, "
                        f"importancia: {importancia})."
                    )

        # --------------------------------------------
        # Inferencia
        # --------------------------------------------

        inferencia = self.inference.inferir(
            premisas
        )

        evidencia.append(
            "Tipo de inferencia: "
            f"{inferencia['tipo']}."
        )

        confianza = inferencia["confianza"]

        if recuerdos:
            confianza += 0.05

        confianza = min(
            confianza,
            1.0
        )

        resultado = ReasoningResult(
            conclusion=inferencia["conclusion"],
            evidencia=evidencia,
            confianza=confianza
        )

        self.last_result = resultado

        return resultado

    def comparar(
        self,
        opcion_a: str,
        opcion_b: str,
        recuerdos=None
    ):
        """Compara dos opciones."""

        opcion_a = opcion_a.strip()
        opcion_b = opcion_b.strip()

        if not opcion_a or not opcion_b:
            resultado = ReasoningResult(
                conclusion=(
                    "No hay dos opciones válidas "
                    "para comparar."
                ),
                evidencia=[],
                confianza=0.0
            )

            self.last_result = resultado
            return resultado

        evidencia = [
            f"Opción A: {opcion_a}",
            f"Opción B: {opcion_b}"
        ]

        if recuerdos:
            for recuerdo in recuerdos:
                evidencia.append(
                    "Memoria relacionada: "
                    f"{recuerdo.get('contenido', '')}."
                )

        premisas = [
            f"opción A: {opcion_a}",
            f"opción B: {opcion_b}"
        ]

        inferencia = self.inference.inferir(
            premisas
        )

        evidencia.append(
            "Tipo de inferencia: "
            f"{inferencia['tipo']}."
        )

        resultado = ReasoningResult(
            conclusion=inferencia["conclusion"],
            evidencia=evidencia,
            confianza=inferencia["confianza"]
        )

        self.last_result = resultado

        return resultado

    def obtener_ultimo_resultado(self):
        """Devuelve el último resultado."""

        return self.last_result