"""
brain/processor.py

Procesador principal del motor de IA.

v0.0.3 Alpha - Memory Seed
"""

from brain.context import Context
from brain.intents import INTENTS, detect_intent
from brain.memory import Memory


class BrainProcessor:
    """Procesa las entradas del usuario."""

    def __init__(self):
        self.memory = Memory()
        self.context = Context(max_messages=10)

    def _clasificar_memoria(self, text: str):
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

    def _calcular_importancia(self, tipo: str):
        """Calcula automáticamente la importancia."""

        importancia = {
            "identidad": 5,
            "proyecto": 5,
            "objetivo": 4,
            "preferencia": 3,
            "general": 1
        }

        return importancia.get(tipo, 1)

    def _extraer_contenido(self, text: str):
        """Extrae la información relevante de una frase."""

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

    def _guardar_memoria_si_importante(self, text: str):
        """Guarda automáticamente información importante."""

        tipo = self._clasificar_memoria(text)

        if tipo == "general":
            return None

        contenido = self._extraer_contenido(text)

        if not contenido:
            return None

        importancia = self._calcular_importancia(tipo)

        return self.memory.guardar(
            contenido,
            tipo=tipo,
            importancia=importancia
        )

    def _normalizar_tipo(self, tipo: str):
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

    def _formatear_recuerdos(self, recuerdos):
        """Convierte recuerdos en texto legible."""

        if not recuerdos:
            return "No tengo recuerdos registrados."

        return "\n".join(
            f"[{recuerdo['id']}] "
            f"{recuerdo['contenido']} "
            f"(tipo: {recuerdo['tipo']}, "
            f"importancia: {recuerdo['importancia']})"
            for recuerdo in recuerdos
        )

    def process(self, text: str):
        """Procesa una entrada completa."""

        text = text.strip().lower()

        if not text:
            return "No recibí ningún mensaje."

        # Guardar en contexto temporal.
        self.context.agregar(text)

        # --------------------------------------------------
        # Mostrar contexto reciente
        # --------------------------------------------------

        if text in (
            "contexto",
            "ver contexto",
            "muestra mi contexto"
        ):
            mensajes = self.context.anteriores(10)

            if not mensajes:
                return "El contexto está vacío."

            return "\n".join(
                f"- {mensaje}"
                for mensaje in mensajes
            )

        # --------------------------------------------------
        # Limpiar contexto temporal
        # --------------------------------------------------

        if text in (
            "limpia contexto",
            "borrar contexto",
            "olvida el contexto"
        ):
            self.context.limpiar()
            return "Contexto temporal eliminado."

        # --------------------------------------------------
        # Mostrar toda la memoria
        # --------------------------------------------------

        if text in (
            "memoria",
            "muestra mi memoria",
            "muéstrame mi memoria",
            "ver memoria"
        ):
            recuerdos = self.memory.obtener_todo()
            return self._formatear_recuerdos(recuerdos)

        # --------------------------------------------------
        # Mostrar memoria importante
        # --------------------------------------------------

        if text in (
            "memoria importante",
            "muestra mi memoria importante",
            "ver memoria importante"
        ):
            recuerdos = self.memory.buscar_por_importancia(4)
            return self._formatear_recuerdos(recuerdos)

        # --------------------------------------------------
        # Mostrar recuerdos por categoría
        # --------------------------------------------------

        if text.startswith("muéstrame mis "):
            tipo = self._normalizar_tipo(
                text[14:]
            )

            recuerdos = self.memory.buscar_por_tipo(
                tipo
            )

            return self._formatear_recuerdos(
                recuerdos
            )

        # --------------------------------------------------
        # Buscar recuerdos relacionados
        # --------------------------------------------------

        if text.startswith("relacionado con "):
            termino = text[16:].strip()

            if not termino:
                return "No indicaste qué recuerdo buscar."

            recuerdo = self.memory.recordar(
                termino
            )

            if not recuerdo:
                return "No encuentro ese recuerdo."

            relacionados = self.memory.obtener_relacionados(
                recuerdo["id"]
            )

            if not relacionados:
                return (
                    f"El recuerdo '{recuerdo['contenido']}' "
                    "no tiene relaciones registradas."
                )

            return "\n".join(
                f"- {item['contenido']} "
                f"(tipo: {item['tipo']})"
                for item in relacionados
            )

        # --------------------------------------------------
        # Eliminar un recuerdo
        # --------------------------------------------------

        if text.startswith("olvida "):
            termino = text[7:].strip()

            if not termino:
                return "No indicaste qué debo olvidar."

            eliminado = self.memory.eliminar(
                termino
            )

            if eliminado:
                return (
                    "Recuerdo eliminado: "
                    f"{eliminado['contenido']}"
                )

            return "No encontré ese recuerdo."

        # --------------------------------------------------
        # Limpiar toda la memoria
        # --------------------------------------------------

        if text in (
            "olvida toda mi memoria",
            "limpia mi memoria",
            "borrar memoria"
        ):
            self.memory.limpiar()
            return "Memoria eliminada correctamente."

        # --------------------------------------------------
        # Buscar un recuerdo específico
        # --------------------------------------------------

        if text.startswith("recuerda mi "):
            termino = text[12:].strip()

            if termino:
                recuerdo = self.memory.recordar(
                    termino
                )

                if recuerdo:
                    return (
                        f"Recuerdo: "
                        f"{recuerdo['contenido']}"
                    )

                return "No encuentro ese recuerdo."

        # --------------------------------------------------
        # Actualizar una preferencia
        # --------------------------------------------------

        if text.startswith("ya no me gusta "):
            contenido = text[15:].strip()

            if not contenido:
                return "No hay nada que actualizar."

            recuerdo = self.memory.recordar(
                contenido
            )

            if not recuerdo:
                return (
                    "No tenía registrado "
                    "ese recuerdo."
                )

            actualizado = self.memory.actualizar(
                contenido,
                f"ya no me gusta {contenido}",
                tipo="preferencia",
                importancia=3
            )

            if actualizado:
                return (
                    "Entendido. He actualizado "
                    "esa preferencia."
                )

        # --------------------------------------------------
        # Guardar manualmente
        # --------------------------------------------------

        if text.startswith("recuerda "):
            contenido = text[9:].strip()

            if contenido:
                tipo = self._clasificar_memoria(
                    contenido
                )

                importancia = self._calcular_importancia(
                    tipo
                )

                self.memory.guardar(
                    contenido,
                    tipo=tipo,
                    importancia=importancia
                )

                return (
                    f"Entendido. Lo guardaré "
                    f"como {tipo} "
                    f"(importancia {importancia})."
                )

            return "No hay nada que guardar."

        # --------------------------------------------------
        # Memoria automática
        # --------------------------------------------------

        recuerdo_nuevo = (
            self._guardar_memoria_si_importante(
                text
            )
        )

        # --------------------------------------------------
        # Intenciones conocidas
        # --------------------------------------------------

        intent = detect_intent(text)

        if intent is not None:
            return INTENTS[intent]["response"]

        # --------------------------------------------------
        # Buscar recuerdo relacionado
        # --------------------------------------------------

        recuerdo_relacionado = self.memory.recordar(
            text
        )

        if recuerdo_relacionado:
            return (
                "Recuerdo relacionado: "
                f"{recuerdo_relacionado['contenido']}"
            )

        # --------------------------------------------------
        # Contexto reciente
        # --------------------------------------------------

        if text in (
            "tema",
            "tema actual",
            "de que hablamos"
        ):
            tema = self.context.tema_principal()

            if tema:
                return f"El tema reciente parece ser: {tema}"

            return "Todavía no tengo suficiente contexto."

        # --------------------------------------------------
        # Confirmar nueva memoria
        # --------------------------------------------------

        if recuerdo_nuevo:
            return (
                "Entendido. Recordaré "
                f"{recuerdo_nuevo['contenido']}."
            )

        return (
            "Todavía estoy aprendiendo "
            f"a procesar: {text}"
        )