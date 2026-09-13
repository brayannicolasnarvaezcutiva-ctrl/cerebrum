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
from src.brain.intent import Intent
from src.brain.cognitive_context_selector import CognitiveContextSelector
from src.brain.cerebrum_llm import CerebrumLLM

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
def test_cognitive_context_retriever_recupera_conocimiento():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )
    from src.brain.intent_detector import IntentDetector

    cognitive = CognitiveEngine()

    cognitive.knowledge_base.agregar(
        "estrella",
        "es",
        "una esfera de plasma"
    )

    cognitive.knowledge_base.agregar(
        "estrella",
        "emite",
        "luz"
    )

    cognitive.knowledge_base.agregar(
        "marte",
        "es",
        "un planeta"
    )

    intencion = IntentDetector().detectar(
        "¿Qué es una estrella?"
    )

    retriever = CognitiveContextRetriever(
        cognitive
    )

    resultado = retriever.recuperar(
        intencion
    )

    assert (
        "estrella es una esfera de plasma"
        in resultado["conocimiento"]
    )

    assert (
        "estrella emite luz"
        in resultado["conocimiento"]
    )

    assert (
        "marte es un planeta"
        not in resultado["conocimiento"]
    )


def test_cognitive_context_retriever_respeta_limite():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )
    from src.brain.intent_detector import IntentDetector

    cognitive = CognitiveEngine()

    for i in range(5):
        cognitive.knowledge_base.agregar(
            "estrella",
            "dato",
            f"informacion {i}"
        )

    intencion = IntentDetector().detectar(
        "¿Qué es una estrella?"
    )

    retriever = CognitiveContextRetriever(
        cognitive,
        limite=2
    )

    resultado = retriever.recuperar(
        intencion
    )

    assert len(
        resultado["conocimiento"]
    ) == 2


def test_cognitive_context_retriever_devuelve_estructura():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )

    cognitive = CognitiveEngine()

    retriever = CognitiveContextRetriever(
        cognitive
    )

    resultado = retriever.recuperar(
        None
    )

    assert set(resultado.keys()) == {
        "memoria",
        "conocimiento",
        "razonamiento",
        "conversacion"
    }

    assert resultado["memoria"] == []
    assert resultado["conocimiento"] == []
    assert resultado["razonamiento"] == []
    assert resultado["conversacion"] == ""
     
def test_cognitive_context_retriever_recupera_conversacion():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )
    from src.brain.intent_detector import IntentDetector

    cognitive = CognitiveEngine()

    intencion = IntentDetector().detectar(
        "¿Qué es una estrella?"
    )

    retriever = CognitiveContextRetriever(
        cognitive
    )

    resultado = retriever.recuperar(
        intencion,
        conversacion=(
            "usuario: Hola\n"
            "asistente: Hola"
        )
    )

    assert (
        resultado["conversacion"]
        == "usuario: Hola\nasistente: Hola"
    )


def test_cognitive_context_retriever_omite_conversacion_si_no_corresponde():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )
    from src.brain.intent import Intent

    cognitive = CognitiveEngine()

    intencion = Intent(
        tipo="comando",
        accion="resolver",
        tema="ecuacion"
    )

    retriever = CognitiveContextRetriever(
        cognitive
    )

    resultado = retriever.recuperar(
        intencion,
        conversacion="usuario: esto no debería entrar"
    )

    assert resultado["conversacion"] == ""


def test_cognitive_context_retriever_estructura_completa():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )

    cognitive = CognitiveEngine()

    retriever = CognitiveContextRetriever(
        cognitive
    )

    resultado = retriever.recuperar(
        None,
        conversacion="historial"
    )

    assert set(resultado.keys()) == {
        "memoria",
        "conocimiento",
        "razonamiento",
        "conversacion"
    }

    assert resultado["memoria"] == []
    assert resultado["conocimiento"] == []
    assert resultado["razonamiento"] == []
    assert resultado["conversacion"] == ""
     
