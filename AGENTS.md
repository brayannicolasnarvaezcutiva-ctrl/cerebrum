# CEREBRUM — Development Instructions

## Project

CEREBRUM is a modular AI project developed in Python.

Current version:
v0.0.4 Alpha — Reasoning Core

## Current architecture

src/
├── brain/
│   ├── context.py
│   ├── engine.py
│   ├── inference.py
│   ├── intents.py
│   ├── logic.py
│   ├── memory.py
│   ├── processor.py
│   └── reasoning.py
├── commands/
├── core/
└── main.py

## Current capabilities

CEREBRUM currently has:

- command system
- intent detection
- persistent memory
- memory categories
- memory importance
- memory search
- memory updates
- memory deletion
- duplicate prevention
- conversation context
- associative memory
- reasoning engine
- inference engine
- logical premise validation
- contradiction detection
- basic modus ponens inference

## Current goal

Improve the architecture of the reasoning system without changing
the already working behavior.

## Important rules

1. Do not delete existing functionality.
2. Do not rewrite the project from scratch.
3. Do not remove Memory, Context, Reasoning, Inference, or Logic.
4. Preserve the current command system.
5. Preserve compatibility with Windows and Linux.
6. Add tests before or alongside major refactors.
7. Keep modules separated by responsibility.
8. Avoid putting all logic into processor.py.
9. Do not introduce unnecessary external dependencies.
10. Explain major architectural changes.

## Refactoring goal

Reduce the responsibility of BrainProcessor.

BrainProcessor should coordinate systems rather than contain
all business logic.

Target architecture:

User
↓
BrainProcessor
├── Context
├── Memory
├── Reasoning
└── Inference
↓
Response

## Testing

Every refactor must preserve the behavior of:

- Memory
- Context
- Reasoning
- Inference
- Logic
- command processing

Run the existing test suite after modifications.

## Git

Do not create commits automatically.

Do not create tags automatically.

Do not push to GitHub automatically.

The human developer will review changes before committing.