import tempfile
import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.context import Context
from brain.memory import Memory
from brain.memory_service import MemoryService
from brain.processor import BrainProcessor
from brain.reasoning import ReasoningEngine
from brain.reasoning_handler import ReasoningRequestHandler
from brain.response_formatter import ResponseFormatter


class TestBrainProcessor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory = Memory(Path(self.temp_dir.name) / "memory.json")
        self.memory_service = MemoryService(self.memory)
        self.context = Context(max_messages=10)
        self.reasoning = ReasoningEngine()
        self.reasoning_handler = ReasoningRequestHandler(
            memory_service=self.memory_service,
            reasoning=self.reasoning
        )
        self.response_formatter = ResponseFormatter()
        self.processor = BrainProcessor(
            memory_service=self.memory_service,
            context=self.context,
            reasoning=self.reasoning,
            reasoning_handler=self.reasoning_handler,
            response_formatter=self.response_formatter
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_usa_las_dependencias_inyectadas(self):
        self.assertIs(self.processor.memory, self.memory)
        self.assertIs(self.processor.memory_service, self.memory_service)
        self.assertIs(self.processor.context, self.context)
        self.assertIs(self.processor.reasoning, self.reasoning)
        self.assertIs(
            self.processor.reasoning_handler,
            self.reasoning_handler
        )
        self.assertIs(
            self.processor.response_formatter,
            self.response_formatter
        )

    def test_conserva_la_inyeccion_directa_de_memoria(self):
        processor = BrainProcessor(
            memory=self.memory,
            context=self.context,
            reasoning=self.reasoning
        )

        self.assertIs(processor.memory, self.memory)
        self.assertIs(processor.memory_service.memory, self.memory)

    def test_delega_solicitudes_de_razonamiento_y_formateo(self):
        handler = _HandlerDePrueba()
        formatter = _FormatterDePrueba()
        processor = BrainProcessor(
            memory_service=self.memory_service,
            context=self.context,
            reasoning=self.reasoning,
            reasoning_handler=handler,
            response_formatter=formatter
        )

        respuesta = processor.process("analiza una premisa")

        self.assertEqual(handler.textos, ["analiza una premisa"])
        self.assertEqual(formatter.solicitudes, [handler.resultado])
        self.assertEqual(respuesta, "respuesta formateada")

    def test_razonamiento_mantiene_prioridad_sobre_memoria_automatica(self):
        respuesta = self.processor.process("analiza mi nombre es ada")

        self.assertIn("Conclusión:", respuesta)
        self.assertEqual(self.memory.obtener_todo(), [])


    def test_rechaza_entrada_vacia(self):
        respuesta = self.processor.process("   ")

        self.assertEqual(respuesta, "No recibí ningún mensaje.")
        self.assertEqual(self.context.obtener_todo(), [])

    def test_guarda_memoria_automatica_importante(self):
        respuesta = self.processor.process("Mi nombre es Ada")

        self.assertEqual(respuesta, "Entendido. Recordaré ada.")
        self.assertEqual(
            self.memory.obtener_todo()[0]["contenido"],
            "ada"
        )
        self.assertEqual(
            self.memory.obtener_todo()[0]["tipo"],
            "identidad"
        )

    def test_recupera_memoria_guardada_manualmente(self):
        respuesta_guardado = self.processor.process("recuerda Python")
        respuesta_recuperacion = self.processor.process("recuerda mi python")

        self.assertEqual(
            respuesta_guardado,
            "Entendido. Lo guardaré como general (importancia 1)."
        )
        self.assertEqual(respuesta_recuperacion, "Recuerdo: python")

    def test_muestra_el_contexto_incluyendo_la_consulta_actual(self):
        self.processor.process("hola")

        respuesta = self.processor.process("contexto")

        self.assertEqual(respuesta, "- hola\n- contexto")

    def test_limpia_el_contexto(self):
        self.processor.process("hola")

        respuesta = self.processor.process("limpia contexto")

        self.assertEqual(respuesta, "Contexto temporal eliminado.")
        self.assertEqual(self.context.obtener_todo(), [])

    def test_analiza_con_recuerdo_relacionado(self):
        self.memory.guardar("estudio", tipo="objetivo", importancia=4)

        respuesta = self.processor.process(
            "analiza si estudio entonces apruebo"
        )

        self.assertIn("Conclusión: apruebo", respuesta)
        self.assertIn("Tipo de inferencia: modus_ponens.", respuesta)
        self.assertIn("Confianza: 100%", respuesta)


class _HandlerDePrueba:

    def __init__(self):
        self.textos = []
        self.resultado = object()

    def manejar(self, text):
        self.textos.append(text)
        return self.resultado


class _FormatterDePrueba:

    def __init__(self):
        self.solicitudes = []

    def formatear_solicitud_razonamiento(self, solicitud):
        self.solicitudes.append(solicitud)
        return "respuesta formateada"


if __name__ == "__main__":
    unittest.main()