def test_cerebrum_llm_flujo_end_to_end_v007():
    from src.brain.cerebrum_llm import CerebrumLLM

    manager = LLMManager(
        LLMConfig(
            proveedor="mock",
            modelo="cerebrum-v007"
        )
    )

    cognitive = CognitiveEngine()

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager
    )

    primera = cerebrum.responder(
        "CEREBRUM es inteligencia artificial"
    )

    segunda = cerebrum.responder(
        "inteligencia artificial es software"
    )

    assert isinstance(
        primera,
        str
    )

    assert isinstance(
        segunda,
        str
    )

    assert (
        "CEREBRUM es inteligencia artificial"
        in primera
    )

    historial = (
        manager
        .obtener_sesion()
        .obtener_contexto()
    )

    assert (
        "usuario: CEREBRUM es inteligencia artificial"
        in historial
    )

    assert (
        "usuario: inteligencia artificial es software"
        in historial
    )

    assert (
        manager
        .obtener_sesion()
        .cantidad_mensajes()
        == 4
    )

    intencion = (
        cognitive
        .obtener_ultima_intencion()
    )

    assert intencion is not None
    assert intencion.tipo == "afirmacion"
    
def test_cognitive_context_retriever_recupera_memoria_relevante():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )

    cognitive = CognitiveEngine()

    intencion = Intent(
        tipo="pregunta",
        accion="recordar",
        tema="estrella"
    )

    conversacion = (
        "usuario: Hola CEREBRUM\n"
        "asistente: Hola\n"
        "usuario: hablamos sobre una estrella\n"
        "asistente: sí, hablamos de astronomía"
    )

    retriever = CognitiveContextRetriever(
        cognitive
    )

    resultado = retriever.recuperar(
        intencion,
        conversacion=conversacion
    )

    assert len(
        resultado["memoria"]
    ) > 0

    assert any(
        "estrella" in linea.lower()
        for linea in resultado["memoria"]
    )


def test_cognitive_context_retriever_limita_memoria():
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )

    cognitive = CognitiveEngine()

    intencion = Intent(
        tipo="pregunta",
        accion="recordar",
        tema="estrella"
    )

    conversacion = "\n".join(
        [
            "usuario: estrella uno",
            "asistente: estrella dos",
            "usuario: estrella tres",
            "asistente: estrella cuatro"
        ]
    )

    retriever = CognitiveContextRetriever(
        cognitive,
        limite=2
    )

    resultado = retriever.recuperar(
        intencion,
        conversacion=conversacion
    )

    assert len(
        resultado["memoria"]
    ) <= 2

def test_cognitive_context_selector_explicacion():
    selector = CognitiveContextSelector()

    intencion = Intent(
        tipo="pregunta",
        accion="explicar",
        tema="astronomia"
    )

    resultado = selector.seleccionar(
        intencion
    )

    assert resultado == {
        "memoria": True,
        "conocimiento": True,
        "razonamiento": True,
        "conversacion": True
    }


def test_cognitive_context_selector_memoria():
    selector = CognitiveContextSelector()

    intencion = Intent(
        tipo="pregunta",
        accion="recordar",
        tema="astronomia"
    )

    resultado = selector.seleccionar(
        intencion
    )

    assert resultado == {
        "memoria": True,
        "conocimiento": False,
        "razonamiento": False,
        "conversacion": True
    }


def test_cognitive_context_selector_resolucion():
    selector = CognitiveContextSelector()

    intencion = Intent(
        tipo="comando",
        accion="resolver",
        tema="ecuacion"
    )

    resultado = selector.seleccionar(
        intencion
    )

    assert resultado == {
        "memoria": False,
        "conocimiento": True,
        "razonamiento": True,
        "conversacion": False
    }

def test_cognitive_strategy_router_explicacion():
    from src.brain.cognitive_strategy_router import (
        CognitiveStrategyRouter
    )

    router = CognitiveStrategyRouter()

    estrategia = router.enrutar(
        Intent(
            tipo="pregunta",
            accion="explicar",
            tema="estrella"
        )
    )

    assert estrategia == "explicacion"


def test_cognitive_strategy_router_memoria():
    from src.brain.cognitive_strategy_router import (
        CognitiveStrategyRouter
    )

    router = CognitiveStrategyRouter()

    estrategia = router.enrutar(
        Intent(
            tipo="pregunta",
            accion="recordar"
        )
    )

    assert estrategia == "memoria"


