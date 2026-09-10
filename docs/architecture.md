# Throughline architecture

## Core abstraction

Throughline is a dependency-driven solutioning compiler.

The core loop is:

`intake -> archetypes -> artefact manifest -> dependency graph -> skill execution -> gates -> accepted artefacts -> blueprint`

### Artefact

A typed, versioned unit of solutioning output with provenance and explicit dependencies.

### Skill

Procedural know-how for producing one independently verifiable unit of work. Skills do not choose workflow order and do not call one another.

### Gate

A predicate deciding whether an artefact is admissible. Deterministic and structural checks should be used before adversarial or rubric evaluation.

### Archetype

A solution-class manifest that adds specialist artefacts and evaluation requirements to the general solution baseline.

### Kernel

Deterministic code responsible for routing, dependency resolution, state, budgets, provenance, and permissions. LLMs must not own these decisions.

## Current implementation boundary

v0.1 stops before autonomous build/deploy execution. It produces a first-pass blueprint skeleton.

The intended future adapter layer may delegate implementation to Claude Code, Codex, OpenHands, infrastructure tools, SaaS APIs, or human task queues.
