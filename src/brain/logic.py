"""
CEREBRUM
Analizador lógico básico.

v0.0.4 Alpha - Reasoning Core
"""


class LogicAnalyzer:
    """Analiza hechos, reglas y contradicciones simples."""

    NEGACIONES = (
        "no ",
        "nunca ",
        "ya no ",
    )

    def __init__(self):
        self.last_analysis = None

    def _limpiar(self, texto):
        """Normaliza el texto."""

        return texto.strip().lower()

    def _es_negacion(self, texto):
        """Comprueba si una frase contiene una negación simple."""

        texto = self._limpiar(texto)

        return texto.startswith(self.NEGACIONES)

    def _quitar_negacion(self, texto):
        """Elimina la negación inicial."""

        texto = self._limpiar(texto)

        for prefijo in self.NEGACIONES:
            if texto.startswith(prefijo):
                return texto[len(prefijo):].strip()

        return texto

    def _buscar_hechos(self, premisas):
        """Separa hechos positivos y negativos."""

        positivos = []
        negativos = []

        for premisa in premisas:
            texto = self._limpiar(premisa)

            if not texto:
                continue

            if self._es_negacion(texto):
                negativos.append(
                    self._quitar_negacion(texto)
                )
            else:
                positivos.append(texto)

        return positivos, negativos

    def detectar_contradicciones(self, premisas):
        """
        Busca pares como:

        estudio
        no estudio
        """

        positivos, negativos = self._buscar_hechos(
            premisas
        )

        contradicciones = []

        for hecho in positivos:
            if hecho in negativos:
                contradicciones.append(
                    f"Contradicción detectada: "
                    f"'{hecho}' y 'no {hecho}'."
                )

        return contradicciones

    def validar_premisas(self, premisas):
        """Evalúa la consistencia de las premisas."""

        if not premisas:
            resultado = {
                "validas": False,
                "consistentes": False,
                "contradicciones": [],
                "cantidad": 0
            }

            self.last_analysis = resultado
            return resultado

        contradicciones = (
            self.detectar_contradicciones(
                premisas
            )
        )

        resultado = {
            "validas": True,
            "consistentes": not bool(
                contradicciones
            ),
            "contradicciones": contradicciones,
            "cantidad": len(premisas)
        }

        self.last_analysis = resultado

        return resultado

    def obtener_ultimo_analisis(self):
        """Devuelve el último análisis lógico."""

        return self.last_analysis