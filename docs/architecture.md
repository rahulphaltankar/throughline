# Throughline architecture

## Core abstraction

Throughline is a dependency-driven artefact planner.

The intended loop is:

```text
intake -> archetypes -> seed manifest -> dependency closure -> topological order
       -> frontier -> [skill execution] -> gates -> accepted artefacts -> blueprint
```

Everything up to and including `frontier` is implemented deterministically.
The provider-independent execution layer in `scripts/pipeline.py` consumes that
frontier, records work orders, invokes a selected adapter, and admits output
only after Tier-0 validation. Its sole adapter today copies controlled fixtures;
no code invokes a model. Gates exist at Tier 0 only.

### Artefact

A typed unit of solutioning output with explicit dependencies, declared in
`ontology/artefacts/core.yaml`. That file is the single source of truth for
dependency edges — archetype manifests and documentation must never restate
them.

There is no versioning, no content hashing and no staleness propagation.

### Execution layer

`scripts/run_pipeline.py` is a resumable runner outside the kernel boundary.
It persists state under `runs/<run-id>/`, resolves accepted upstream output,
calls a provider-neutral `ProducerAdapter`, then uses the real Tier-0 gate to
mark each artefact accepted or rejected. It blocks visibly when an unbound
dependency or an accepted-but-missing input prevents progress.

### Skill

Procedural know-how for producing one artefact type, written as Markdown
instructions for a model. Skills do not choose workflow order and do not call one
another. The registry binds an artefact type to a Skill via `produced_by`; the
binding is a *declaration*, not a dispatch mechanism.

### Gate

A predicate deciding whether an artefact is admissible.

Only **Tier 0** exists: `scripts/gates/validate_artifact.py` parses frontmatter
and checks it against the ontology. It validates structure — required fields,
known types, dependency coverage, evidence shape, human-review flags, declared
section headings. It does not assess whether the content is true, well-reasoned
or complete. Tiers 1–4 in `ontology/gates/README.md` are unimplemented.

### Archetype

A solution-class manifest that adds specialist artefacts to the general
baseline. Selection is deterministic keyword matching over the intake text, with
no stemming.

Because the kernel closes the manifest transitively over the registry, an
archetype manifest declares **intent** ("this class of problem needs a threat
model") and never has to enumerate that artefact's dependencies.

### Kernel

Deterministic code in `src/throughline/` responsible for routing, closure,
ordering, frontier calculation and reporting. Per CONSTITUTION.md principle 2 it
contains no LLM calls; `tests/test_engine.py` enforces this by AST inspection of
imports, which also bars network libraries and `subprocess`.

The kernel does not manage state, budgets, provenance or permissions. Those are
listed in the roadmap, not built.

## Current implementation boundary

v0.2 produces an **artefact plan**. It stops well before generation, let alone
build or deploy.

The first runner now exists, but its only producer is intentionally synthetic.
A real provider adapter must still render a Skill plus resolved input artefacts
into output without changing the kernel boundary.

A future adapter layer could delegate implementation to Claude Code, Codex,
OpenHands, infrastructure tools or human task queues. None of that exists.
