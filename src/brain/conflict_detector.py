"""
CEREBRUM
Detector de contradicciones en conocimiento.

v0.0.9 Alpha - Reasoning Upgrade
"""

from .knowledge import KnowledgeBase, KnowledgeFact


class ConflictDetector:
    """
    Detecta si una conclusión entra en conflicto
    con hechos ya existentes en la base de conocimiento.
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase
    ):
        self.knowledge_base = knowledge_base

    def detectar(
        self,
        conclusion: KnowledgeFact
    ) -> list[KnowledgeFact]:
        """
        Devuelve hechos que contradicen la conclusión.

        Dos hechos se consideran conflictivos cuando:
        - tienen el mismo sujeto
        - tienen la misma relación
        - tienen diferente objeto
        """

        if not isinstance(
            conclusion,
            KnowledgeFact
        ):
            return []

        hechos = self.knowledge_base.buscar(
            sujeto=conclusion.sujeto,
            relacion=conclusion.relacion
        )

        conflictos = []

        for hecho in hechos:
            if not isinstance(
                hecho,
                KnowledgeFact
            ):
                continue

            if (
                hecho.objeto != conclusion.objeto
                and hecho != conclusion
            ):
                conflictos.append(
                    hecho
                )

        return conflictos

    def tiene_conflicto(
        self,
        conclusion: KnowledgeFact
    ) -> bool:
        """
        Indica si existe al menos una contradicción.
        """

        return bool(
            self.detectar(
                conclusion
            )
        )

    def evaluar(
        self,
        conclusion: KnowledgeFact
    ) -> dict:
        """
        Evalúa una conclusión y devuelve información
        sobre posibles conflictos.
        """

        conflictos = self.detectar(
            conclusion
        )

        return {
            "tiene_conflicto": bool(
                conflictos
            ),
            "cantidad": len(
                conflictos
            ),
            "conflictos": conflictos
        }