# Throughline architecture

## Core abstraction

Throughline is a dependency-driven artefact planner.

The intended loop is:

```text
intake -> archetypes -> seed manifest -> dependency closure -> topological order
       -> frontier -> [skill execution] -> gates -> accepted artefacts -> blueprint
```

Everything up to and including `frontier` is implemented deterministically.
`[skill execution]` **does not exist**: no code invokes a model, supplies it
upstream artefacts, or writes an output file. Gates exist at Tier 0 only.

### Artefact

A typed unit of solutioning output with explicit dependencies, declared in
`ontology/artefacts/core.yaml`. That file is the single source of truth for
dependency edges — archetype manifests and documentation must never restate
them.

There is no versioning, no content hashing and no staleness propagation.

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

The gap between the plan and the Skills is the next implementation step: a
runner that walks the frontier, invokes the bound Skill with resolved upstream
artefacts, writes the output, and gates it. That runner must live in `scripts/`,
outside the deterministic kernel boundary.

A future adapter layer could delegate implementation to Claude Code, Codex,
OpenHands, infrastructure tools or human task queues. None of that exists.
