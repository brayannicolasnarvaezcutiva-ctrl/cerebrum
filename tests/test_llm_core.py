"""
Pruebas del LLM Core.

CEREBRUM v0.0.6 Alpha
"""

from src.brain.cognitive_engine import CognitiveEngine
from src.brain.cognitive_llm_bridge import CognitiveLLMBridge

from src.brain.llm import LLMRequest, LLMResponse
from src.brain.llm_config import LLMConfig
from src.brain.llm_context import LLMContext
from src.brain.llm_context_builder import LLMContextBuilder
from src.brain.llm_conversation import LLMConversation
from src.brain.llm_engine import LLMEngine
from src.brain.llm_factory import LLMFactory
from src.brain.llm_manager import LLMManager
from src.brain.llm_response_formatter import LLMResponseFormatter
from src.brain.llm_service import LLMService

from src.brain.mock_llm import MockLLMProvider


def test_llm_context_construye():
    contexto = LLMContext(
        mensaje="Hola",
        memoria=["memoria 1"],
        conocimiento=["dato 1"],
        razonamiento=["inferencia 1"],
        instrucciones="Responde claro"
    )

    resultado = contexto.construir()

    assert "Hola" in resultado
    assert "memoria 1" in resultado
    assert "dato 1" in resultado
    assert "inferencia 1" in resultado
    assert "Responde claro" in resultado


def test_context_builder_elimina_duplicados():
    builder = LLMContextBuilder()

    contexto = builder.construir(
        mensaje="Hola",
        memoria=["dato", "dato", "   "],
        conocimiento=["x", "x"],
        razonamiento=["y", "y"]
    )

    assert contexto.memoria == ["dato"]
    assert contexto.conocimiento == ["x"]
    assert contexto.razonamiento == ["y"]


def test_context_builder_incluye_conversacion():
    builder = LLMContextBuilder()

    contexto = builder.construir(
        mensaje="¿Recuerdas?",
        conversacion=(
            "usuario: Hola\n"
            "asistente: Hola"
        )
    )

    resultado = contexto.construir()

    assert "Historial de conversación:" in resultado
    assert "usuario: Hola" in resultado
    assert "asistente: Hola" in resultado


def test_llm_conversation_agrega_mensajes():
    conversation = LLMConversation()

    usuario = conversation.agregar_usuario(
        "Hola CEREBRUM"
    )

    asistente = conversation.agregar_asistente(
        "Hola"
    )

    assert usuario is not None
    assert asistente is not None
    assert len(conversation.obtener_todo()) == 2


def test_llm_conversation_rechaza_roles_invalidos():
    conversation = LLMConversation()

    resultado = conversation.agregar(
        "robot",
        "Mensaje"
    )

    assert resultado is None
    assert conversation.obtener_todo() == []


def test_llm_conversation_limita_historial():
    conversation = LLMConversation(
        max_mensajes=2
    )

    conversation.agregar_usuario("uno")
    conversation.agregar_asistente("dos")
    conversation.agregar_usuario("tres")

    mensajes = conversation.obtener_todo()

    assert len(mensajes) == 2
    assert mensajes[0].contenido == "dos"
    assert mensajes[1].contenido == "tres"


def test_llm_request_construye_prompt():
    contexto = LLMContext(
        mensaje="Hola CEREBRUM"
    )

    request = LLMRequest(
        contexto=contexto
    )

    assert "Hola CEREBRUM" in request.construir_prompt()


def test_mock_provider_genera_respuesta():
    contexto = LLMContext(
        mensaje="Hola CEREBRUM"
    )

    request = LLMRequest(
        contexto=contexto
    )

    provider = MockLLMProvider()

    respuesta = provider.generar(request)

    assert isinstance(respuesta, LLMResponse)
    assert respuesta.modelo == "mock-llm"
    assert respuesta.confianza == 1.0
    assert "Hola CEREBRUM" in respuesta.contenido


def test_llm_engine_guarda_ultima_respuesta():
    config = LLMConfig(
        proveedor="mock"
    )

    engine = LLMEngine.desde_config(config)

    request = LLMRequest(
        contexto=LLMContext(
            mensaje="Hola"
        )
    )

    respuesta = engine.generar(request)

    assert engine.obtener_ultima_respuesta() == respuesta


