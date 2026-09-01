"""
CEREBRUM
Sistema de memoria persistente y asociativa.

v0.0.3 Alpha - Memory Seed
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path


class MemoryCorruptionError(RuntimeError):
    """Indica que el archivo de memoria no se puede usar con seguridad."""

    def __init__(self, file_path, reason):
        super().__init__(
            f"La memoria persistente está corrupta en "
            f"'{file_path}': {reason}"
        )


class Memory:
    """Gestiona la memoria persistente de CEREBRUM."""

    STOPWORDS = {
        "que", "como", "para", "este", "esta",
        "esto", "desde", "porque", "cuando",
        "donde", "quiero", "mi", "mis", "me",
        "muy", "una", "uno", "las", "los",
        "del", "con", "por", "sobre", "es",
        "soy"
    }

    def __init__(self, file_path="data/memory.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self._guardar_archivo([])

    def _guardar_archivo(self, memoria):
        """Escribe la memoria en disco mediante un reemplazo atómico."""

        contenido = json.dumps(
            memoria,
            indent=4,
            ensure_ascii=False
        )
        archivo_temporal = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.file_path.parent,
                prefix=f".{self.file_path.name}.",
                suffix=".tmp",
                delete=False
            ) as temporal:
                archivo_temporal = Path(temporal.name)
                temporal.write(contenido)
                temporal.flush()
                os.fsync(temporal.fileno())

            os.replace(archivo_temporal, self.file_path)

        finally:
            if (
                archivo_temporal is not None
                and archivo_temporal.exists()
            ):
                archivo_temporal.unlink()

    def _cargar_archivo(self):
        """Carga la memoria desde disco."""

        try:
            contenido = self.file_path.read_text(
                encoding="utf-8"
            )

        except FileNotFoundError:
            return []

        try:
            memoria = json.loads(contenido)

        except json.JSONDecodeError as error:
            raise MemoryCorruptionError(
                self.file_path,
                "el contenido no es JSON válido"
            ) from error

        if not isinstance(memoria, list):
            raise MemoryCorruptionError(
                self.file_path,
                "el contenido debe ser una lista de recuerdos"
            )

        return memoria

    def _siguiente_id(self, memoria):
        """Genera un ID único."""

        if not memoria:
            return 1

        ids = [
            recuerdo.get("id", 0)
            for recuerdo in memoria
            if isinstance(recuerdo, dict)
        ]

        return max(ids, default=0) + 1

    def _palabras_clave(self, texto):
        """Extrae palabras relevantes para asociaciones."""

        palabras = texto.lower().split()

        return {
            palabra.strip(".,!?¿¡:;()[]{}\"'")
            for palabra in palabras
            if len(palabra.strip(".,!?¿¡:;()[]{}\"'")) >= 4
            and palabra.strip(".,!?¿¡:;()[]{}\"'") not in self.STOPWORDS
        }

    def _crear_relaciones(self, nuevo_recuerdo, memoria):
        """Relaciona el nuevo recuerdo con recuerdos similares."""

        nuevas_claves = self._palabras_clave(
            nuevo_recuerdo["contenido"]
        )

        for recuerdo in memoria:
            if recuerdo["id"] == nuevo_recuerdo["id"]:
                continue

            claves_existentes = self._palabras_clave(
                recuerdo.get("contenido", "")
            )

            if nuevas_claves & claves_existentes:
                if nuevo_recuerdo["id"] not in recuerdo.get(
                    "relaciones", []
                ):
                    recuerdo.setdefault(
                        "relaciones", []
                    ).append(nuevo_recuerdo["id"])

                if recuerdo["id"] not in nuevo_recuerdo.get(
                    "relaciones", []
                ):
                    nuevo_recuerdo.setdefault(
                        "relaciones", []
                    ).append(recuerdo["id"])

    def guardar(
        self,
        contenido,
        tipo="general",
        importancia=1
    ):
        """Guarda un recuerdo evitando duplicados."""

        memoria = self._cargar_archivo()

        contenido = contenido.strip()
        tipo = tipo.strip().lower()

        importancia = max(
            1,
            min(5, int(importancia))
        )

        for recuerdo in memoria:
            contenido_existente = (
                recuerdo.get("contenido", "")
                .strip()
                .lower()
            )

            tipo_existente = (
                recuerdo.get("tipo", "")
                .strip()
                .lower()
            )

            if (
                contenido_existente == contenido.lower()
                and tipo_existente == tipo
            ):
                if importancia > recuerdo.get(
                    "importancia",
                    1
                ):
                    recuerdo["importancia"] = importancia
                    recuerdo["fecha"] = datetime.now().isoformat(
                        timespec="seconds"
                    )
                    self._guardar_archivo(memoria)

                return recuerdo

        recuerdo = {
            "id": self._siguiente_id(memoria),
            "tipo": tipo,
            "contenido": contenido,
            "importancia": importancia,
            "fecha": datetime.now().isoformat(
                timespec="seconds"
            ),
            "relaciones": []
        }

        self._crear_relaciones(
            recuerdo,
            memoria
        )

        memoria.append(recuerdo)
        self._guardar_archivo(memoria)

        return recuerdo

    def buscar(self, termino):
        """Busca recuerdos relacionados con un término."""

        memoria = self._cargar_archivo()
        termino = termino.lower().strip()

        resultados = [
            recuerdo
            for recuerdo in memoria
            if termino in recuerdo.get(
                "contenido",
                ""
            ).lower()
        ]

        return sorted(
            resultados,
            key=lambda recuerdo: recuerdo.get(
                "importancia",
                1
            ),
            reverse=True
        )

    def buscar_por_tipo(self, tipo):
        """Devuelve recuerdos de un tipo específico."""

        memoria = self._cargar_archivo()
        tipo = tipo.lower().strip()

        resultados = [
            recuerdo
            for recuerdo in memoria
            if recuerdo.get(
                "tipo",
                ""
            ).lower() == tipo
        ]

        return sorted(
            resultados,
            key=lambda recuerdo: recuerdo.get(
                "importancia",
                1
            ),
            reverse=True
        )

    def buscar_por_importancia(self, minimo=1):
        """Devuelve recuerdos con importancia mínima."""

        memoria = self._cargar_archivo()

        minimo = max(
            1,
            min(5, int(minimo))
        )

        resultados = [
            recuerdo
            for recuerdo in memoria
            if recuerdo.get(
                "importancia",
                1
            ) >= minimo
        ]

        return sorted(
            resultados,
            key=lambda recuerdo: recuerdo.get(
                "importancia",
                1
            ),
            reverse=True
        )

    def recordar(self, termino):
        """Devuelve el recuerdo más importante que coincida."""

        resultados = self.buscar(termino)

        if resultados:
            return resultados[0]

        return None

    def obtener_relacionados(self, recuerdo_id):
        """Devuelve recuerdos relacionados con un ID."""

        memoria = self._cargar_archivo()

        objetivo = None

        for recuerdo in memoria:
            if recuerdo.get("id") == recuerdo_id:
                objetivo = recuerdo
                break

        if objetivo is None:
            return []

        relaciones = objetivo.get(
            "relaciones",
            []
        )

        return [
            recuerdo
            for recuerdo in memoria
            if recuerdo.get("id") in relaciones
        ]

    def actualizar(
        self,
        termino,
        nuevo_contenido,
        tipo=None,
        importancia=None
    ):
        """Actualiza el primer recuerdo coincidente."""

        memoria = self._cargar_archivo()
        termino = termino.lower().strip()

        for recuerdo in memoria:
            contenido = recuerdo.get(
                "contenido",
                ""
            ).lower()

            if termino in contenido:
                recuerdo["contenido"] = nuevo_contenido

                if tipo is not None:
                    recuerdo["tipo"] = (
                        tipo.strip().lower()
                    )

                if importancia is not None:
                    recuerdo["importancia"] = max(
                        1,
                        min(5, int(importancia))
                    )

                recuerdo["fecha"] = datetime.now().isoformat(
                    timespec="seconds"
                )

                self._guardar_archivo(memoria)
                return recuerdo

        return None

    def eliminar(self, termino):
        """Elimina el primer recuerdo coincidente."""

        memoria = self._cargar_archivo()
        termino = termino.lower().strip()

        for indice, recuerdo in enumerate(memoria):
            contenido = recuerdo.get(
                "contenido",
                ""
            ).lower()

            if termino in contenido:
                eliminado = memoria.pop(indice)

                for otro in memoria:
                    if eliminado["id"] in otro.get(
                        "relaciones",
                        []
                    ):
                        otro["relaciones"].remove(
                            eliminado["id"]
                        )

                self._guardar_archivo(memoria)

                return eliminado

        return None

    def obtener_todo(self):
        """Devuelve todos los recuerdos."""

        return self._cargar_archivo()

    def limpiar(self):
        """Elimina toda la memoria."""

        self._guardar_archivo([])
