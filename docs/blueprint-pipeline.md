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
- the **dependency deficit** — registry-required upstream artefacts that no
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
   records what those artefacts require but cannot get.

## Current coverage

Seven artefact types have a Skill binding: `problem-frame`, `evidence-brief`,
`current-state-assessment`, `requirements`, `acceptance-criteria`,
`solution-options`, `solution-recommendation`.

For PP20 the kernel plans **49 artefacts**. Seven have a producer. **The
executable sequence is an MVP slice, not the solution.**

### Known dependency deficits

The executable sequence cannot satisfy some of its own registry-required inputs:

| Artefact | Missing upstream | Consequence |
|---|---|---|
| `requirements` | `business-objectives`, `stakeholder-map` | Objectives are inferred from the intake; requirement ownership is unattributed. |
| `solution-recommendation` | `kpi-model` | No agreed baseline or target measure to judge the recommendation against. |

These are not hidden. Each affected artefact must declare them in
`unsatisfied_inputs` with a reason, the gate rejects the artefact if it does not,
and the kernel reports them in `plan.json` under
`mvp_unsatisfied_dependencies`.

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