def test_cognitive_strategy_router_ninguna():
    from src.brain.cognitive_strategy_router import (
        CognitiveStrategyRouter
    )

    router = CognitiveStrategyRouter()

    assert (
        router.enrutar(None)
        == "respuesta_general"
    )


def test_cognitive_strategy_router_instrucciones():
    from src.brain.cognitive_strategy_router import (
        CognitiveStrategyRouter
    )

    router = CognitiveStrategyRouter()

    instrucciones = router.instrucciones(
        "resolucion"
    )

    assert (
        "paso a paso"
        in instrucciones
    )

def test_cerebrum_llm_selecciona_estrategia():
    from src.brain.cerebrum_llm import CerebrumLLM

    manager = LLMManager(
        LLMConfig(proveedor="mock")
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=manager
    )

    assert (
        cerebrum.obtener_estrategia(
            "¿Qué es una estrella?"
        )
        == "explicacion"
    )


def test_cerebrum_llm_contexto_recuperado():
    from src.brain.cerebrum_llm import CerebrumLLM

    cognitive = CognitiveEngine()

    cognitive.knowledge_base.agregar(
        "estrella",
        "es",
        "una esfera de plasma"
    )

    manager = LLMManager(
        LLMConfig(proveedor="mock")
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager
    )

    contexto = cerebrum.obtener_contexto_recuperado(
        "¿Qué es una estrella?"
    )

    assert (
        "estrella es una esfera de plasma"
        in contexto["conocimiento"]
    )


def test_cerebrum_llm_prompt_incluye_estrategia():
    from src.brain.cerebrum_llm import CerebrumLLM

    manager = LLMManager(
        LLMConfig(proveedor="mock")
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=manager
    )

    respuesta = cerebrum.responder(
        "¿Qué es una estrella?"
    )

    assert (
        "Estrategia de procesamiento: explicacion"
        in respuesta
    )

def test_cerebrum_v007_flujo_completo():
    from src.brain.cerebrum_llm import CerebrumLLM

    cognitive = CognitiveEngine()

    cognitive.knowledge_base.agregar(
        "estrella",
        "es",
        "una esfera de plasma",
        0.95
    )

    cognitive.knowledge_base.agregar(
        "estrella",
        "emite",
        "luz",
        0.90
    )

    manager = LLMManager(
        LLMConfig(
            proveedor="mock",
            modelo="cerebrum-v007"
        )
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager
    )

    respuesta = cerebrum.responder(
        "¿Qué es una estrella?"
    )

    assert isinstance(
        respuesta,
        str
    )

    assert (
        "Estrategia de procesamiento: explicacion"
        in respuesta
    )

    contexto = cerebrum.obtener_contexto_recuperado(
        "¿Qué es una estrella?"
    )

    assert (
        "estrella es una esfera de plasma"
        in contexto["conocimiento"]
    )

    assert (
        "estrella emite luz"
        in contexto["conocimiento"]
    )

    assert (
        cognitive
        .obtener_ultima_intencion()
        .accion
        == "explicar"
    )

    assert (
        manager
        .obtener_sesion()
        .cantidad_mensajes()
        == 2
    )

def test_memory_bridge_guardar_memoria_importante():
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_service import MemoryService
    from src.brain.memory import Memory

    memoria = Memory(
        file_path="data/test_memory_bridge.json"
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service
    )

    resultado = bridge.guardar(
        "mi proyecto es CEREBRUM"
    )

    assert resultado is not None
    assert resultado["contenido"] == "CEREBRUM"


def test_memory_bridge_recordar():
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_service import MemoryService
    from src.brain.memory import Memory

    memoria = Memory(
        file_path="data/test_memory_bridge.json"
    )

    memoria.guardar(
        "CEREBRUM",
        tipo="proyecto",
        importancia=5
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service
    )

    recuerdo = bridge.recordar(
        "CEREBRUM"
    )

    assert recuerdo is not None
    assert recuerdo["contenido"] == "CEREBRUM"


