"""
CEREBRUM
Formateador de respuestas del procesador.

v0.0.4 Alpha - Reasoning Core
"""


class ResponseFormatter:
    """Convierte resultados de los sistemas internos en texto."""

    def formatear_solicitud_razonamiento(self, solicitud):
        """Convierte una solicitud de razonamiento en respuesta."""

        if solicitud.mensaje:
            return solicitud.mensaje

        return self.formatear_razonamiento(
            solicitud.resultado
        )

    def formatear_razonamiento(self, resultado):
        """Convierte un resultado de razonamiento en texto."""

        evidencia = resultado.evidencia

        if evidencia:
            texto_evidencia = "\n".join(
                f"- {dato}"
                for dato in evidencia
            )
        else:
            texto_evidencia = (
                "- No se encontró evidencia adicional."
            )

        return (
            f"Conclusión: {resultado.conclusion}\n"
            f"Evidencia:\n"
            f"{texto_evidencia}\n"
            f"Confianza: "
            f"{resultado.confianza:.0%}"
        )

    def formatear_recuerdos(self, recuerdos):
        """Convierte recuerdos en texto legible."""

        if not recuerdos:
            return "No tengo recuerdos registrados."

        resultado = []

        for recuerdo in recuerdos:
            resultado.append(
                f"[{recuerdo['id']}] "
                f"{recuerdo['contenido']} "
                f"(tipo: {recuerdo['tipo']}, "
                f"importancia: "
                f"{recuerdo['importancia']})"
            )

        return "\n".join(resultado)

    def formatear_relacionados(self, recuerdo, relacionados):
        """Convierte relaciones de memoria en texto."""

        if not relacionados:
            return (
                f"El recuerdo "
                f"'{recuerdo['contenido']}' "
                "no tiene relaciones registradas."
            )

        return "\n".join(
            f"- {item['contenido']} "
            f"(tipo: {item['tipo']})"
            for item in relacionados
        )

    def formatear_contexto(self, mensajes):
        """Convierte el contexto reciente en texto."""

        return "\n".join(
            f"- {mensaje}"
            for mensaje in mensajes
        )

    def formatear_tema(self, tema):
        """Convierte un tema del contexto en respuesta."""

        return (
            "El tema reciente parece ser: "
            f"{tema}"
        )

    def formatear_recuerdo(self, recuerdo):
        """Convierte un recuerdo recuperado en texto."""

        return f"Recuerdo: {recuerdo['contenido']}"

    def formatear_recuerdo_eliminado(self, recuerdo):
        """Convierte un recuerdo eliminado en texto."""

        return f"Recuerdo eliminado: {recuerdo['contenido']}"

    def formatear_guardado_manual(self, tipo, importancia):
        """Convierte un guardado manual en texto."""

        return (
            "Entendido. Lo guardaré "
            f"como {tipo} "
            f"(importancia {importancia})."
        )

    def formatear_nueva_memoria(self, recuerdo):
        """Convierte una memoria automática en texto."""

        return (
            "Entendido. Recordaré "
            f"{recuerdo['contenido']}."
        )

    def formatear_recuerdo_relacionado(self, recuerdo):
        """Convierte un recuerdo relacionado en texto."""

        return (
            "Recuerdo relacionado: "
            f"{recuerdo['contenido']}"
        )

    def formatear_repeticion(self, anterior):
        """Convierte una repetición de contexto en texto."""

        return (
            "Entiendo. Seguimos con "
            f"{anterior}."
        )
