"""
CEREBRUM
Motor de inferencia lógica básica.

v0.0.4 Alpha - Reasoning Core
"""

from .logic import LogicAnalyzer


class InferenceEngine:
    """Realiza inferencias simples a partir de premisas."""

    def __init__(self):
        self.last_inference = None
        self.logic = LogicAnalyzer()

    def _limpiar(self, texto):
        """Normaliza un texto."""

        return texto.strip().lower()

    def _normalizar_hecho(self, texto):
        """Elimina palabras de relleno."""

        texto = self._limpiar(texto)

        prefijos = [
            "que ",
            "el hecho de que ",
            "el hecho que "
        ]

        for prefijo in prefijos:
            if texto.startswith(prefijo):
                texto = texto[len(prefijo):]

        return texto.strip()

    def _buscar_regla(self, premisas):
        """Busca una regla 'si X entonces Y'."""

        for premisa in premisas:
            texto = self._limpiar(premisa)

            if (
                texto.startswith("si ")
                and " entonces " in texto
            ):
                partes = texto[3:].split(
                    " entonces ",
                    1
                )

                if len(partes) == 2:
                    condicion = partes[0].strip()
                    consecuencia = partes[1].strip()

                    return condicion, consecuencia

        return None

    def _hay_hecho(self, hecho, premisas):
        """Comprueba si existe el hecho."""

        hecho = self._normalizar_hecho(
            hecho
        )

        for premisa in premisas:
            premisa_normalizada = (
                self._normalizar_hecho(
                    premisa
                )
            )

            if premisa_normalizada == hecho:
                return True

        return False

    def _separar_justificacion(self, texto):
        """Separa una conclusión de una justificación."""

        texto = self._limpiar(texto)

        if " porque " not in texto:
            return texto, None

        partes = texto.split(
            " porque ",
            1
        )

        conclusion = partes[0].strip()
        justificacion = partes[1].strip()

        return conclusion, justificacion

    def inferir(self, premisas):
        """Realiza una inferencia lógica."""

        if not premisas:
            resultado = {
                "conclusion": "No hay premisas suficientes.",
                "premisas": [],
                "confianza": 0.0,
                "tipo": "sin_datos"
            }

            self.last_inference = resultado
            return resultado

        premisas = [
            self._limpiar(premisa)
            for premisa in premisas
            if premisa
            and self._limpiar(premisa)
        ]

        if not premisas:
            resultado = {
                "conclusion": "No hay premisas válidas.",
                "premisas": [],
                "confianza": 0.0,
                "tipo": "sin_datos"
            }

            self.last_inference = resultado
            return resultado

        # --------------------------------------------
        # Validar consistencia
        # --------------------------------------------

        validacion = self.logic.validar_premisas(
            premisas
        )

        if not validacion["consistentes"]:
            resultado = {
                "conclusion": (
                    "No puedo realizar una inferencia "
                    "con premisas contradictorias."
                ),
                "premisas": premisas,
                "confianza": 0.0,
                "tipo": "contradiccion",
                "contradicciones": (
                    validacion["contradicciones"]
                )
            }

            self.last_inference = resultado
            return resultado

        # --------------------------------------------
        # Separar justificaciones
        # --------------------------------------------

        premisas_procesadas = []

        for premisa in premisas:
            conclusion, justificacion = (
                self._separar_justificacion(
                    premisa
                )
            )

            premisas_procesadas.append(
                conclusion
            )

            if justificacion:
                premisas_procesadas.append(
                    justificacion
                )

        # --------------------------------------------
        # Buscar regla
        # --------------------------------------------

        regla = self._buscar_regla(
            premisas_procesadas
        )

        if regla:
            condicion, consecuencia = regla

            if self._hay_hecho(
                condicion,
                premisas_procesadas
            ):
                resultado = {
                    "conclusion": consecuencia,
                    "premisas": premisas_procesadas,
                    "confianza": 0.95,
                    "tipo": "modus_ponens",
                    "contradicciones": []
                }

                self.last_inference = resultado
                return resultado

            resultado = {
                "conclusion": (
                    f"No puedo concluir '{consecuencia}' "
                    f"porque no se cumple la condición "
                    f"'{condicion}'."
                ),
                "premisas": premisas_procesadas,
                "confianza": 0.7,
                "tipo": "regla_no_activada",
                "contradicciones": []
            }

            self.last_inference = resultado
            return resultado

        # --------------------------------------------
        # Varias premisas
        # --------------------------------------------

        if len(premisas_procesadas) >= 2:
            resultado = {
                "conclusion": (
                    "Existen varias premisas que pueden "
                    "utilizarse para construir una inferencia."
                ),
                "premisas": premisas_procesadas,
                "confianza": 0.6,
                "tipo": "multiples_premisas",
                "contradicciones": []
            }

            self.last_inference = resultado
            return resultado

        # --------------------------------------------
        # Una sola premisa
        # --------------------------------------------

        resultado = {
            "conclusion": (
                f"La premisa '{premisas_procesadas[0]}' "
                "puede utilizarse como punto de partida."
            ),
            "premisas": premisas_procesadas,
            "confianza": 0.4,
            "tipo": "premisa_simple",
            "contradicciones": []
        }

        self.last_inference = resultado
        return resultado

    def obtener_ultima_inferencia(self):
        """Devuelve la última inferencia."""

        return self.last_inference