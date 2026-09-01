import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.logic import LogicAnalyzer


class TestLogicAnalyzer(unittest.TestCase):

    def setUp(self):
        self.logic = LogicAnalyzer()

    def test_premisas_vacias_no_son_validas(self):
        resultado = self.logic.validar_premisas([])

        self.assertEqual(
            resultado,
            {
                "validas": False,
                "consistentes": False,
                "contradicciones": [],
                "cantidad": 0
            }
        )
        self.assertEqual(self.logic.obtener_ultimo_analisis(), resultado)

    def test_detecta_contradicciones_simples(self):
        contradicciones = self.logic.detectar_contradicciones(
            ["Estudio", "no estudio"]
        )

        self.assertEqual(
            contradicciones,
            ["Contradicción detectada: 'estudio' y 'no estudio'."]
        )

    def test_valida_premisas_consistentes(self):
        resultado = self.logic.validar_premisas(
            ["estudio", "nunca abandono"]
        )

        self.assertTrue(resultado["validas"])
        self.assertTrue(resultado["consistentes"])
        self.assertEqual(resultado["contradicciones"], [])
        self.assertEqual(resultado["cantidad"], 2)


if __name__ == "__main__":
    unittest.main()
