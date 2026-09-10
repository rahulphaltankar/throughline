# Throughline

**A deterministic artefact planner for solutioning work.**

Throughline takes a problem statement, pain point, opportunity or hypothesis and
works out **which solutioning artefacts are required, in what dependency order,
which of them can currently be produced, and which human decisions are
unavoidable**.

It plans the work. It does not do the work.

> **Read this before evaluating the repo.** Throughline does not generate
> solution content, does not call an LLM, does not estimate cost or effort, and
> has no real provider adapter. Twelve artefact types have a Claude Skill that
> tells a model how to write them; the other 46 have no producer at all. See
> [What exists today](#what-exists-today).

## What exists today

| Layer | State |
|---|---|
| Artefact registry — 58 typed artefacts with dependency edges | **Implemented** |
| Archetype routing — 11 keyword-matched solution classes | **Implemented** |
| Transitive dependency closure | **Implemented** |
| Topological ordering + dependency-ready frontier | **Implemented** |
| Skill bindings (`produced_by`) for 12 of 58 artefact types | **Implemented** |
| Canonical artefact output contract | **Implemented** |
| Tier-0 deterministic gate (structure only) | **Implemented** |
| Claude Skills — procedural instructions for 11 single-purpose artefact types, plus `requirements` | **Implemented (prose)** |
| Provider-independent execution runner | **Implemented (local fixture adapter only)** |
| Real LLM artefact generation | **Not implemented** |
| Gate tiers 1–4 (structural predicates, adversarial, rubric, human) | **Not implemented** |
| PMO calculation (WBS, estimation, schedule, budget) | **Not implemented** |
| Ledger, versioning, staleness propagation, approval objects | **Not implemented** |
| Any execution or deployment capability | **Not implemented, and out of scope** |

The kernel emits an **artefact plan**: which artefacts, in what order, produced
by what, and what is still unproducible. It does not emit problem framing,
requirements, architecture, estimates or budgets. Nothing in this repository
writes an artefact.

### What "Skill binding" does and does not mean

Twelve artefact types resolve to a `SKILL.md` — a set of written instructions
for a model. The execution runner resolves the binding and passes a complete
work order to an adapter; its only adapter copies controlled fixtures. Nothing
in the repository invokes a model.

The artefacts under `tests/fixtures/pp20/` are **hand-written test data** used to
exercise the gate. They are not system output and must never be presented as
such.

## Architecture

```text
Problem / Opportunity
        |
        v
   Intake Contract              (schemas/intake.schema.json - not yet enforced)
        |
        v
 Archetype Classifier           deterministic keyword rules
        |
        v
 Seed Artefact Manifest         ontology/archetypes/*.yaml
        |
        v
 Transitive Closure             ontology/artefacts/core.yaml owns every edge
        |
        v
 Topological Order + Frontier   deterministic, no LLM
        |
        v
     Artefact Plan              plan.json / plan.md
        |
        v
 Provider-independent runner     (`scripts/run_pipeline.py`)
        v
 [ Local test adapter / future provider adapter ]
        |
        v
   Tier-0 Gate                  structure only
```

## Design principles

1. The graph routes work; the model does not invent workflow order.
2. Artefacts are typed and provenance-aware.
3. Every important claim is `observed`, `cited`, `derived`, or `assumed`.
4. Acceptance criteria are frozen by a human before downstream solutioning.
5. Deterministic gates outrank LLM judgement.
6. The author never grades its own work. *(Aspiration: not yet enforced — see
   [Known limitations](#known-limitations).)*
7. Human approvals are explicit and typed. *(Partially: the plan names them;
   there is no approval object.)*
8. No execution capability is implied by a plan.
9. Unknowns become research questions or expiring assumptions — not invented facts.
10. Project-management outputs are first-class artefact **types** in the
    registry. Nothing calculates them.

The 15 lifecycle phases in `ontology/views/phases-15.yaml` are a **reporting
projection**, not the control structure. Nothing currently reads that file.

## Quick start

```bash
PYTHONPATH=src python -m throughline.cli plan projects/pp20/problem.yaml --out projects/pp20/blueprint
```

Produces `plan.json` and `plan.md`. For PP20 that is a plan of **49 artefacts**,
of which 12 have a producer and 37 do not.

Run the checks:

```bash
make check
```

That runs the test suite, exhaustive archetype graph validation, and the
artefact gate over the benchmark fixtures.

## Repository map

```text
ontology/artefacts/core.yaml      58 artefact types; the dependency graph
ontology/archetypes/              11 solution classes
ontology/artefact-contract.yaml   the one canonical output contract
src/throughline/                  the deterministic kernel (no LLM, no network)
scripts/gates/                    Tier-0 artefact gate
scripts/validate_ontology.py      exhaustive archetype resolution check
.claude/skills/                   12 Skills: 11 chain + 1 umbrella
tests/fixtures/pp20/              hand-written benchmark artefacts (TEST DATA)
tests/fixtures/broken/            deliberate false-positive probes
projects/pp20/problem.yaml        the PP20 intake record
docs/artefact-contract.md         the contract, explained
```

## Known limitations

- **No real generation.** The runner currently has only a local fixture adapter
  that copies controlled test data. No LLM or external provider adapter exists.
- **12 of 58 artefact types have a producer.** For PP20 that is 12 of 49 planned
  artefacts. The bound slice is still not a complete solution blueprint.
- **The remaining frontier is unbound.** After the PP20 bound slice, the local
  runner blocks on `business-case`, `risk-register`, `target-architecture`, and
  `traceability`; it does not manufacture them.
- **The gate validates structure, not truth.** A conformant artefact is
  well-formed and honest about its gaps. It is not correct, evidenced or
  approved. Tiers 1–4 do not exist.
- **Principle 6 is unenforced.** Nothing structurally prevents the same
  invocation from authoring and grading an artefact.
- **Classification is keyword matching** with no stemming; `supplier` will not
  match `suppliers`.
- **`schemas/intake.schema.json` is not enforced.** No validation runs against it.
- **`ontology/capabilities.yaml`, `ontology/views/phases-15.yaml`,
  `ontology/policies/` are inert.** Nothing reads them.
- **`migration-cutover` and `retirement-plan`** exist in the registry but are
  named by no archetype.

## Status

`v0.2 artefact planner`

A design-and-prototype foundation, not production software. It is deliberately
smaller than it looks: the value is in the typed artefact graph and the
deterministic kernel, not in any generated output.