def test_factory_crea_mock():
    config = LLMConfig(
        proveedor="mock",
        modelo="test-model"
    )

    provider = LLMFactory.crear(config)

    assert isinstance(provider, MockLLMProvider)
    assert provider.modelo == "test-model"


def test_factory_rechaza_proveedor_desconocido():
    config = LLMConfig(
        proveedor="inventado"
    )

    try:
        LLMFactory.crear(config)
    except ValueError as error:
        assert "no soportado" in str(error)
    else:
        raise AssertionError(
            "La factory debía rechazar el proveedor."
        )


def test_llm_service_genera_texto():
    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    resultado = service.generar_texto(
        "Hola CEREBRUM"
    )

    assert isinstance(resultado, str)
    assert "Hola CEREBRUM" in resultado


def test_llm_service_guarda_conversacion():
    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    service.generar_texto(
        "Hola CEREBRUM"
    )

    historial = (
        service
        .obtener_conversacion()
        .obtener_todo()
    )

    assert len(historial) == 2
    assert historial[0].rol == "usuario"
    assert historial[1].rol == "asistente"


def test_llm_service_conversacion_acumulada():
    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    service.generar_texto("Primer mensaje")
    service.generar_texto("Segundo mensaje")

    historial = (
        service
        .obtener_conversacion()
        .obtener_todo()
    )

    assert len(historial) == 4
    assert historial[0].contenido == "Primer mensaje"
    assert historial[2].contenido == "Segundo mensaje"


def test_llm_service_puede_limpiar_conversacion():
    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    service.generar_texto("Hola")

    service.limpiar_conversacion()

    assert (
        service
        .obtener_conversacion()
        .obtener_todo()
        == []
    )


def test_response_formatter():
    formatter = LLMResponseFormatter()

    respuesta = LLMResponse(
        contenido="  Hola  ",
        modelo="test",
        confianza=1.0
    )

    assert formatter.formatear(
        respuesta
    ) == "Hola"


def test_llm_manager():
    manager = LLMManager(
        LLMConfig(
            proveedor="mock",
            modelo="manager-test"
        )
    )

    assert isinstance(
        manager.obtener_proveedor(),
        MockLLMProvider
    )

    respuesta = manager.generar_texto(
        "Hola"
    )

    assert "Hola" in respuesta


def test_llm_manager_cambia_configuracion():
    manager = LLMManager()

    manager.cambiar_configuracion(
        LLMConfig(
            proveedor="mock",
            modelo="nuevo-modelo"
        )
    )

    assert (
        manager.obtener_configuracion().modelo
        == "nuevo-modelo"
    )

    assert isinstance(
        manager.obtener_proveedor(),
        MockLLMProvider
    )


def test_cognitive_llm_bridge_genera_respuesta():
    cognitive = CognitiveEngine()

    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    bridge = CognitiveLLMBridge(
        cognitive_engine=cognitive,
        llm_service=service
    )

    respuesta = bridge.generar(
        "CEREBRUM es inteligencia artificial"
    )

    assert isinstance(
        respuesta,
        LLMResponse
    )

    assert (
        "CEREBRUM es inteligencia artificial"
        in respuesta.contenido
    )


def test_cognitive_llm_bridge_incluye_inferencia():
    cognitive = CognitiveEngine()

    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    bridge = CognitiveLLMBridge(
        cognitive_engine=cognitive,
        llm_service=service
    )

    bridge.generar(
        "CEREBRUM es inteligencia artificial"
    )

    respuesta = bridge.generar(
        "inteligencia artificial es software"
    )

    assert "cerebrum es software" in (
        respuesta.contenido.lower()
    )


def test_cognitive_llm_bridge_mantiene_conversacion():
    cognitive = CognitiveEngine()

    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    bridge = CognitiveLLMBridge(
        cognitive_engine=cognitive,
        llm_service=service
    )

    bridge.generar(
        "Primer mensaje"
    )

    bridge.generar(
        "Segundo mensaje"
    )

    historial = (
        service
        .obtener_conversacion()
        .construir_contexto()
    )

    assert "usuario: Primer mensaje" in historial
    assert "usuario: Segundo mensaje" in historial
from src.brain.llm_orchestrator import LLMOrchestrator


