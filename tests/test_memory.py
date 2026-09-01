import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.brain.memory import Memory, MemoryCorruptionError


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

    def test_busquedas_por_tipo_e_importancia(self):
        self.memory.guardar(
            "Python para automatización",
            tipo="proyecto",
            importancia=5
        )
        self.memory.guardar(
            "Python para scripts pequeños",
            tipo="general",
            importancia=2
        )

        resultados = self.memory.buscar("python")

        self.assertEqual(
            [recuerdo["importancia"] for recuerdo in resultados],
            [5, 2]
        )
        self.assertEqual(
            self.memory.buscar_por_tipo("proyecto")[0]["contenido"],
            "Python para automatización"
        )
        self.assertEqual(
            len(self.memory.buscar_por_importancia(4)),
            1
        )

    def test_crea_y_elimina_relaciones(self):
        primero = self.memory.guardar(
            "Aprendo Python para automatización"
        )
        segundo = self.memory.guardar(
            "Python es mi lenguaje favorito"
        )

        relacionados = self.memory.obtener_relacionados(
            primero["id"]
        )

        self.assertEqual(
            [recuerdo["id"] for recuerdo in relacionados],
            [segundo["id"]]
        )

        self.memory.eliminar("automatización")

        self.assertEqual(
            self.memory.obtener_relacionados(segundo["id"]),
            []
        )

    def test_limpiar_elimina_todos_los_recuerdos(self):
        self.memory.guardar("primer recuerdo")
        self.memory.guardar("segundo recuerdo")

        self.memory.limpiar()

        self.assertEqual(self.memory.obtener_todo(), [])

    def test_carga_json_valido(self):
        recuerdos = [
            {
                "id": 1,
                "tipo": "general",
                "contenido": "recuerdo válido",
                "importancia": 1,
                "fecha": "2026-08-31T00:00:00",
                "relaciones": []
            }
        ]
        self.memory.file_path.write_text(
            json.dumps(recuerdos, ensure_ascii=False),
            encoding="utf-8"
        )

        self.assertEqual(self.memory.obtener_todo(), recuerdos)

    def test_memoria_vacia_se_distingue_de_memoria_corrupta(self):
        self.assertEqual(self.memory.obtener_todo(), [])

    def test_json_corrupto_lanza_error_y_no_se_sobrescribe(self):
        contenido_corrupto = "{ memoria invalida"
        self.memory.file_path.write_text(
            contenido_corrupto,
            encoding="utf-8"
        )

        with self.assertRaises(MemoryCorruptionError) as error:
            self.memory.obtener_todo()

        self.assertIn(
            str(self.memory.file_path),
            str(error.exception)
        )
        with self.assertRaises(MemoryCorruptionError):
            self.memory.guardar("nuevo recuerdo")

        self.assertEqual(
            self.memory.file_path.read_text(encoding="utf-8"),
            contenido_corrupto
        )

    def test_persistencia_despues_de_multiples_operaciones(self):
        self.memory.guardar("primer recuerdo")
        self.memory.guardar("segundo recuerdo")
        self.memory.actualizar("primer", "primer recuerdo actualizado")
        self.memory.eliminar("segundo")

        memoria_recargada = Memory(self.memory.file_path)

        self.assertEqual(
            [recuerdo["contenido"] for recuerdo in memoria_recargada.obtener_todo()],
            ["primer recuerdo actualizado"]
        )

    def test_actualizar_preserva_los_demas_datos(self):
        self.memory.guardar("primer recuerdo", tipo="objetivo")
        self.memory.guardar("segundo recuerdo", tipo="proyecto")

        self.memory.actualizar(
            "primer",
            "primer recuerdo actualizado"
        )

        recuerdos = self.memory.obtener_todo()

        self.assertEqual(len(recuerdos), 2)
        self.assertEqual(
            recuerdos[0]["contenido"],
            "primer recuerdo actualizado"
        )
        self.assertEqual(recuerdos[1]["contenido"], "segundo recuerdo")
        self.assertEqual(recuerdos[1]["tipo"], "proyecto")

    def test_fallo_de_reemplazo_preserva_el_archivo_original(self):
        self.memory.guardar("recuerdo original")
        contenido_original = self.memory.file_path.read_text(
            encoding="utf-8"
        )

        with patch(
            "src.brain.memory.os.replace",
            side_effect=OSError("fallo de reemplazo")
        ):
            with self.assertRaises(OSError):
                self.memory.guardar("recuerdo nuevo")

        self.assertEqual(
            self.memory.file_path.read_text(encoding="utf-8"),
            contenido_original
        )
        self.assertEqual(
            list(self.memory.file_path.parent.glob(".memory.json.*.tmp")),
            []
        )


if __name__ == "__main__":
    unittest.main()