def test_memory_bridge_recuperar_relevante():
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_service import MemoryService
    from src.brain.memory import Memory

    memoria = Memory(
        file_path="data/test_memory_bridge.json"
    )

    memoria.guardar(
        "Estoy desarrollando CEREBRUM",
        tipo="proyecto",
        importancia=5
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service
    )

    recuerdos = bridge.recuperar_relevante(
        "CEREBRUM"
    )

    assert len(recuerdos) > 0


def test_memory_bridge_contexto_para():
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_service import MemoryService
    from src.brain.memory import Memory

    memoria = Memory(
        file_path="data/test_memory_bridge.json"
    )

    memoria.guardar(
        "Mi proyecto es CEREBRUM",
        tipo="proyecto",
        importancia=5
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service
    )

    contexto = bridge.contexto_para(
        "CEREBRUM"
    )

    assert len(contexto) > 0
    assert any(
        "CEREBRUM" in linea
        for linea in contexto
    )

def test_memory_bridge_obtener_contexto_limita():
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_service import MemoryService
    from src.brain.memory import Memory

    memoria = Memory(
        file_path="data/test_memory_bridge.json"
    )

    memoria.guardar(
        "CEREBRUM es un proyecto de inteligencia artificial",
        tipo="proyecto",
        importancia=5
    )

    memoria.guardar(
        "CEREBRUM tiene un sistema cognitivo",
        tipo="proyecto",
        importancia=4
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service
    )

    contexto = bridge.obtener_contexto(
        "CEREBRUM",
        limite=1
    )

    assert len(contexto) <= 1


def test_memory_bridge_contexto_para_devuelve_texto():
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_service import MemoryService
    from src.brain.memory import Memory

    memoria = Memory(
        file_path="data/test_memory_bridge.json"
    )

    memoria.guardar(
        "CEREBRUM es mi proyecto",
        tipo="proyecto",
        importancia=5
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service
    )

    contexto = bridge.contexto_para(
        "CEREBRUM"
    )

    assert isinstance(
        contexto,
        list
    )

    assert any(
        "CEREBRUM" in texto
        for texto in contexto
    )

def test_cerebrum_llm_integra_memory_bridge():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )
    from src.brain.cognitive_context_selector import (
        CognitiveContextSelector
    )

    memoria = Memory(
        file_path="data/test_cerebrum_memory_bridge.json"
    )

    memoria.guardar(
        "Mi proyecto es CEREBRUM",
        tipo="proyecto",
        importancia=5
    )

    memory_service = MemoryService(
        memory=memoria
    )

    memory_bridge = MemoryBridge(
        memory_service=memory_service
    )

    cognitive = CognitiveEngine()

    retriever = CognitiveContextRetriever(
        cognitive_engine=cognitive,
        selector=CognitiveContextSelector(),
        memory_bridge=memory_bridge
    )

    contexto = retriever.recuperar(
        Intent(
            tipo="pregunta",
            accion="recordar",
            tema="CEREBRUM"
        )
    )

    assert len(
        contexto["memoria"]
    ) > 0

    assert any(
        "CEREBRUM" in recuerdo
        for recuerdo in contexto["memoria"]
    )


def test_cerebrum_llm_contexto_recuperado_usa_memory_bridge():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.cognitive_context_retriever import (
        CognitiveContextRetriever
    )
    from src.brain.cognitive_context_selector import (
        CognitiveContextSelector
    )

    memoria = Memory(
        file_path="data/test_cerebrum_memory_bridge_2.json"
    )

    memoria.guardar(
        "Estoy construyendo CEREBRUM",
        tipo="proyecto",
        importancia=5
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    cognitive = CognitiveEngine()

    retriever = CognitiveContextRetriever(
        cognitive_engine=cognitive,
        selector=CognitiveContextSelector(),
        memory_bridge=bridge
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        context_retriever=retriever
    )

    intencion = Intent(
        tipo="pregunta",
        accion="recordar",
        tema="CEREBRUM"
    )

    contexto = (
        cerebrum
        .obtener_contexto_recuperado(
            intencion
        )
    )

    assert len(
        contexto["memoria"]
    ) > 0

    assert any(
        "CEREBRUM" in recuerdo
        for recuerdo in contexto["memoria"]
    )

def test_cerebrum_llm_expone_memory_bridge():
    from src.brain.memory_bridge import MemoryBridge

    cognitive = CognitiveEngine()

    manager = LLMManager(
        LLMConfig(
            proveedor="mock"
        )
    )

    bridge = MemoryBridge()

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager,
        memory_bridge=bridge
    )

    assert cerebrum.memory_bridge is bridge