def test_llm_orchestrator_procesa():
    cognitive = CognitiveEngine()

    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    orchestrator = LLMOrchestrator(
        cognitive_engine=cognitive,
        llm_service=service
    )

    respuesta = orchestrator.procesar(
        "CEREBRUM es inteligencia artificial"
    )

    assert isinstance(
        respuesta,
        LLMResponse
    )

    assert (
        "CEREBRUM es inteligencia artificial"
        in respuesta.contenido
    )


def test_llm_orchestrator_incluye_conocimiento():
    cognitive = CognitiveEngine()

    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    orchestrator = LLMOrchestrator(
        cognitive_engine=cognitive,
        llm_service=service
    )

    orchestrator.procesar(
        "CEREBRUM es inteligencia artificial"
    )

    respuesta = orchestrator.procesar(
        "inteligencia artificial es software"
    )

    contenido = respuesta.contenido.lower()

    assert "inteligencia artificial es software" in contenido
    assert "cerebrum es software" in contenido


def test_llm_orchestrator_mantiene_historial():
    cognitive = CognitiveEngine()

    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    orchestrator = LLMOrchestrator(
        cognitive_engine=cognitive,
        llm_service=service
    )

    orchestrator.procesar("Primer mensaje")
    orchestrator.procesar("Segundo mensaje")

    historial = (
        service
        .obtener_conversacion()
        .construir_contexto()
    )

    assert "usuario: Primer mensaje" in historial
    assert "usuario: Segundo mensaje" in historial
from src.brain.llm_errors import (
    LLMProviderError,
    LLMResponseError,
)


class FailingProvider:
    def generar(self, request):
        raise RuntimeError("fallo de prueba")


class NoneProvider:
    def generar(self, request):
        return None


class InvalidResponseProvider:
    def generar(self, request):
        return "respuesta inválida"


def test_llm_engine_convierte_error_del_proveedor():
    engine = LLMEngine(
        provider=FailingProvider(),
        config=LLMConfig(proveedor="mock")
    )

    request = LLMRequest(
        contexto=LLMContext(
            mensaje="Hola"
        )
    )

    try:
        engine.generar(request)
    except LLMProviderError as error:
        assert "fallo de prueba" in str(error)
    else:
        raise AssertionError(
            "Se esperaba LLMProviderError."
        )


def test_llm_engine_rechaza_respuesta_none():
    engine = LLMEngine(
        provider=NoneProvider(),
        config=LLMConfig(proveedor="mock")
    )

    request = LLMRequest(
        contexto=LLMContext(
            mensaje="Hola"
        )
    )

    try:
        engine.generar(request)
    except LLMResponseError:
        pass
    else:
        raise AssertionError(
            "Se esperaba LLMResponseError."
        )


def test_llm_engine_rechaza_tipo_de_respuesta_invalido():
    engine = LLMEngine(
        provider=InvalidResponseProvider(),
        config=LLMConfig(proveedor="mock")
    )

    request = LLMRequest(
        contexto=LLMContext(
            mensaje="Hola"
        )
    )

    try:
        engine.generar(request)
    except LLMResponseError:
        pass
    else:
        raise AssertionError(
            "Se esperaba LLMResponseError."
        )
from src.brain.cognitive_prompt_builder import CognitivePromptBuilder
from src.brain.llm_context_limits import LLMContextLimits


def test_context_limits_limita_lista():
    limits = LLMContextLimits(
        max_memory_items=2
    )

    resultado = limits.limitar_lista(
        ["uno", "dos", "tres"],
        2
    )

    assert resultado == ["uno", "dos"]


def test_context_limits_elimina_duplicados():
    limits = LLMContextLimits()

    resultado = limits.limitar_lista(
        ["uno", "uno", "dos"],
        10
    )

    assert resultado == ["uno", "dos"]


def test_context_limits_limita_caracteres():
    limits = LLMContextLimits(
        max_characters=20
    )

    resultado = limits.limitar_contexto(
        "abcdefghijklmnopqrstuvwxyz"
    )

    assert len(resultado) == 20


def test_cognitive_prompt_builder_limita_prompt():
    limits = LLMContextLimits(
        max_characters=100
    )

    builder = CognitivePromptBuilder(
        limits=limits
    )

    contexto = LLMContext(
        mensaje="Hola CEREBRUM",
        memoria=[
            "Este es un dato bastante largo que ocupa espacio."
        ]
    )

    prompt = builder.construir(
        contexto
    )

    assert len(prompt) <= 100


