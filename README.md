# Throughline

**A governed intent-to-solution blueprint compiler.**

Throughline takes a messy problem statement, pain point, opportunity, or hypothesis and compiles it into a traceable solution blueprint: problem framing, requirements, options, architecture, data, AI, security/privacy/regulatory considerations, commercial case, delivery plan, project-management artefacts, deployment, operations, change, and evidence.

This repository is the **blueprint-first** implementation. It does not deploy or operate customer systems. It deliberately separates:

- **Intent** — what the requester says they need.
- **Artefacts** — typed outputs produced by solutioning work.
- **Dependencies** — what must exist before an artefact can be produced.
- **Gates** — what must be true before an artefact is accepted.
- **Skills** — procedural know-how used by an AI worker to produce one artefact.
- **Agents** — bounded execution roles.
- **Kernel** — deterministic orchestration and state logic.
- **Human decisions** — decisions that cannot safely be delegated.

The 15 lifecycle phases from the design work remain a **reporting view**, not the machine control structure.

## Design principles

1. **The graph routes work; the model does not invent workflow order.**
2. **Artefacts are typed and provenance-aware.**
3. **Every important claim is `observed`, `cited`, `derived`, or `assumed`.**
4. **Acceptance criteria are frozen before downstream solutioning.**
5. **Deterministic gates outrank LLM judgement.**
6. **The author never grades its own work.**
7. **Human approvals are explicit, typed, hash-bound, and non-waivable where required.**
8. **No execution capability is implied by a blueprint.**
9. **Unknowns become research questions or expiring assumptions—not invented facts.**
10. **Project-management outputs are first-class solution artefacts.**

## Claude Skill

The repo contains a project Skill at:

```text
.claude/skills/solution-blueprint/SKILL.md
```

Claude Code can discover project Skills from that exact structure. The Skill instructs Claude to use Throughline as the planning/blueprinting method and to generate a complete first-pass solution blueprint without executing production changes.

## Quick start

```bash
python -m throughline.cli plan projects/pp20/problem.yaml --out projects/pp20/blueprint
```

The command produces:

```text
blueprint/plan.json
blueprint/plan.md
```

## What the MVP does

The deterministic kernel currently:

- loads an intake record;
- classifies likely solution archetypes using explicit rules;
- composes required artefacts from those archetypes;
- resolves the dependency graph;
- calculates a deterministic execution frontier;
- emits a first-pass blueprint structure;
- identifies human decision points;
- records evidence requirements and open questions;
- generates PMO artefacts such as WBS, estimation inputs, resource-plan inputs, schedule inputs and budget inputs.

It intentionally does **not** pretend that it can objectively validate soft questions such as market desirability, organisational willingness, or legal attestation.

## Architecture

```text
Problem / Opportunity
        |
        v
   Intake Contract
        |
        v
 Archetype Classifier  <--- explicit rules, model may assist later
        |
        v
 Artefact Manifest
        |
        v
 Dependency Graph
        |
        +-------------------+
        |                   |
        v                   v
   Skills / Workers       Gates
        |                   |
        +---------+---------+
                  v
          Accepted Artefacts
                  |
                  v
            Solution Blueprint
```

The eventual autonomous layer can sit above this deterministic kernel. Coding/deployment executors such as Claude Code, Codex, or OpenHands should remain adapters, not be reinvented inside Throughline.

## Status

`v0.1 blueprint compiler`

This repository is a design-and-prototype foundation, not production enterprise software.


## First artefact-producing pipeline

Throughline now includes a first real solutioning chain:

`problem-frame → evidence-brief → current-state-assessment → requirements → solution-options → solution-recommendation`

A benchmark instance is included under `examples/pp20/`. The chain is generic; PP20 is test data, not a hard-coded workflow.

Claude Skills are stored under `.claude/skills/`. The repository remains blueprint-only: it does not execute production changes.
