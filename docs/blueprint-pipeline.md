# The artefact pipeline

**This document does not define the pipeline order.** It cannot: the order is
derived from `ontology/artefacts/core.yaml` at runtime. There is exactly one
source of truth for dependencies, and it is the registry.

To see the sequence for any intake:

```bash
PYTHONPATH=src python -m throughline.cli plan projects/pp20/problem.yaml --out /tmp/plan
```

The output reports:

- the full artefact plan in dependency order;
- the **frontier** — artefacts whose upstream inputs are all satisfied;
- the **currently executable sequence** — the subset with a Skill binding;
- any **dependency deficit** — registry-required upstream artefacts that no
  Skill can currently produce.

## How the sequence is derived

1. `classify()` selects archetypes from the intake.
2. `seed_artifacts()` collects what those archetypes name.
3. `close_dependencies()` expands the seed set over the registry's `requires`
   edges until it is closed. An archetype manifest never has to restate a
   dependency the registry already owns.
4. `topological_order()` sorts the closed set.
5. `compute_frontier()` returns what is genuinely ready now.
6. `derive_mvp_sequence()` filters to artefacts with a `produced_by` binding and
   records any required upstream artefacts that cannot be produced.

## Current coverage

Twelve artefact types have a Skill binding: `problem-frame`, `assumption-register`,
`business-objectives`, `evidence-brief`, `open-questions`, `stakeholder-map`,
`kpi-model`, `current-state-assessment`, `requirements`, `acceptance-criteria`,
`solution-options`, and `solution-recommendation`.

For PP20 the kernel plans **49 artefacts**. Twelve have a producer. **The
executable sequence is an MVP slice, not the solution.**

### Current execution boundary

The expanded bound slice has no unsatisfied upstream dependency. The local
runner accepts all 12 PP20 fixture-backed artefacts, then blocks at the next
unbound frontier: `business-case`, `risk-register`, `target-architecture`, and
`traceability`. A missing input must still be declared in `unsatisfied_inputs`
when it occurs; the gate rejects silently dropped dependencies.

## Human freeze points

- Problem significance and truth: human accountable owner.
- Acceptance criteria: human freeze before material downstream commitment.
- Material solution recommendation: human decision.
- Regulatory / legal attestation: human only.

The kernel identifies these from `human_required` in the registry. It does not
model, record or enforce the approval itself. There is no approval object.

## Benchmark

`tests/fixtures/pp20/` holds hand-written reference artefacts used to exercise
the gate. **They are test data.** Nothing generates them, and they must never be
consumed as pipeline input or presented as system output.
