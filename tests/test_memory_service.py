import tempfile
import unittest
from pathlib import Path
import sys


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from brain.memory import Memory
from brain.memory_service import MemoryService


class TestMemoryService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory = Memory(Path(self.temp_dir.name) / "memory.json")
        self.service = MemoryService(self.memory)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_clasifica_tipos_de_memoria(self):
        casos = {
            "mi nombre es ada": "identidad",
            "mi proyecto es cerebrum": "proyecto",
            "me gusta python": "preferencia",
            "quiero aprender lógica": "objetivo",
            "mensaje sin patrón": "general"
        }

        for texto, tipo_esperado in casos.items():
            with self.subTest(texto=texto):
                self.assertEqual(
                    self.service.clasificar_memoria(texto),
                    tipo_esperado
                )

    def test_calcula_importancia_y_normaliza_tipos(self):
        self.assertEqual(
            self.service.calcular_importancia("identidad"),
            5
        )
        self.assertEqual(
            self.service.calcular_importancia("proyecto"),
            5
        )
        self.assertEqual(
            self.service.calcular_importancia("objetivo"),
            4
        )
        self.assertEqual(
            self.service.calcular_importancia("preferencia"),
            3
        )
        self.assertEqual(
            self.service.normalizar_tipo(" Preferencias "),
            "preferencia"
        )

    def test_extrae_contenido_conservando_la_politica_actual(self):
        self.assertEqual(
            self.service.extraer_contenido("mi nombre es ada"),
            "ada"
        )
        self.assertEqual(
            self.service.extraer_contenido("soy ada"),
            "soy ada"
        )

    def test_guarda_memoria_automatica_importante(self):
        recuerdo = self.service.guardar_si_importante(
            "mi objetivo es aprender python"
        )

        self.assertIsNotNone(recuerdo)
        self.assertEqual(recuerdo["contenido"], "aprender python")
        self.assertEqual(recuerdo["tipo"], "objetivo")
        self.assertEqual(recuerdo["importancia"], 4)
        self.assertIsNone(
            self.service.guardar_si_importante("mensaje general")
        )

    def test_guarda_manualmente_con_politica_de_tipo(self):
        recuerdo, tipo, importancia = self.service.guardar_manualmente(
            "me gusta python"
        )

        self.assertEqual(recuerdo["contenido"], "me gusta python")
        self.assertEqual(tipo, "preferencia")
        self.assertEqual(importancia, 3)

    def test_busca_recuerdos_relacionados_por_texto_y_tipo(self):
        alto = self.memory.guardar(
            "Python para automatización",
            tipo="proyecto",
            importancia=5
        )
        bajo = self.memory.guardar(
            "Python para scripts",
            tipo="preferencia",
            importancia=3
        )

        resultados = self.service.obtener_recuerdos_para_texto(
            "Quiero usar Python"
        )

        self.assertEqual(
            [recuerdo["id"] for recuerdo in resultados],
            [alto["id"], bajo["id"]]
        )
        self.assertEqual(
            self.service.buscar_por_tipo("preferencias")[0]["id"],
            bajo["id"]
        )

    def test_administra_actualizacion_eliminacion_y_relaciones(self):
        preferencia = self.memory.guardar(
            "me gusta python",
            tipo="preferencia"
        )
        relacionado = self.memory.guardar(
            "python para automatización"
        )

        recuerdo, relacionados = self.service.obtener_relacionados(
            "gusta python"
        )

        self.assertEqual(recuerdo["id"], preferencia["id"])
        self.assertEqual(
            [item["id"] for item in relacionados],
            [relacionado["id"]]
        )

        actualizado = self.service.actualizar_preferencia("gusta python")

        self.assertEqual(
            actualizado["contenido"],
            "ya no me gusta gusta python"
        )
        eliminado = self.service.eliminar("automatización")
        self.assertEqual(eliminado["id"], relacionado["id"])


if __name__ == "__main__":
    unittest.main()
