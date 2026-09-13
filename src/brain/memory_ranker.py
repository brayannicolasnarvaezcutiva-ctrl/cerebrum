"""
CEREBRUM
Ranking de recuerdos por relevancia.

v0.0.8 Alpha - Memory Bridge
"""

from datetime import datetime


class MemoryRanker:
    """
    Ordena recuerdos según relevancia temática,
    importancia y recencia.
    """

    def __init__(
        self,
        peso_relevancia: float = 0.6,
        peso_importancia: float = 0.3,
        peso_recencia: float = 0.1
    ):
        self.peso_relevancia = float(
            peso_relevancia
        )

        self.peso_importancia = float(
            peso_importancia
        )

        self.peso_recencia = float(
            peso_recencia
        )

    def ordenar(
        self,
        recuerdos: list[dict],
        texto: str
    ) -> list[dict]:
        """Ordena recuerdos por puntuación."""

        if not isinstance(
            recuerdos,
            list
        ):
            return []

        palabras = self._palabras(
            texto
        )

        puntuados = []

        for recuerdo in recuerdos:

            if not isinstance(
                recuerdo,
                dict
            ):
                continue

            contenido = recuerdo.get(
                "contenido",
                ""
            )

            relevancia = self._relevancia(
                contenido,
                palabras
            )

            importancia = self._importancia(
                recuerdo
            )

            recencia = self._recencia(
                recuerdo
            )

            puntuacion = (
                relevancia
                * self.peso_relevancia
                + importancia
                * self.peso_importancia
                + recencia
                * self.peso_recencia
            )

            puntuados.append(
                (
                    puntuacion,
                    recuerdo
                )
            )

        puntuados.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            recuerdo
            for _, recuerdo
            in puntuados
        ]

    def puntuar(
        self,
        recuerdo: dict,
        texto: str
    ) -> float:
        """Devuelve la puntuación de un recuerdo."""

        if not isinstance(
            recuerdo,
            dict
        ):
            return 0.0

        palabras = self._palabras(
            texto
        )

        relevancia = self._relevancia(
            recuerdo.get(
                "contenido",
                ""
            ),
            palabras
        )

        importancia = self._importancia(
            recuerdo
        )

        recencia = self._recencia(
            recuerdo
        )

        return (
            relevancia
            * self.peso_relevancia
            + importancia
            * self.peso_importancia
            + recencia
            * self.peso_recencia
        )

    @staticmethod
    def _palabras(
        texto: str
    ) -> set[str]:
        """Extrae palabras útiles."""

        if not isinstance(
            texto,
            str
        ):
            return set()

        return {
            palabra.strip(
                ".,!?¿¡:;()[]{}\"'"
            )
            for palabra in texto.lower().split()
            if len(
                palabra.strip(
                    ".,!?¿¡:;()[]{}\"'"
                )
            ) >= 4
        }

    @staticmethod
    def _relevancia(
        contenido: str,
        palabras: set[str]
    ) -> float:
        """Calcula una relevancia entre 0 y 1."""

        if not contenido or not palabras:
            return 0.0

        palabras_contenido = {
            palabra.strip(
                ".,!?¿¡:;()[]{}\"'"
            )
            for palabra in contenido.lower().split()
            if palabra.strip(
                ".,!?¿¡:;()[]{}\"'"
            )
        }

        coincidencias = (
            palabras
            & palabras_contenido
        )

        return min(
            1.0,
            len(coincidencias)
            / len(palabras)
        )

    @staticmethod
    def _importancia(
        recuerdo: dict
    ) -> float:
        """Normaliza la importancia a 0–1."""

        importancia = max(
            1,
            min(
                5,
                int(
                    recuerdo.get(
                        "importancia",
                        1
                    )
                )
            )
        )

        return importancia / 5.0

    @staticmethod
    def _recencia(
        recuerdo: dict
    ) -> float:
        """Calcula una recencia aproximada."""

        fecha = recuerdo.get(
            "fecha"
        )

        if not fecha:
            return 0.0

        try:
            fecha_recuerdo = datetime.fromisoformat(
                fecha
            )
        except (
            TypeError,
            ValueError
        ):
            return 0.0

        ahora = datetime.now(
            fecha_recuerdo.tzinfo
        ) if fecha_recuerdo.tzinfo else datetime.now()

        dias = (
            ahora - fecha_recuerdo
        ).total_seconds() / 86400

        if dias < 0:
            dias = 0

        return 1.0 / (
            1.0 + dias / 30.0
        )