# MODELS.md

This repository prefers runtime model discovery over permanent model pinning.

## Principle

- if a newer free Gemini Flash-family model appears, the automation should naturally prefer it through API discovery
- if a model disappears, automation should fall back safely
- repository content should avoid pretending a single model name will last forever

## Operational Meaning

- model choice is an implementation detail of the automation
- repository evolution should stay portable across compatible AI systems