def test_cerebrum_llm_puede_guardar_y_recordar():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_cerebrum_memory_bridge_3.json"
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=LLMManager(
            LLMConfig(proveedor="mock")
        ),
        memory_bridge=bridge
    )

    cerebrum.guardar_memoria_manual(
        "CEREBRUM usa memoria persistente"
    )

    recuerdo = cerebrum.recordar(
        "CEREBRUM"
    )

    assert recuerdo is not None

    assert (
        recuerdo["contenido"]
        == "CEREBRUM usa memoria persistente"
    )


def test_cerebrum_llm_obtiene_contexto_de_memoria():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_cerebrum_memory_bridge_4.json"
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    bridge.guardar_manual(
        "CEREBRUM es un proyecto de inteligencia artificial"
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=LLMManager(
            LLMConfig(proveedor="mock")
        ),
        memory_bridge=bridge
    )

    contexto = cerebrum.obtener_contexto_de_memoria(
        "CEREBRUM"
    )

    assert (
        "CEREBRUM es un proyecto de inteligencia artificial"
        in contexto
    )


def test_cerebrum_llm_obtiene_memorias_relevantes():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_cerebrum_memory_bridge_5.json"
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    bridge.guardar_manual(
        "Estoy desarrollando CEREBRUM"
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=LLMManager(
            LLMConfig(proveedor="mock")
        ),
        memory_bridge=bridge
    )

    recuerdos = cerebrum.obtener_memorias_relevantes(
        "CEREBRUM"
    )

    assert len(
        recuerdos
    ) > 0

def test_memory_policy_guarda_proyecto():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_policy import MemoryPolicy

    memoria = Memory(
        file_path="data/test_memory_policy_1.json"
    )

    service = MemoryService(
        memory=memoria
    )

    policy = MemoryPolicy()

    resultado = policy.evaluar(
        service,
        "mi proyecto es CEREBRUM"
    )

    assert resultado["guardar"] is True
    assert resultado["tipo"] == "proyecto"
    assert resultado["importancia"] == 5
    assert resultado["contenido"] == "CEREBRUM"


def test_memory_policy_no_guarda_texto_general():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_policy import MemoryPolicy

    memoria = Memory(
        file_path="data/test_memory_policy_2.json"
    )

    service = MemoryService(
        memory=memoria
    )

    policy = MemoryPolicy()

    resultado = policy.evaluar(
        service,
        "hoy hace calor"
    )

    assert resultado["guardar"] is False
    assert resultado["tipo"] == "general"


def test_memory_policy_guardar_si_corresponde():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_policy import MemoryPolicy

    memoria = Memory(
        file_path="data/test_memory_policy_3.json"
    )

    service = MemoryService(
        memory=memoria
    )

    policy = MemoryPolicy()

    recuerdo = policy.guardar_si_corresponde(
        service,
        "estoy trabajando en CEREBRUM"
    )

    assert recuerdo is not None
    assert recuerdo["tipo"] == "proyecto"

    recuerdos = memoria.obtener_todo()

    assert len(recuerdos) == 1

def test_memory_bridge_evalua_memoria():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_policy import MemoryPolicy

    memoria = Memory(
        file_path="data/test_memory_bridge_policy.json"
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service,
        memory_policy=MemoryPolicy()
    )

    resultado = bridge.evaluar(
        "mi proyecto es CEREBRUM"
    )

    assert resultado["guardar"] is True
    assert resultado["tipo"] == "proyecto"
    assert resultado["importancia"] == 5


