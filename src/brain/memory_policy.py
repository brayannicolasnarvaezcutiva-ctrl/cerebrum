"""
CEREBRUM
Política de decisión para memoria persistente.

v0.0.8 Alpha - Memory Bridge
"""


class MemoryPolicy:
    """
    Decide cuándo una entrada merece convertirse
    en memoria persistente.
    """

    TIPOS_IMPORTANTES = {
        "identidad",
        "proyecto",
        "objetivo",
        "preferencia"
    }

    def evaluar(
        self,
        memory_service,
        texto: str
    ) -> dict:
        """
        Evalúa una entrada y devuelve una decisión.

        Resultado:

        {
            "guardar": bool,
            "tipo": str,
            "importancia": int,
            "contenido": str
        }
        """

        if not isinstance(
            texto,
            str
        ):
            return {
                "guardar": False,
                "tipo": "general",
                "importancia": 1,
                "contenido": ""
            }

        texto = texto.strip()

        if not texto:
            return {
                "guardar": False,
                "tipo": "general",
                "importancia": 1,
                "contenido": ""
            }

        tipo = memory_service.clasificar_memoria(
            texto
        )

        importancia = memory_service.calcular_importancia(
            tipo
        )

        contenido = memory_service.extraer_contenido(
            texto
        )

        guardar = (
            tipo in self.TIPOS_IMPORTANTES
            and bool(contenido)
        )

        return {
            "guardar": guardar,
            "tipo": tipo,
            "importancia": importancia,
            "contenido": contenido
        }

    def guardar_si_corresponde(
        self,
        memory_service,
        texto: str
    ):
        """
        Evalúa una entrada y la guarda solamente
        si la política lo considera importante.
        """

        evaluacion = self.evaluar(
            memory_service,
            texto
        )

        if not evaluacion["guardar"]:
            return None

        return memory_service.memory.guardar(
            evaluacion["contenido"],
            tipo=evaluacion["tipo"],
            importancia=evaluacion["importancia"]
        )