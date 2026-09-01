import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.reasoning import ReasoningEngine


class TestReasoningEngine(unittest.TestCase):

    def setUp(self):
        self.reasoning = ReasoningEngine()

    def test_analizar_texto_vacio(self):
        resultado = self.reasoning.analizar("   ")

        self.assertEqual(resultado.conclusion, "No hay información suficiente.")
        self.assertEqual(resultado.evidencia, [])
        self.assertEqual(resultado.confianza, 0.0)

    def test_analizar_usa_recuerdos_como_evidencia(self):
        resultado = self.reasoning.analizar(
            "si estudio entonces apruebo",
            recuerdos=[
                {
                    "contenido": "estudio",
                    "tipo": "objetivo",
                    "importancia": 4
                }
            ]
        )

        self.assertEqual(resultado.conclusion, "apruebo")
        self.assertEqual(resultado.confianza, 1.0)
        self.assertIn(
            "Memoria utilizada como evidencia: estudio "
            "(tipo: objetivo, importancia: 4).",
            resultado.evidencia
        )
        self.assertIn(
            "Tipo de inferencia: modus_ponens.",
            resultado.evidencia
        )
        self.assertEqual(
            self.reasoning.obtener_ultimo_resultado(),
            resultado
        )

    def test_comparar_opciones_conserva_recuerdos_en_evidencia(self):
        resultado = self.reasoning.comparar(
            "Python",
            "Rust",
            recuerdos=[{"contenido": "Prefiero Python"}]
        )

        self.assertEqual(
            resultado.conclusion,
            "Existen varias premisas que pueden utilizarse para "
            "construir una inferencia."
        )
        self.assertEqual(resultado.confianza, 0.6)
        self.assertIn(
            "Memoria relacionada: Prefiero Python.",
            resultado.evidencia
        )

    def test_comparar_requiere_dos_opciones(self):
        resultado = self.reasoning.comparar("Python", " ")

        self.assertEqual(
            resultado.conclusion,
            "No hay dos opciones válidas para comparar."
        )
        self.assertEqual(resultado.evidencia, [])
        self.assertEqual(resultado.confianza, 0.0)


if __name__ == "__main__":
    unittest.main()
