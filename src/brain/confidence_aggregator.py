"""
CEREBRUM
Agregador de confianza para razonamiento.

v0.0.9 Alpha - Reasoning Upgrade
"""


class ConfidenceAggregator:
    """
    Combina diferentes señales de confianza en una
    puntuación única de razonamiento.
    """

    def __init__(
        self,
        peso_conclusion: float = 0.4,
        peso_evidencia: float = 0.6
    ):
        self.peso_conclusion = float(
            peso_conclusion
        )

        self.peso_evidencia = float(
            peso_evidencia
        )

    def calcular(
        self,
        confianza_conclusion: float,
        confianzas_evidencia: list[float]
    ) -> float:
        """
        Calcula una confianza agregada entre 0 y 1.
        """

        conclusion = self._normalizar(
            confianza_conclusion
        )

        if not confianzas_evidencia:
            return conclusion * self.peso_conclusion

        evidencias = [
            self._normalizar(confianza)
            for confianza in confianzas_evidencia
        ]

        promedio_evidencia = (
            sum(evidencias)
            / len(evidencias)
        )

        resultado = (
            conclusion * self.peso_conclusion
            + promedio_evidencia
            * self.peso_evidencia
        )

        return self._normalizar(
            resultado
        )

    def desde_recuerdos(
        self,
        conclusion,
        evidencias
    ) -> float:
        """
        Calcula confianza directamente desde
        objetos que contienen el atributo 'confianza'.
        """

        if conclusion is None:
            return 0.0

        confianza_conclusion = getattr(
            conclusion,
            "confianza",
            0.0
        )

        confianzas_evidencia = [
            getattr(
                evidencia,
                "confianza",
                0.0
            )
            for evidencia in (
                evidencias
                if isinstance(
                    evidencias,
                    list
                )
                else []
            )
        ]

        return self.calcular(
            confianza_conclusion,
            confianzas_evidencia
        )

    @staticmethod
    def _normalizar(
        valor
    ) -> float:
        """
        Limita una confianza al rango 0–1.
        """

        try:
            valor = float(valor)
        except (
            TypeError,
            ValueError
        ):
            return 0.0

        return max(
            0.0,
            min(
                1.0,
                valor
            )
        )