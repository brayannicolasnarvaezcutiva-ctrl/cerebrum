"""
CEREBRUM
Inferencia sobre conocimiento estructurado.

v0.0.5 Alpha - Cognitive Core
"""

from .knowledge import KnowledgeBase, KnowledgeFact
from .novelty_detector import NoveltyDetector


class KnowledgeInference:
    """Genera nuevos hechos a partir del conocimiento existente."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.novelty = NoveltyDetector(knowledge_base)

    def inferir_es(self) -> list[KnowledgeFact]:
        """
        Aplica inferencia transitiva sobre la relación 'es'.

        Ejemplo:

            A es B
            B es C
            --------
            A es C
        """

        hechos = self.knowledge_base.obtener_todo()
        nuevos = []

        for primero in hechos:
            if primero.relacion != "es":
                continue

            for segundo in hechos:
                if segundo.relacion != "es":
                    continue

                if primero.objeto != segundo.sujeto:
                    continue

                if primero.sujeto == segundo.objeto:
                    continue

                # Creamos la posible conclusión sin modificar todavía
                candidato = KnowledgeFact(
                    sujeto=primero.sujeto,
                    relacion="es",
                    objeto=segundo.objeto,
                    confianza=min(
                        primero.confianza,
                        segundo.confianza
                    )
                )

                # Solo consideramos la conclusión
                # si todavía no estaba almacenada.
                if not self.knowledge_base.existe(
                    sujeto=candidato.sujeto,
                    relacion=candidato.relacion,
                    objeto=candidato.objeto
                ):
                    nuevo = self.knowledge_base.agregar(
                        sujeto=candidato.sujeto,
                        relacion=candidato.relacion,
                        objeto=candidato.objeto,
                        confianza=candidato.confianza
                    )

                    if nuevo is not None and nuevo not in nuevos:
                        nuevos.append(nuevo)

        return nuevos

    def inferir_todo(self) -> list[KnowledgeFact]:
        """Ejecuta todas las reglas de inferencia disponibles."""

        return self.inferir_es()