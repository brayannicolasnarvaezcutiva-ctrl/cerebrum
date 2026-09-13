"""
CEREBRUM
Puente entre el sistema de memoria y el núcleo cognitivo.

v0.0.8 Alpha - Memory Bridge
"""

from .memory_policy import MemoryPolicy
from .memory_ranker import MemoryRanker
from .memory_service import MemoryService


class MemoryBridge:
    """
    Punto de acceso de alto nivel a la memoria de CEREBRUM.

    Coordina:

        MemoryPolicy
        MemoryRanker
        MemoryService

    sin exponer directamente el almacenamiento.
    """

    def __init__(
        self,
        memory_service: MemoryService | None = None,
        memory_policy: MemoryPolicy | None = None,
        memory_ranker: MemoryRanker | None = None
    ):
        self.memory_service = (
            memory_service
            or MemoryService()
        )

        self.memory_policy = (
            memory_policy
            or MemoryPolicy()
        )

        self.memory_ranker = (
            memory_ranker
            or MemoryRanker()
        )

    def evaluar(
        self,
        contenido: str
    ) -> dict:
        """
        Evalúa si un contenido merece convertirse
        en memoria persistente.
        """

        self._validar_texto(
            contenido,
            "contenido"
        )

        return self.memory_policy.evaluar(
            self.memory_service,
            contenido
        )

    def guardar(
        self,
        contenido: str
    ):
        """
        Guarda automáticamente si la política lo permite.
        """

        self._validar_texto(
            contenido,
            "contenido"
        )

        contenido = contenido.strip()

        if not contenido:
            return None

        return self.memory_policy.guardar_si_corresponde(
            self.memory_service,
            contenido
        )

    def guardar_manual(
        self,
        contenido: str
    ):
        """
        Guarda una memoria de forma explícita.
        """

        self._validar_texto(
            contenido,
            "contenido"
        )

        contenido = contenido.strip()

        if not contenido:
            raise ValueError(
                "contenido no puede estar vacío"
            )

        return self.memory_service.guardar_manualmente(
            contenido
        )

    def recordar(
        self,
        termino: str
    ):
        """
        Recupera el recuerdo más importante
        relacionado con un término.
        """

        self._validar_texto(
            termino,
            "termino"
        )

        termino = termino.strip()

        if not termino:
            return None

        return self.memory_service.recordar(
            termino
        )

    def recuperar_relevante(
        self,
        texto: str
    ):
        """
        Recupera y ordena recuerdos relevantes.
        """

        self._validar_texto(
            texto,
            "texto"
        )

        texto = texto.strip()

        if not texto:
            return []

        recuerdos = (
            self.memory_service
            .obtener_recuerdos_para_texto(
                texto
            )
        )

        return self.memory_ranker.ordenar(
            recuerdos,
            texto
        )

    def obtener_contexto(
        self,
        texto: str,
        limite: int = 10
    ) -> list[dict]:
        """
        Recupera recuerdos relevantes y limita su cantidad.
        """

        self._validar_texto(
            texto,
            "texto"
        )

        limite = max(
            1,
            int(limite)
        )

        recuerdos = self.recuperar_relevante(
            texto
        )

        return recuerdos[:limite]

    def contexto_para(
        self,
        texto: str,
        limite: int = 10
    ) -> list[str]:
        """
        Convierte recuerdos relevantes en texto
        listo para contexto cognitivo.
        """

        recuerdos = self.obtener_contexto(
            texto,
            limite=limite
        )

        return [
            recuerdo["contenido"]
            for recuerdo in recuerdos
            if isinstance(
                recuerdo,
                dict
            )
            and recuerdo.get(
                "contenido"
            )
        ]

    def obtener_relacionados(
        self,
        termino: str
    ):
        """
        Recupera un recuerdo y sus relacionados.
        """

        self._validar_texto(
            termino,
            "termino"
        )

        termino = termino.strip()

        if not termino:
            return None, []

        return self.memory_service.obtener_relacionados(
            termino
        )

    def obtener_todo(self):
        """
        Devuelve todos los recuerdos.
        """

        return self.memory_service.obtener_todo()

    def buscar_por_importancia(
        self,
        minimo: int
    ):
        """
        Devuelve recuerdos con importancia mínima.
        """

        return self.memory_service.buscar_por_importancia(
            minimo
        )

    def buscar_por_tipo(
        self,
        tipo: str
    ):
        """
        Devuelve recuerdos de un tipo determinado.
        """

        self._validar_texto(
            tipo,
            "tipo"
        )

        return self.memory_service.buscar_por_tipo(
            tipo
        )

    def eliminar(
        self,
        termino: str
    ):
        """
        Elimina el primer recuerdo coincidente.
        """

        self._validar_texto(
            termino,
            "termino"
        )

        termino = termino.strip()

        if not termino:
            return None

        return self.memory_service.eliminar(
            termino
        )

    def limpiar(self):
        """
        Elimina toda la memoria.
        """

        return self.memory_service.limpiar()

    @staticmethod
    def _validar_texto(
        valor,
        nombre: str
    ):
        """
        Valida un parámetro de texto.
        """

        if not isinstance(
            valor,
            str
        ):
            raise TypeError(
                f"{nombre} debe ser un texto"
            )