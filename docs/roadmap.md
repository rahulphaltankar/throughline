# Throughline build roadmap

## 0. Artefact planner — DONE (v0.2)

- canonical artefact catalogue (58 typed artefacts)
- archetype routing (11 classes)
- transitive dependency closure; all archetypes resolve
- topological order and dependency-ready frontier
- Skill bindings in the registry
- one canonical artefact output contract
- Tier-0 structural gate with false-positive fixtures
- PP20 benchmark and CI

## 1. Generation — in progress

`scripts/run_pipeline.py` now provides the bounded, resumable execution path:
frontier → work order → provider adapter → Tier-0 gate → persisted status. Its
only adapter copies controlled fixtures; it does not generate content.

Still required:

- a real provider adapter that renders a bound Skill using resolved upstream
  artefacts, while preserving the runner's explicit request/result contract
- generated-vs-fixture diffing as the first real eval
- producers for the artefacts the chain already depends on and cannot get:
  `business-objectives`, `stakeholder-map`, `kpi-model`

## 2. Evidence and gate tiers

- Tier 1: structural predicates over artefact content
- Tier 2: adversarial review
- Tier 3: calibrated rubric judgement, with human-labelled calibration data
- Tier 4: human validation
- citation and link verification
- enforcement of principle 6 (the author must not grade its own work)
- intake schema enforcement (`schemas/intake.schema.json` is currently unread)

## 3. Stateful execution

- append-only ledger
- artefact versioning and acceptance hashes
- content-hash staleness propagation
- human approval objects and an approval inbox

## 4. Calculation layers

- PMO calculation: WBS decomposition, estimation model, schedule, budget.
  These are artefact *types* today; nothing computes them.
- architecture diagram generation
- technology-option research adapters

## 5. Optional build adapters

Claude Code, Codex, OpenHands, Terraform/Pulumi, GitHub/MCP.

## 6. RUN mode

Observability, SLOs, incident diagnosis, gated remediation, benefits-realisation
feedback.

---

Stages 4–6 are speculative. Stage 1 is the only one with a concrete next action.