def test_memory_bridge_guardar_usa_policy():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_policy import MemoryPolicy

    memoria = Memory(
        file_path="data/test_memory_bridge_policy_2.json"
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service,
        memory_policy=MemoryPolicy()
    )

    recuerdo = bridge.guardar(
        "mi proyecto es CEREBRUM"
    )

    assert recuerdo is not None

    recuerdos = memoria.obtener_todo()

    assert len(recuerdos) == 1


def test_memory_bridge_no_guarda_general():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_policy import MemoryPolicy

    memoria = Memory(
        file_path="data/test_memory_bridge_policy_3.json"
    )

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service,
        memory_policy=MemoryPolicy()
    )

    recuerdo = bridge.guardar(
        "hoy hace calor"
    )

    assert recuerdo is None

    assert memoria.obtener_todo() == []

def test_cerebrum_llm_guarda_memoria_importante_automaticamente():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_cerebrum_auto_memory.json"
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    cognitive = CognitiveEngine()

    manager = LLMManager(
        LLMConfig(
            proveedor="mock"
        )
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager,
        memory_bridge=bridge
    )

    cerebrum.responder(
        "mi proyecto es CEREBRUM"
    )

    recuerdos = memoria.obtener_todo()

    assert len(
        recuerdos
    ) == 1

    assert recuerdos[0]["tipo"] == "proyecto"
    assert recuerdos[0]["contenido"] == "CEREBRUM"


def test_cerebrum_llm_no_guarda_memoria_general():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_cerebrum_auto_memory_2.json"
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=LLMManager(
            LLMConfig(
                proveedor="mock"
            )
        ),
        memory_bridge=bridge
    )

    cerebrum.responder(
        "hoy está lloviendo"
    )

    assert (
        memoria.obtener_todo()
        == []
    )


def test_cerebrum_llm_memoria_no_rompe_respuesta():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_cerebrum_memoria_fallida.json"
    )

    def guardar_fallido(_memoria):
        raise RuntimeError(
            "fallo de almacenamiento"
        )

    memoria._guardar_archivo = guardar_fallido

    service = MemoryService(
        memory=memoria
    )

    bridge = MemoryBridge(
        memory_service=service
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=CognitiveEngine(),
        llm_manager=LLMManager(
            LLMConfig(
                proveedor="mock"
            )
        ),
        memory_bridge=bridge
    )

    respuesta = cerebrum.responder(
        "mi proyecto es CEREBRUM"
    )

    assert isinstance(
        respuesta,
        str
    )

    assert (
        "Respuesta simulada del LLM."
        in respuesta
    )

def test_memory_ranker_prioriza_relevancia():
    from src.brain.memory_ranker import MemoryRanker

    ranker = MemoryRanker()

    recuerdos = [
        {
            "contenido": "Me gusta la música",
            "importancia": 3
        },
        {
            "contenido": "Mi proyecto es CEREBRUM",
            "importancia": 5
        }
    ]

    resultado = ranker.ordenar(
        recuerdos,
        "CEREBRUM"
    )

    assert (
        resultado[0]["contenido"]
        == "Mi proyecto es CEREBRUM"
    )


def test_memory_ranker_puntua_importancia():
    from src.brain.memory_ranker import MemoryRanker

    ranker = MemoryRanker()

    recuerdo = {
        "contenido": "CEREBRUM",
        "importancia": 5
    }

    puntuacion = ranker.puntuar(
        recuerdo,
        "CEREBRUM"
    )

    assert puntuacion > 0.5


def test_memory_ranker_ignora_recuerdo_invalido():
    from src.brain.memory_ranker import MemoryRanker

    ranker = MemoryRanker()

    resultado = ranker.ordenar(
        [
            "esto no es un recuerdo"
        ],
        "CEREBRUM"
    )

    assert resultado == []


