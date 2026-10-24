# CEREBRUM — Development Instructions

## Project

CEREBRUM is a modular AI project developed in Python.

Current version:
v0.0.9 Alpha — preparation toward v0.1.0

## Current architecture

`src/` is the package root. Internal modules use the `brain`, `commands`, and
`core` package namespaces; imports inside `brain` are relative.

```text
main -> core.App -> commands.CommandManager -> BrainEngine -> BrainProcessor
                                                     ├─ Context
                                                     ├─ MemoryService -> Memory
                                                     └─ ReasoningRequestHandler

ChatController -> CerebrumLLM -> CognitiveEngine -> KnowledgeReasoning
                                            ├─ MemoryBridge
                                            └─ LLMManager
```

## Important rules

1. Do not delete existing functionality or rewrite the project from scratch.
2. Preserve the command system and its user-facing responses.
3. Preserve the public API and JSON format of `Memory`.
4. Preserve compatibility with Windows and Linux.
5. Add or update tests alongside architecture changes.
6. Keep modules separated by responsibility; `BrainProcessor` coordinates.
7. Keep the mock LLM usable without the optional OpenAI dependency.
8. Do not introduce unnecessary external dependencies.
9. Never store real memory, credentials, test artifacts, caches, or virtual
   environments in Git.
10. Explain major architectural changes.

## Reasoning boundaries

- `ReasoningEngine` preserves the text-based command flow.
- `ReasoningResult` is the canonical result contract and retains textual
  compatibility fields while carrying structured conclusions.
- `KnowledgeInference` owns inference rule discovery.
- `ExplainedKnowledgeInference` adds explanation and evidence.
- `KnowledgeReasoning` coordinates validation, confidence and conflicts for
  the Cognitive Core.

## Testing

Run the complete suite with `pytest`. Tests that persist memory must use
temporary paths and must not change `data/memory.json`.

## Git

Do not create commits, tags, or pushes unless the human developer explicitly
requests them.
