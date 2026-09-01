"""
CEREBRUM
Política de memoria de la capa de aplicación.

v0.0.4 Alpha - Reasoning Core
"""

from brain.memory import Memory


class MemoryService:
    """Coordina la política de memoria sobre un almacenamiento Memory."""

    def __init__(self, memory=None):
        self.memory = memory if memory is not None else Memory()

    def clasificar_memoria(self, text: str):
        """Determina el tipo de información."""

        reglas = {
            "identidad": [
                "mi nombre es ",
                "me llamo ",
                "soy "
            ],
            "proyecto": [
                "mi proyecto es ",
                "estoy trabajando en ",
                "estoy haciendo "
            ],
            "preferencia": [
                "me gusta ",
                "me encanta ",
                "prefiero ",
                "no me gusta ",
                "ya no me gusta "
            ],
            "objetivo": [
                "quiero ",
                "mi objetivo es ",
                "planeo "
            ]
        }

        for tipo, patrones in reglas.items():
            if any(patron in text for patron in patrones):
                return tipo

        return "general"

    def calcular_importancia(self, tipo: str):
        """Calcula automáticamente la importancia."""

        importancia = {
            "identidad": 5,
            "proyecto": 5,
            "objetivo": 4,
            "preferencia": 3,
            "general": 1
        }

        return importancia.get(tipo, 1)

    def extraer_contenido(self, text: str):
        """Extrae la información relevante."""

        patrones = [
            "mi nombre es ",
            "me llamo ",
            "mi proyecto es ",
            "me gusta ",
            "me encanta ",
            "prefiero ",
            "no me gusta ",
            "ya no me gusta ",
            "mi objetivo es ",
            "quiero ",
            "planeo "
        ]

        for patron in patrones:
            if patron in text:
                contenido = text.split(
                    patron,
                    1
                )[1].strip()

                if contenido:
                    return contenido

        return text

    def normalizar_tipo(self, tipo: str):
        """Normaliza nombres de categorías."""

        equivalencias = {
            "preferencias": "preferencia",
            "proyectos": "proyecto",
            "identidades": "identidad",
            "objetivos": "objetivo",
            "generales": "general"
        }

        tipo = tipo.lower().strip()

        return equivalencias.get(
            tipo,
            tipo
        )

    def guardar_si_importante(self, text: str):
        """Guarda automáticamente información importante."""

        tipo = self.clasificar_memoria(text)

        if tipo == "general":
            return None

        contenido = self.extraer_contenido(text)

        if not contenido:
            return None

        importancia = self.calcular_importancia(tipo)

        return self.memory.guardar(
            contenido,
            tipo=tipo,
            importancia=importancia
        )

    def guardar_manualmente(self, contenido):
        """Guarda una memoria con el tipo e importancia calculados."""

        tipo = self.clasificar_memoria(contenido)
        importancia = self.calcular_importancia(tipo)

        recuerdo = self.memory.guardar(
            contenido,
            tipo=tipo,
            importancia=importancia
        )

        return recuerdo, tipo, importancia

    def obtener_recuerdos_para_texto(self, texto):
        """Busca recuerdos relacionados con un texto."""

        palabras = texto.lower().split()

        resultados = []
        ids_vistos = set()

        for palabra in palabras:
            palabra = palabra.strip(
                ".,!?¿¡:;()[]{}\"'"
            )

            if len(palabra) < 4:
                continue

            recuerdos = self.memory.buscar(
                palabra
            )

            for recuerdo in recuerdos:
                recuerdo_id = recuerdo.get(
                    "id"
                )

                if recuerdo_id not in ids_vistos:
                    resultados.append(recuerdo)
                    ids_vistos.add(recuerdo_id)

        resultados.sort(
            key=lambda recuerdo: recuerdo.get(
                "importancia",
                1
            ),
            reverse=True
        )

        return resultados

    def obtener_todo(self):
        """Devuelve todos los recuerdos."""

        return self.memory.obtener_todo()

    def buscar_por_importancia(self, minimo):
        """Busca recuerdos por importancia mínima."""

        return self.memory.buscar_por_importancia(minimo)

    def buscar_por_tipo(self, tipo):
        """Busca recuerdos por tipo, aceptando nombres plurales."""

        return self.memory.buscar_por_tipo(
            self.normalizar_tipo(tipo)
        )

    def recordar(self, termino):
        """Recupera el recuerdo más importante que coincida."""

        return self.memory.recordar(termino)

    def obtener_relacionados(self, termino):
        """Recupera un recuerdo y sus relaciones."""

        recuerdo = self.recordar(termino)

        if not recuerdo:
            return None, []

        relacionados = self.memory.obtener_relacionados(
            recuerdo["id"]
        )

        return recuerdo, relacionados

    def eliminar(self, termino):
        """Elimina el primer recuerdo que coincida."""

        return self.memory.eliminar(termino)

    def limpiar(self):
        """Elimina todos los recuerdos."""

        self.memory.limpiar()

    def actualizar_preferencia(self, contenido):
        """Actualiza una preferencia existente."""

        return self.memory.actualizar(
            contenido,
            f"ya no me gusta {contenido}",
            tipo="preferencia",
            importancia=3
        )
