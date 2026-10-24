# CEREBRUM

v0.0.9 Alpha — preparación arquitectónica hacia v0.1.0.

CEREBRUM combina memoria persistente, razonamiento clásico basado en texto,
conocimiento estructurado e integración opcional con proveedores LLM.

## Instalación para desarrollo

Requiere Python 3.11 o posterior.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

El proveedor OpenAI es opcional. Instálalo solo cuando vaya a utilizarse:

```powershell
pip install -e ".[openai]"
```

También se proporcionan `requirements-dev.txt` y `requirements-openai.txt`
para flujos que no usan instalación editable.

## Ejecución

Tras instalar el paquete, inicia la interfaz de línea de comandos con:

```powershell
cerebrum
```

Durante desarrollo, sin instalar el paquete:

```powershell
$env:PYTHONPATH = "src"
python -m main
```

## Pruebas

```powershell
pytest
```

Las pruebas usan memoria temporal y no deben modificar `data/memory.json`.
El proveedor `mock` funciona sin credenciales ni el SDK de OpenAI.

## Arquitectura

- `brain`: memoria, razonamiento clásico, núcleo cognitivo y LLM Core.
- `commands` y `core`: interfaz de línea de comandos y arranque.
- `tests`: pruebas unitarias e integración.

El razonamiento clásico conserva las respuestas de los comandos existentes.
El núcleo cognitivo produce resultados estructurados con inferencias,
validación, confianza y conflictos.