def test_cognitive_prompt_builder_omite_datos_invalidos():
    limits = LLMContextLimits()

    builder = CognitivePromptBuilder(
        limits=limits
    )

    contexto = LLMContext(
        mensaje="Hola",
        memoria=[
            "dato válido",
            "",
            "   "
        ]
    )

    prompt = builder.construir(
        contexto
    )

    assert "dato válido" in prompt
    assert prompt.count("dato válido") == 1
from src.brain.llm_errors import LLMResponseError


def test_llm_service_rechaza_mensaje_vacio():
    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    try:
        service.generar("")
    except LLMResponseError as error:
        assert "no puede estar vacío" in str(error)
    else:
        raise AssertionError(
            "Se esperaba LLMResponseError."
        )


def test_llm_service_rechaza_mensaje_solo_espacios():
    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    try:
        service.generar("     ")
    except LLMResponseError as error:
        assert "no puede estar vacío" in str(error)
    else:
        raise AssertionError(
            "Se esperaba LLMResponseError."
        )


def test_llm_service_rechaza_mensaje_no_texto():
    engine = LLMEngine.desde_config(
        LLMConfig(proveedor="mock")
    )

    service = LLMService(engine)

    try:
        service.generar(None)
    except LLMResponseError as error:
        assert "debe ser texto" in str(error)
    else:
        raise AssertionError(
            "Se esperaba LLMResponseError."
        )
from src.brain.llm_environment import LLMEnvironment


def test_llm_environment_valores_por_defecto(monkeypatch):
    monkeypatch.delenv(
        "CEREBRUM_LLM_PROVIDER",
        raising=False
    )

    monkeypatch.delenv(
        "CEREBRUM_LLM_MODEL",
        raising=False
    )

    monkeypatch.delenv(
        "CEREBRUM_LLM_TEMPERATURE",
        raising=False
    )

    monkeypatch.delenv(
        "CEREBRUM_LLM_MAX_TOKENS",
        raising=False
    )

    config = LLMEnvironment.cargar()

    assert config.proveedor == "mock"
    assert config.modelo == "mock-llm"
    assert config.temperatura == 0.7
    assert config.max_tokens == 1000


def test_llm_environment_carga_variables(monkeypatch):
    monkeypatch.setenv(
        "CEREBRUM_LLM_PROVIDER",
        "mock"
    )

    monkeypatch.setenv(
        "CEREBRUM_LLM_MODEL",
        "cerebrum-test"
    )

    monkeypatch.setenv(
        "CEREBRUM_LLM_TEMPERATURE",
        "0.9"
    )

    monkeypatch.setenv(
        "CEREBRUM_LLM_MAX_TOKENS",
        "500"
    )

    config = LLMEnvironment.cargar()

    assert config.proveedor == "mock"
    assert config.modelo == "cerebrum-test"
    assert config.temperatura == 0.9
    assert config.max_tokens == 500
from src.brain.llm_manager import LLMManager


def test_llm_manager_desde_entorno(monkeypatch):
    monkeypatch.setenv(
        "CEREBRUM_LLM_PROVIDER",
        "mock"
    )

    monkeypatch.setenv(
        "CEREBRUM_LLM_MODEL",
        "entorno-test"
    )

    manager = LLMManager.desde_entorno()

    assert manager.obtener_configuracion().proveedor == "mock"
    assert manager.obtener_configuracion().modelo == "entorno-test"
    assert isinstance(
        manager.obtener_proveedor(),
        MockLLMProvider
    )
def test_cerebrum_llm_procesa():
    from src.brain.cerebrum_llm import CerebrumLLM

    cognitive = CognitiveEngine()

    manager = LLMManager(
        LLMConfig(proveedor="mock")
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager
    )

    respuesta = cerebrum.procesar(
        "CEREBRUM es inteligencia artificial"
    )

    assert isinstance(
        respuesta,
        LLMResponse
    )

    assert (
        "CEREBRUM es inteligencia artificial"
        in respuesta.contenido
    )


