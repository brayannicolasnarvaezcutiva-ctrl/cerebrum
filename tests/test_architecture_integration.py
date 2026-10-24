"""Pruebas de integración para los límites consolidados hacia v0.1.0."""

from importlib import import_module

import pytest

from brain.cognitive_context_retriever import CognitiveContextRetriever
from brain.cognitive_engine import CognitiveEngine
from brain.knowledge import KnowledgeBase
from brain.knowledge_inference import KnowledgeInference
from brain.llm import LLMProvider, LLMRequest
from brain.llm_config import LLMConfig
from brain.llm_engine import LLMEngine
from brain.llm_errors import LLMProviderError
from brain.llm_service import LLMService
from brain.memory import Memory
from brain.memory_knowledge_bridge import MemoryKnowledgeBridge
from brain.memory_service import MemoryService
from brain.reasoning import ReasoningEngine, ReasoningResult as LegacyAlias
from brain.reasoning_result import ReasoningResult
from brain.reasoning_validator import ReasoningValidator


def test_reasoning_result_es_unico_y_compatible_con_el_motor_clasico():
    resultado = ReasoningEngine().analizar("premisa de prueba")

    assert LegacyAlias is ReasoningResult
    assert isinstance(resultado, ReasoningResult)
    assert resultado.conclusion
    assert resultado.tuvo_resultados is True


def test_reasoning_result_acepta_las_firmas_posicionales_historicas():
    clasico = ReasoningResult("conclusión", ["evidencia"], 0.8)
    estructurado = ReasoningResult([], 0.6, True, False, [])

    assert (clasico.conclusion, clasico.evidencia, clasico.confianza) == (
        "conclusión", ["evidencia"], 0.8
    )
    assert (
        estructurado.conclusiones,
        estructurado.confianza,
        estructurado.valido
    ) == ([], 0.6, True)


def test_cognitive_engine_expone_resultado_estructurado_al_contexto():
    engine = CognitiveEngine()

    engine.procesar("cerebrum es inteligencia artificial")
    resultado = engine.procesar("inteligencia artificial es software")

    razonamiento = resultado.resultado_razonamiento

    assert razonamiento is not None
    assert razonamiento.valido is True
    assert any(
        explicacion.conclusion.sujeto == "cerebrum"
        and explicacion.conclusion.objeto == "software"
        for explicacion in razonamiento.conclusiones
    )

    contexto = CognitiveContextRetriever(engine).recuperar(
        resultado.intencion,
        resultado_razonamiento=razonamiento
    )

    assert "cerebrum es software" in contexto["razonamiento"]


def test_razonamiento_estructurado_reporta_conflictos():
    engine = CognitiveEngine()

    engine.aprender("cerebrum es software")
    engine.aprender("cerebrum es inteligencia")
    engine.aprender("inteligencia es hardware")

    resultado = engine.razonar()
    validacion = ReasoningValidator().validar_resultado(resultado)

    assert resultado.tiene_conflicto is True
    assert resultado.valido is False
    assert any(conflicto.objeto == "software" for conflicto in resultado.conflictos)
    assert validacion["tipo"] == "con_conflicto"


def test_knowledge_inference_no_duplica_hechos_almacenados():
    knowledge = KnowledgeBase()
    knowledge.agregar("a", "es", "b")
    knowledge.agregar("b", "es", "c")
    inference = KnowledgeInference(knowledge)

    primeros = inference.inferir_todo()
    segundos = inference.inferir_todo()

    assert [(fact.sujeto, fact.objeto) for fact in primeros] == [("a", "c")]
    assert segundos == []


def test_memory_knowledge_bridge_convierte_recuerdos_en_texto(tmp_path):
    memory = Memory(tmp_path / "memory.json")
    service = MemoryService(memory)
    memory.guardar("cerebrum es software", importancia=4)
    bridge = MemoryKnowledgeBridge(service, KnowledgeBase())

    assert bridge.recuperar("cerebrum") == ["cerebrum es software"]

    hechos = bridge.aprender_desde_memoria("cerebrum")

    assert [(fact.sujeto, fact.relacion, fact.objeto) for fact in hechos] == [
        ("cerebrum", "es", "software")
    ]


def test_memory_service_delega_la_decision_automatica_a_su_politica(tmp_path):
    class Policy:
        def __init__(self):
            self.calls = []

        def guardar_si_corresponde(self, service, text):
            self.calls.append((service, text))
            return "guardado"

    policy = Policy()
    service = MemoryService(
        Memory(tmp_path / "memory.json"),
        memory_policy=policy
    )

    assert service.guardar_si_importante("mi proyecto es cerebrum") == "guardado"
    assert policy.calls == [(service, "mi proyecto es cerebrum")]


class _BrokenProvider(LLMProvider):
    def generar(self, request: LLMRequest):
        raise RuntimeError("fallo de proveedor")


def test_llm_service_revierte_el_turno_si_el_proveedor_falla():
    engine = LLMEngine(
        provider=_BrokenProvider(),
        config=LLMConfig(proveedor="mock")
    )
    service = LLMService(engine)

    with pytest.raises(LLMProviderError):
        service.generar("hola")

    assert service.obtener_sesion().cantidad_mensajes() == 0


def test_entry_point_principal_es_importable_desde_el_paquete_instalado():
    main = import_module("main")

    assert callable(main.main)