def test_memory_ranker_recencia_es_valida():
    from datetime import datetime

    from src.brain.memory_ranker import MemoryRanker

    ranker = MemoryRanker()

    recuerdo = {
        "contenido": "CEREBRUM",
        "importancia": 5,
        "fecha": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    puntuacion = ranker.puntuar(
        recuerdo,
        "CEREBRUM"
    )

    assert puntuacion > 0.0

def test_memory_bridge_usa_memory_ranker():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge
    from src.brain.memory_ranker import MemoryRanker

    memoria = Memory(
        file_path="data/test_memory_bridge_ranker.json"
    )

    memoria.guardar(
        "CEREBRUM es mi proyecto",
        tipo="proyecto",
        importancia=5
    )

    memoria.guardar(
        "Me gusta programar",
        tipo="preferencia",
        importancia=3
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        ),
        memory_ranker=MemoryRanker()
    )

    recuerdos = bridge.recuperar_relevante(
        "CEREBRUM"
    )

    assert len(recuerdos) > 0
    assert (
        recuerdos[0]["contenido"]
        == "CEREBRUM es mi proyecto"
    )


def test_memory_bridge_contexto_respeta_ranking():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_memory_bridge_ranker_2.json"
    )

    memoria.guardar(
        "CEREBRUM es mi proyecto",
        tipo="proyecto",
        importancia=5
    )

    memoria.guardar(
        "CEREBRUM tiene memoria",
        tipo="proyecto",
        importancia=4
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    contexto = bridge.obtener_contexto(
        "CEREBRUM",
        limite=1
    )

    assert len(contexto) == 1
    assert (
        contexto[0]["contenido"]
        == "CEREBRUM es mi proyecto"
    )

def test_cerebrum_llm_integra_memoria_persistente_en_contexto():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    memoria = Memory(
        file_path="data/test_v008_integracion_memoria.json"
    )

    memoria.guardar(
        "CEREBRUM es mi proyecto principal",
        tipo="proyecto",
        importancia=5
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    cognitive = CognitiveEngine()

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=LLMManager(
            LLMConfig(
                proveedor="mock"
            )
        ),
        memory_bridge=bridge
    )

    respuesta = cerebrum.responder(
        "¿Qué es mi proyecto CEREBRUM?"
    )

    assert (
        "CEREBRUM es mi proyecto principal"
        in respuesta
    )

def test_memory_bridge_persiste_entre_instancias():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    ruta = "data/test_v008_persistencia.json"

    memoria_1 = Memory(
        file_path=ruta
    )

    bridge_1 = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria_1
        )
    )

    bridge_1.guardar_manual(
        "CEREBRUM tiene memoria persistente"
    )

    memoria_2 = Memory(
        file_path=ruta
    )

    bridge_2 = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria_2
        )
    )

    recuerdo = bridge_2.recordar(
        "CEREBRUM"
    )

    assert recuerdo is not None

    assert (
        recuerdo["contenido"]
        == "CEREBRUM tiene memoria persistente"
    )

def test_cerebrum_v008_memoria_end_to_end():
    from src.brain.memory import Memory
    from src.brain.memory_service import MemoryService
    from src.brain.memory_bridge import MemoryBridge

    ruta = "data/test_v008_e2e.json"

    memoria = Memory(
        file_path=ruta
    )

    bridge = MemoryBridge(
        memory_service=MemoryService(
            memory=memoria
        )
    )

    cognitive = CognitiveEngine()

    manager = LLMManager(
        LLMConfig(
            proveedor="mock",
            modelo="cerebrum-v008"
        )
    )

    cerebrum = CerebrumLLM(
        cognitive_engine=cognitive,
        llm_manager=manager,
        memory_bridge=bridge
    )

    # 1. CEREBRUM aprende una memoria importante.
    cerebrum.responder(
        "mi proyecto es CEREBRUM"
    )

    # 2. Esa memoria debe existir.
    recuerdo = cerebrum.recordar(
        "CEREBRUM"
    )

    assert recuerdo is not None

    # 3. Nueva interacción.
    respuesta = cerebrum.responder(
        "¿Qué es mi proyecto CEREBRUM?"
    )

    assert isinstance(
        respuesta,
        str
    )

    # 4. El recuerdo debe poder recuperarse.
    contexto = cerebrum.obtener_contexto_de_memoria(
        "CEREBRUM"
    )

    assert any(
        "CEREBRUM" in texto
        for texto in contexto
    )

    # 5. Debe existir una sesión con ambos turnos.
    assert (
        manager
        .obtener_sesion()
        .cantidad_mensajes()
        == 4
    )