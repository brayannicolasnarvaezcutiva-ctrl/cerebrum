import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.inference import InferenceEngine


class TestInferenceEngine(unittest.TestCase):

    def setUp(self):
        self.inference = InferenceEngine()

    def test_sin_premisas_devuelve_sin_datos(self):
        resultado = self.inference.inferir([])

        self.assertEqual(
            resultado,
            {
                "conclusion": "No hay premisas suficientes.",
                "premisas": [],
                "confianza": 0.0,
                "tipo": "sin_datos"
            }
        )
        self.assertEqual(
            self.inference.obtener_ultima_inferencia(),
            resultado
        )

    def test_aplica_modus_ponens(self):
        resultado = self.inference.inferir(
            ["Si estudio entonces apruebo", "estudio"]
        )

        self.assertEqual(resultado["conclusion"], "apruebo")
        self.assertEqual(resultado["tipo"], "modus_ponens")
        self.assertEqual(resultado["confianza"], 0.95)
        self.assertEqual(resultado["contradicciones"], [])

    def test_informa_cuando_la_regla_no_se_activa(self):
        resultado = self.inference.inferir(
            ["si estudio entonces apruebo", "descanso"]
        )

        self.assertEqual(resultado["tipo"], "regla_no_activada")
        self.assertEqual(resultado["confianza"], 0.7)
        self.assertEqual(
            resultado["conclusion"],
            "No puedo concluir 'apruebo' porque no se cumple la "
            "condición 'estudio'."
        )

    def test_no_infiere_con_premisas_contradictorias(self):
        resultado = self.inference.inferir(
            ["estudio", "no estudio"]
        )

        self.assertEqual(resultado["tipo"], "contradiccion")
        self.assertEqual(resultado["confianza"], 0.0)
        self.assertEqual(
            resultado["contradicciones"],
            ["Contradicción detectada: 'estudio' y 'no estudio'."]
        )

    def test_separa_justificaciones_antes_de_inferir(self):
        resultado = self.inference.inferir(
            ["llueve porque hay nubes", "hace frío"]
        )

        self.assertEqual(resultado["tipo"], "multiples_premisas")
        self.assertEqual(
            resultado["premisas"],
            ["llueve", "hay nubes", "hace frío"]
        )


if __name__ == "__main__":
    unittest.main()
