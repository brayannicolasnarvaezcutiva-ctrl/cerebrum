"""
brain/processor.py

Procesador principal del motor de IA.

v0.0.4 Alpha - Reasoning Core
"""

from brain.context import Context
from brain.intents import INTENTS, detect_intent
from brain.memory_service import MemoryService
from brain.reasoning import ReasoningEngine
from brain.reasoning_handler import ReasoningRequestHandler
from brain.response_formatter import ResponseFormatter


class BrainProcessor:
    """Procesa las entradas del usuario."""

    def __init__(
        self,
        memory=None,
        context=None,
        reasoning=None,
        memory_service=None,
        reasoning_handler=None,
        response_formatter=None
    ):
        """Inicializa el procesador con dependencias opcionales."""

        self.memory_service = (
            memory_service
            if memory_service is not None
            else MemoryService(memory)
        )
        self.memory = self.memory_service.memory
        self.context = (
            context
            if context is not None
            else Context(max_messages=10)
        )
        self.reasoning = (
            reasoning
            if reasoning is not None
            else ReasoningEngine()
        )
        self.reasoning_handler = (
            reasoning_handler
            if reasoning_handler is not None
            else ReasoningRequestHandler(
                memory_service=self.memory_service,
                reasoning=self.reasoning
            )
        )
        self.response_formatter = (
            response_formatter
            if response_formatter is not None
            else ResponseFormatter()
        )

    def _guardar_contexto(self, text: str):
        """Guarda un mensaje en el contexto temporal."""

        self.context.agregar(text)

    def process(self, text: str):
        """Procesa una entrada completa."""

        text = text.strip().lower()

        if not text:
            return "No recibí ningún mensaje."

        self._guardar_contexto(text)

        solicitud_razonamiento = self.reasoning_handler.manejar(text)

        if solicitud_razonamiento is not None:
            return self.response_formatter.formatear_solicitud_razonamiento(
                solicitud_razonamiento
            )

        # ==================================================
        # CONTEXTO
        # ==================================================

        if text in (
            "contexto",
            "ver contexto",
            "muestra mi contexto"
        ):
            mensajes = self.context.anteriores(10)

            if not mensajes:
                return "El contexto está vacío."

            return self.response_formatter.formatear_contexto(
                mensajes
            )

        # ==================================================
        # TEMA
        # ==================================================

        if text in (
            "tema",
            "tema actual",
            "de que hablamos"
        ):
            tema = self.context.tema_principal()

            if tema:
                return self.response_formatter.formatear_tema(
                    tema
                )

            return (
                "Todavía no tengo suficiente contexto."
            )

        # ==================================================
        # LIMPIAR CONTEXTO
        # ==================================================

        if text in (
            "limpia contexto",
            "borrar contexto",
            "olvida el contexto"
        ):
            self.context.limpiar()

            return (
                "Contexto temporal eliminado."
            )

        # ==================================================
        # MOSTRAR MEMORIA
        # ==================================================

        if text in (
            "memoria",
            "muestra mi memoria",
            "muéstrame mi memoria",
            "ver memoria"
        ):
            recuerdos = self.memory_service.obtener_todo()

            return self.response_formatter.formatear_recuerdos(
                recuerdos
            )

        # ==================================================
        # MEMORIA IMPORTANTE
        # ==================================================

        if text in (
            "memoria importante",
            "muestra mi memoria importante",
            "ver memoria importante"
        ):
            recuerdos = (
                self.memory_service.buscar_por_importancia(
                    4
                )
            )

            return self.response_formatter.formatear_recuerdos(
                recuerdos
            )

        # ==================================================
        # MEMORIA POR TIPO
        # ==================================================

        if text.startswith("muéstrame mis "):
            recuerdos = (
                self.memory_service.buscar_por_tipo(
                    text[14:]
                )
            )

            return self.response_formatter.formatear_recuerdos(
                recuerdos
            )

        # ==================================================
        # RECUERDOS RELACIONADOS
        # ==================================================

        if text.startswith("relacionado con "):
            termino = text[16:].strip()

            if not termino:
                return (
                    "No indicaste qué recuerdo buscar."
                )

            recuerdo, relacionados = (
                self.memory_service.obtener_relacionados(
                    termino
                )
            )

            if not recuerdo:
                return "No encuentro ese recuerdo."

            return self.response_formatter.formatear_relacionados(
                recuerdo,
                relacionados
            )

        # ==================================================
        # OLVIDAR
        # ==================================================

        if text.startswith("olvida "):
            termino = text[7:].strip()

            if not termino:
                return (
                    "No indicaste qué debo olvidar."
                )

            eliminado = self.memory_service.eliminar(
                termino
            )

            if eliminado:
                return self.response_formatter.formatear_recuerdo_eliminado(
                    eliminado
                )

            return "No encontré ese recuerdo."

        # ==================================================
        # BORRAR TODA LA MEMORIA
        # ==================================================

        if text in (
            "olvida toda mi memoria",
            "limpia mi memoria",
            "borrar memoria"
        ):
            self.memory_service.limpiar()

            return (
                "Memoria eliminada correctamente."
            )

        # ==================================================
        # RECORDAR
        # ==================================================

        if text.startswith("recuerda mi "):
            termino = text[12:].strip()

            if termino:
                recuerdo = self.memory_service.recordar(
                    termino
                )

                if recuerdo:
                    return self.response_formatter.formatear_recuerdo(
                        recuerdo
                    )

                return "No encuentro ese recuerdo."

        # ==================================================
        # ACTUALIZAR PREFERENCIA
        # ==================================================

        if text.startswith("ya no me gusta "):
            contenido = text[15:].strip()

            if not contenido:
                return (
                    "No hay nada que actualizar."
                )

            recuerdo = self.memory_service.recordar(
                contenido
            )

            if not recuerdo:
                return (
                    "No tenía registrado "
                    "ese recuerdo."
                )

            actualizado = self.memory_service.actualizar_preferencia(
                contenido
            )

            if actualizado:
                return (
                    "Entendido. He actualizado "
                    "esa preferencia."
                )

        # ==================================================
        # GUARDAR MANUALMENTE
        # ==================================================

        if text.startswith("recuerda "):
            contenido = text[9:].strip()

            if contenido:
                _, tipo, importancia = (
                    self.memory_service.guardar_manualmente(
                        contenido
                    )
                )

                return self.response_formatter.formatear_guardado_manual(
                    tipo,
                    importancia
                )

            return "No hay nada que guardar."

        # ==================================================
        # MEMORIA AUTOMÁTICA
        # ==================================================

        recuerdo_nuevo = (
            self.memory_service.guardar_si_importante(
                text
            )
        )

        # ==================================================
        # INTENCIONES
        # ==================================================

        intent = detect_intent(text)

        if intent is not None:
            return INTENTS[intent]["response"]

        # ==================================================
        # MEMORIA RELACIONADA
        # ==================================================

        recuerdo_relacionado = (
            self.memory_service.recordar(text)
        )

        if recuerdo_relacionado:
            return self.response_formatter.formatear_recuerdo_relacionado(
                recuerdo_relacionado
            )

        # ==================================================
        # CONTEXTO RECIENTE
        # ==================================================

        anteriores = self.context.anteriores(3)

        if len(anteriores) >= 2:
            anterior = anteriores[-2]

            if text == anterior:
                return self.response_formatter.formatear_repeticion(
                    anterior
                )

        # ==================================================
        # NUEVA MEMORIA
        # ==================================================

        if recuerdo_nuevo:
            return self.response_formatter.formatear_nueva_memoria(
                recuerdo_nuevo
            )

        return (
            "Todavía estoy aprendiendo "
            f"a procesar: {text}"
        )
