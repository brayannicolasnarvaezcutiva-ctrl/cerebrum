"""
CEREBRUM
Extractor básico de conocimiento desde lenguaje natural.

v0.0.5 Alpha - Cognitive Core
"""

import re

from .knowledge import KnowledgeBase, KnowledgeFact


class KnowledgeExtractor:
    """Extrae hechos estructurados desde frases simples."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def extraer(self, texto: str) -> KnowledgeFact | None:
        """
        Intenta convertir una frase en un hecho estructurado.

        Ejemplos:
            "CEREBRUM usa Python"
            -> cerebrum / usa / python

            "Mi proyecto es CEREBRUM"
            -> proyecto / es / cerebrum
        """

        if not isinstance(texto, str):
            return None

        texto = texto.strip()

        if not texto:
            return None

        texto = re.sub(r"\s+", " ", texto)
        texto = texto.rstrip(".!?")

        # ---------------------------------------------------------
        # Patrón 1:
        # "Mi proyecto es CEREBRUM"
        # ---------------------------------------------------------
        patron_proyecto = re.match(
            r"mi proyecto es (.+)",
            texto,
            re.IGNORECASE
        )

        if patron_proyecto:
            objeto = patron_proyecto.group(1).strip()

            return self.knowledge_base.agregar(
                sujeto="proyecto",
                relacion="es",
                objeto=objeto
            )

        # ---------------------------------------------------------
        # Patrón 2:
        # "X es Y"
        # ---------------------------------------------------------
        patron_es = re.match(
            r"(.+?)\s+es\s+(.+)",
            texto,
            re.IGNORECASE
        )

        if patron_es:
            sujeto = patron_es.group(1).strip()
            objeto = patron_es.group(2).strip()

            return self.knowledge_base.agregar(
                sujeto=sujeto,
                relacion="es",
                objeto=objeto
            )

        # ---------------------------------------------------------
        # Patrón 3:
        # "X usa Y"
        # ---------------------------------------------------------
        patron_usa = re.match(
            r"(.+?)\s+usa\s+(.+)",
            texto,
            re.IGNORECASE
        )

        if patron_usa:
            sujeto = patron_usa.group(1).strip()
            objeto = patron_usa.group(2).strip()

            return self.knowledge_base.agregar(
                sujeto=sujeto,
                relacion="usa",
                objeto=objeto
            )

        # ---------------------------------------------------------
        # Patrón 4:
        # "X tiene Y"
        # ---------------------------------------------------------
        patron_tiene = re.match(
            r"(.+?)\s+tiene\s+(.+)",
            texto,
            re.IGNORECASE
        )

        if patron_tiene:
            sujeto = patron_tiene.group(1).strip()
            objeto = patron_tiene.group(2).strip()

            return self.knowledge_base.agregar(
                sujeto=sujeto,
                relacion="tiene",
                objeto=objeto
            )

        # ---------------------------------------------------------
        # Patrón 5:
        # "X necesita Y"
        # ---------------------------------------------------------
        patron_necesita = re.match(
            r"(.+?)\s+necesita\s+(.+)",
            texto,
            re.IGNORECASE
        )

        if patron_necesita:
            sujeto = patron_necesita.group(1).strip()
            objeto = patron_necesita.group(2).strip()

            return self.knowledge_base.agregar(
                sujeto=sujeto,
                relacion="necesita",
                objeto=objeto
            )

        return None

    def extraer_varios(self, textos: list[str]):
        """Extrae conocimiento de varias frases."""

        resultados = []

        for texto in textos:
            fact = self.extraer(texto)

            if fact is not None:
                resultados.append(fact)

        return resultados