import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.context import Context


class TestContext(unittest.TestCase):

    def test_agregar_recorta_y_limita_mensajes(self):
        context = Context(max_messages=2)

        context.agregar("  primer mensaje  ")
        context.agregar("segundo mensaje")
        context.agregar("tercer mensaje")

        self.assertEqual(
            context.obtener_todo(),
            ["segundo mensaje", "tercer mensaje"]
        )
        self.assertEqual(context.ultimo(), "tercer mensaje")
        self.assertEqual(context.anteriores(1), ["tercer mensaje"])

    def test_ignora_mensajes_vacios_y_busca_terminos(self):
        context = Context()

        context.agregar("   ")
        context.agregar("Hablamos sobre Python")

        self.assertEqual(len(context), 1)
        self.assertTrue(context.contiene("PYTHON"))
        self.assertFalse(context.contiene(""))

    def test_tema_principal_descarta_palabras_ignoradas(self):
        context = Context()

        context.agregar("Quiero aprender Python")
        context.agregar("Python sirve para automatización")

        self.assertEqual(context.tema_principal(), "python")

    def test_limpiar_restablece_el_contexto(self):
        context = Context()
        context.agregar("mensaje")

        context.limpiar()

        self.assertEqual(context.obtener_todo(), [])
        self.assertIsNone(context.ultimo())
        self.assertEqual(context.anteriores(0), [])


if __name__ == "__main__":
    unittest.main()
