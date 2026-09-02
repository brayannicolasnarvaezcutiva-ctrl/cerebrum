"""
CEREBRUM
Sistema básico de representación de conocimiento.

v0.0.5 Alpha - Cognitive Core
"""

from dataclasses import dataclass


@dataclass
class KnowledgeFact:
    """Representa un hecho conocido."""

    sujeto: str
    relacion: str
    objeto: str
    confianza: float = 1.0


class KnowledgeBase:
    """Gestiona hechos estructurados de conocimiento."""

    def __init__(self):
        self.facts: list[KnowledgeFact] = []

    def agregar(
        self,
        sujeto: str,
        relacion: str,
        objeto: str,
        confianza: float = 1.0
    ):
        """Agrega un hecho evitando duplicados."""

        sujeto = sujeto.strip().lower()
        relacion = relacion.strip().lower()
        objeto = objeto.strip().lower()

        confianza = max(
            0.0,
            min(1.0, float(confianza))
        )

        if not sujeto or not relacion or not objeto:
            return None

        for fact in self.facts:
            if (
                fact.sujeto == sujeto
                and fact.relacion == relacion
                and fact.objeto == objeto
            ):
                if confianza > fact.confianza:
                    fact.confianza = confianza

                return fact

        fact = KnowledgeFact(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto,
            confianza=confianza
        )

        self.facts.append(fact)

        return fact

    def buscar(
        self,
        sujeto=None,
        relacion=None,
        objeto=None
    ):
        """Busca hechos que coincidan con los filtros."""

        sujeto = (
            sujeto.strip().lower()
            if sujeto
            else None
        )

        relacion = (
            relacion.strip().lower()
            if relacion
            else None
        )

        objeto = (
            objeto.strip().lower()
            if objeto
            else None
        )

        resultados = []

        for fact in self.facts:

            if sujeto is not None:
                if fact.sujeto != sujeto:
                    continue

            if relacion is not None:
                if fact.relacion != relacion:
                    continue

            if objeto is not None:
                if fact.objeto != objeto:
                    continue

            resultados.append(fact)

        return sorted(
            resultados,
            key=lambda fact: fact.confianza,
            reverse=True
        )

    def existe(
        self,
        sujeto,
        relacion,
        objeto
    ):
        """Comprueba si existe un hecho."""

        return bool(
            self.buscar(
                sujeto=sujeto,
                relacion=relacion,
                objeto=objeto
            )
        )

    def eliminar(
        self,
        sujeto,
        relacion,
        objeto
    ):
        """Elimina un hecho específico."""

        resultados = self.buscar(
            sujeto=sujeto,
            relacion=relacion,
            objeto=objeto
        )

        if not resultados:
            return False

        fact = resultados[0]

        self.facts.remove(fact)

        return True

    def obtener_todo(self):
        """Devuelve todos los hechos."""

        return list(self.facts)

    def limpiar(self):
        """Elimina todo el conocimiento."""

        self.facts.clear()