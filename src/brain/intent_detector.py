"""
CEREBRUM
Detector heurístico de intención.

v0.0.7 Alpha - Cognitive Interaction
"""

from .intent import Intent


class IntentDetector:
    """Detecta intenciones básicas mediante reglas."""

    PATRONES_ACCION = {
        "explicar": (
            "explica",
            "explícame",
            "explicame",
            "explícame",
            "qué es",
            "que es",
        ),
        "buscar": (
            "busca",
            "buscar",
            "encuentra",
            "encontrar",
            "investiga",
            "investigar",
        ),
        "crear": (
            "crea",
            "crear",
            "genera",
            "generar",
            "haz",
            "hacer",
        ),
        "resolver": (
            "resuelve",
            "resolver",
            "soluciona",
            "solucionar",
            "calcula",
            "calcular",
        ),
        "recordar": (
            "recuerda",
            "recordar",
            "qué recuerdas",
            "que recuerdas",
            "qué sabes de mí",
            "que sabes de mi",
        ),
    }

    PALABRAS_PREGUNTA = (
        "qué",
        "que",
        "cómo",
        "como",
        "cuándo",
        "cuando",
        "dónde",
        "donde",
        "por qué",
        "porque",
        "quién",
        "quien",
        "cuál",
        "cual",
    )

    PALABRAS_COMANDO = (
        "haz",
        "hacer",
        "crea",
        "crear",
        "dame",
        "genera",
        "generar",
        "ejecuta",
        "ejecutar",
        "resuelve",
        "resolver",
        "busca",
        "buscar",
    )

    def detectar(
        self,
        mensaje: str
    ) -> Intent:
        """Detecta una intención a partir del texto."""

        if not isinstance(mensaje, str):
            return Intent(
                tipo="desconocido",
                accion="ninguna",
                confianza=0.0
            )

        mensaje = mensaje.strip()

        if not mensaje:
            return Intent(
                tipo="desconocido",
                accion="ninguna",
                confianza=0.0
            )

        texto = self._normalizar(
            mensaje
        )

        tipo = self._detectar_tipo(
            texto
        )

        accion = self._detectar_accion(
            texto
        )

        tema = self._detectar_tema(
            texto,
            accion
        )

        confianza = self._calcular_confianza(
            tipo=tipo,
            accion=accion,
            tema=tema
        )

        return Intent(
            tipo=tipo,
            accion=accion,
            tema=tema,
            confianza=confianza
        )

    @staticmethod
    def _normalizar(
        texto: str
    ) -> str:
        """Normaliza espacios y formato básico."""

        return " ".join(
            texto.lower().split()
        )

    def _detectar_tipo(
        self,
        texto: str
    ) -> str:
        """Detecta el tipo general de entrada."""

        if "?" in texto:
            return "pregunta"

        if texto.startswith("¿"):
            return "pregunta"

        if any(
            texto.startswith(palabra)
            for palabra in self.PALABRAS_PREGUNTA
        ):
            return "pregunta"

        if any(
            texto.startswith(palabra)
            for palabra in self.PALABRAS_COMANDO
        ):
            return "comando"

        return "afirmacion"

    def _detectar_accion(
        self,
        texto: str
    ) -> str:
        """Detecta la acción más relevante."""

        for accion, patrones in self.PATRONES_ACCION.items():
            for patron in patrones:
                if patron in texto:
                    return accion

        return "ninguna"

    def _detectar_tema(
        self,
        texto: str,
        accion: str
    ) -> str:
        """Obtiene una aproximación del tema."""

        texto = texto.replace(
            "¿",
            ""
        ).replace(
            "?",
            ""
        )

        palabras = texto.split()

        palabras_eliminadas = {
            "qué",
            "que",
            "cómo",
            "como",
            "cuándo",
            "cuando",
            "dónde",
            "donde",
            "por",
            "quién",
            "quien",
            "cuál",
            "cual",
            "es",
            "son",
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
            "de",
            "del",
            "sobre",
            "acerca",
            "acerca",
            "me",
            "mí",
            "mi",
            "puedes",
            "podrías",
            "podrias",
            "por",
            "favor",
            "explica",
            "explícame",
            "explicame",
            "busca",
            "buscar",
            "encuentra",
            "encontrar",
            "crea",
            "crear",
            "genera",
            "generar",
            "haz",
            "hacer",
            "resuelve",
            "resolver",
            "soluciona",
            "solucionar",
            "recuerda",
            "recordar",
        }

        palabras_tema = [
            palabra
            for palabra in palabras
            if palabra not in palabras_eliminadas
        ]

        return " ".join(
            palabras_tema[:5]
        )

    @staticmethod
    def _calcular_confianza(
        tipo: str,
        accion: str,
        tema: str
    ) -> float:
        """Calcula una confianza heurística."""

        confianza = 0.25

        if tipo != "desconocido":
            confianza += 0.25

        if accion != "ninguna":
            confianza += 0.30

        if tema:
            confianza += 0.20

        return min(
            1.0,
            confianza
        )