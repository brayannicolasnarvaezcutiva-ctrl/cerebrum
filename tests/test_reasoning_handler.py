import tempfile
import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.memory import Memory
from brain.memory_service import MemoryService
from brain.reasoning import ReasoningEngine
from brain.reasoning_handler import ReasoningRequestHandler


class TestReasoningRequestHandler(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory = Memory(Path(self.temp_dir.name) / "memory.json")
        self.memory_service = MemoryService(self.memory)
        self.reasoning = ReasoningEngine()
        self.handler = ReasoningRequestHandler(
            memory_service=self.memory_service,
            reasoning=self.reasoning
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ignora_solicitudes_que_no_son_de_razonamiento(self):
        self.assertIsNone(self.handler.manejar("contexto"))

    def test_informa_cuando_no_hay_contenido_para_analizar(self):
        resultado = self.handler.manejar("analiza ")

        self.assertEqual(resultado.mensaje, "No hay nada que analizar.")
        self.assertIsNone(resultado.resultado)

    def test_analizar_usa_memoria_como_evidencia(self):
        self.memory.guardar("estudio", tipo="objetivo", importancia=4)

        solicitud = self.handler.manejar(
            "analiza si estudio entonces apruebo"
        )

        self.assertIsNone(solicitud.mensaje)
        self.assertEqual(solicitud.resultado.conclusion, "apruebo")
        self.assertEqual(solicitud.resultado.confianza, 1.0)
        self.assertIn(
            "Memoria utilizada como evidencia: estudio "
            "(tipo: objetivo, importancia: 4).",
            solicitud.resultado.evidencia
        )

    def test_comparar_valida_formato_y_prepara_evidencia(self):
        invalida = self.handler.manejar("compara python")

        self.assertEqual(
            invalida.mensaje,
            "Usa el formato: compara opción A vs opción B"
        )

        self.memory.guardar("prefiero python", importancia=3)
        valida = self.handler.manejar("compara python vs rust")

        self.assertIsNone(valida.mensaje)
        self.assertEqual(valida.resultado.confianza, 0.6)
        self.assertIn(
            "Memoria relacionada: prefiero python.",
            valida.resultado.evidencia
        )


if __name__ == "__main__":
    unittest.main()
