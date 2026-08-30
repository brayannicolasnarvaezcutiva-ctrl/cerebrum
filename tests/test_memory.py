import tempfile
import unittest
from pathlib import Path

from src.brain.memory import Memory


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.memory = Memory(
            Path(self.temp_dir.name) / "memory.json"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_guardar_y_recuperar(self):
        self.memory.guardar(
            "me gusta Blender",
            tipo="preferencia",
            importancia=3
        )

        recuerdo = self.memory.recordar(
            "Blender"
        )

        self.assertIsNotNone(recuerdo)
        self.assertEqual(
            recuerdo["contenido"],
            "me gusta Blender"
        )

    def test_no_duplica(self):
        self.memory.guardar(
            "me gusta Blender",
            tipo="preferencia"
        )

        self.memory.guardar(
            "me gusta Blender",
            tipo="preferencia"
        )

        recuerdos = self.memory.obtener_todo()

        self.assertEqual(
            len(recuerdos),
            1
        )

    def test_actualizar(self):
        self.memory.guardar(
            "me gusta Blender",
            tipo="preferencia"
        )

        resultado = self.memory.actualizar(
            "Blender",
            "ya no me gusta Blender",
            tipo="preferencia"
        )

        self.assertIsNotNone(resultado)

        recuerdo = self.memory.recordar(
            "Blender"
        )

        self.assertEqual(
            recuerdo["contenido"],
            "ya no me gusta Blender"
        )


if __name__ == "__main__":
    unittest.main()