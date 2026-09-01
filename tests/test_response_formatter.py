import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.reasoning import ReasoningResult
from brain.reasoning_handler import ReasoningRequestResult
from brain.response_formatter import ResponseFormatter


class TestResponseFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = ResponseFormatter()

    def test_formatea_resultado_de_razonamiento(self):
        resultado = ReasoningResult(
            conclusion="apruebo",
            evidencia=["Premisa válida.", "Tipo de inferencia: modus_ponens."],
            confianza=0.95
        )

        texto = self.formatter.formatear_razonamiento(resultado)

        self.assertEqual(
            texto,
            "Conclusión: apruebo\n"
            "Evidencia:\n"
            "- Premisa válida.\n"
            "- Tipo de inferencia: modus_ponens.\n"
            "Confianza: 95%"
        )

    def test_formatea_mensaje_de_solicitud_de_razonamiento(self):
        solicitud = ReasoningRequestResult(
            mensaje="No hay nada que analizar."
        )

        self.assertEqual(
            self.formatter.formatear_solicitud_razonamiento(solicitud),
            "No hay nada que analizar."
        )

    def test_formatea_recuerdos_y_relaciones(self):
        recuerdo = {
            "id": 1,
            "contenido": "aprendo python",
            "tipo": "objetivo",
            "importancia": 4
        }
        relacionado = {
            "id": 2,
            "contenido": "python para automatización",
            "tipo": "proyecto",
            "importancia": 5
        }

        self.assertEqual(
            self.formatter.formatear_recuerdos([recuerdo]),
            "[1] aprendo python (tipo: objetivo, importancia: 4)"
        )
        self.assertEqual(
            self.formatter.formatear_recuerdos([]),
            "No tengo recuerdos registrados."
        )
        self.assertEqual(
            self.formatter.formatear_relacionados(
                recuerdo,
                [relacionado]
            ),
            "- python para automatización (tipo: proyecto)"
        )

    def test_formatea_respuestas_de_memoria_y_contexto(self):
        recuerdo = {"contenido": "python"}

        self.assertEqual(
            self.formatter.formatear_recuerdo(recuerdo),
            "Recuerdo: python"
        )
        self.assertEqual(
            self.formatter.formatear_recuerdo_eliminado(recuerdo),
            "Recuerdo eliminado: python"
        )
        self.assertEqual(
            self.formatter.formatear_contexto(["hola", "contexto"]),
            "- hola\n- contexto"
        )
        self.assertEqual(
            self.formatter.formatear_tema("python"),
            "El tema reciente parece ser: python"
        )


if __name__ == "__main__":
    unittest.main()