def test_cerebrum_llm_responder():
    from src.brain.cerebrum_llm import CerebrumLLM

    cognitive = CognitiveEngine()

    manager = LLMManager(
        LLMConfig(proveedor="mock")
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager
    )

    respuesta = cerebrum.responder(
        "Hola CEREBRUM"
    )

    assert isinstance(
        respuesta,
        str
    )

    assert "Hola CEREBRUM" in respuesta


def test_cerebrum_llm_integra_inferencia():
    from src.brain.cerebrum_llm import CerebrumLLM

    cognitive = CognitiveEngine()

    manager = LLMManager(
        LLMConfig(proveedor="mock")
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager
    )

    cerebrum.responder(
        "CEREBRUM es inteligencia artificial"
    )

    respuesta = cerebrum.responder(
        "inteligencia artificial es software"
    )

    assert "cerebrum es software" in (
        respuesta.lower()
    )


def test_cerebrum_llm_limpia_conversacion():
    from src.brain.cerebrum_llm import CerebrumLLM

    manager = LLMManager(
        LLMConfig(proveedor="mock")
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=manager
    )

    cerebrum.responder("Hola")

    assert (
        manager
        .obtener_sesion()
        .cantidad_mensajes()
        == 2
    )

    cerebrum.limpiar_conversacion()

    assert (
        manager
        .obtener_sesion()
        .cantidad_mensajes()
        == 0
    )
def test_openai_provider_construye_request():
    from src.brain.openai_provider import OpenAIProvider

    class FakeResponse:
        output_text = "Respuesta de prueba"

    class FakeResponses:
        def __init__(self):
            self.argumentos = None

        def create(self, **kwargs):
            self.argumentos = kwargs
            return FakeResponse()

    class FakeClient:
        def __init__(self):
            self.responses = FakeResponses()

    provider = OpenAIProvider.__new__(
        OpenAIProvider
    )

    provider.modelo = "modelo-test"
    provider.max_tokens = 500
    provider.api_key = "fake-key"
    provider.client = FakeClient()

    request = LLMRequest(
        contexto=LLMContext(
            mensaje="Hola CEREBRUM"
        ),
        temperatura=0.8
    )

    respuesta = provider.generar(request)

    argumentos = provider.client.responses.argumentos

    assert respuesta.contenido == "Respuesta de prueba"
    assert argumentos["model"] == "modelo-test"
    assert argumentos["input"] == "=== MENSAJE DEL USUARIO ===\nHola CEREBRUM"
    assert argumentos["temperature"] == 0.8
    assert argumentos["max_output_tokens"] == 500
def test_llm_factory_openai_requires_online():
    config = LLMConfig(
        proveedor="openai",
        modo="local"
    )

    try:
        LLMFactory.crear(config)
    except ValueError as error:
        assert "modo='online'" in str(error)
    else:
        raise AssertionError(
            "OpenAI debía requerir modo online."
        )


def test_llm_config_rechaza_modo_invalido():
    try:
        LLMConfig(
            proveedor="mock",
            modo="invalido"
        )
    except ValueError as error:
        assert "Modo LLM no válido" in str(error)
    else:
        raise AssertionError(
            "Se esperaba ValueError."
        )


def test_llm_manager_desde_entorno_usa_configuracion(monkeypatch):
    monkeypatch.setenv(
        "CEREBRUM_LLM_PROVIDER",
        "mock"
    )

    monkeypatch.setenv(
        "CEREBRUM_LLM_MODEL",
        "diagnostic-model"
    )

    manager = LLMManager.desde_entorno()

    config = manager.obtener_configuracion()

    assert config.proveedor == "mock"
    assert config.modelo == "diagnostic-model"

    assert isinstance(
        manager.obtener_proveedor(),
        MockLLMProvider
    )
def test_cerebrum_llm_flujo_completo():
    from src.brain.cerebrum_llm import CerebrumLLM

    manager = LLMManager(
        LLMConfig(
            proveedor="mock",
            modelo="cerebrum-e2e"
        )
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=manager
    )

    primera = cerebrum.responder(
        "CEREBRUM es inteligencia artificial"
    )

    segunda = cerebrum.responder(
        "inteligencia artificial es software"
    )

    assert "CEREBRUM es inteligencia artificial" in primera

    assert (
        "cerebrum es software"
        in segunda.lower()
    )

    assert (
        manager.obtener_sesion().cantidad_mensajes()
        == 4
    )