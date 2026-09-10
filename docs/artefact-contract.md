# Canonical artefact output contract

Every Throughline artefact is a Markdown file with a YAML frontmatter block.
There is exactly one contract. It is defined machine-readably in
[`ontology/artefact-contract.yaml`](../ontology/artefact-contract.yaml), which
is the single source of truth; this page restates it for humans and
`tests/test_contract.py` keeps the two in sync.

The gate `scripts/gates/validate_artifact.py` enforces this contract. An
artefact that does not conform is rejected.

## Required frontmatter fields

- `id`
- `type`
- `schema_version`
- `produced_by`
- `inputs`
- `status`
- `evidence`
- `assumptions`
- `open_questions`
- `review_required`

Optional: `unsatisfied_inputs`, `notes`. Any other key is rejected.

## Example

```yaml
---
id: PP20-A01
type: problem-frame
schema_version: 1
produced_by: skill:problem-frame
inputs:
- id: PP20
  type: intake
status: proposed
evidence:
- claim: The supplied row identifies the lack of a common semantic layer.
  class: observed
  source: projects/pp20/problem.yaml
  confidence: high
assumptions:
- id: A1
  statement: PLM, ERP, ALM, MES and service are the relevant systems.
  validation: Confirm the actual system landscape with the accountable owner.
open_questions:
- id: Q1
  question: Are identifier mismatches a material cause of delay?
  owner: CDIO / Enterprise Architect
review_required: false
---
```

## Field rules

| Field | Rule |
|---|---|
| `id` | Non-empty string, unique within a project. |
| `type` | Must exist in `ontology/artefacts/core.yaml`. Unknown types are rejected, never waved through. |
| `schema_version` | Must equal the `schema_version` in the contract file (currently `1`). |
| `produced_by` | `skill:<directory>`, and `.claude/skills/<directory>/SKILL.md` must exist. Must agree with the registry's `produced_by` for this type. |
| `inputs` | List of `{id, type}`. Each `type` must be a known artefact type, or the pseudo-type `intake` to reference the originating intake record. |
| `status` | One of `draft`, `proposed`, `accepted`, `stale`, `rejected`. |
| `evidence` | List of `{claim, class, source, confidence}`. `class` is one of `observed`, `cited`, `derived`, `assumed`. `confidence` is `low`, `medium` or `high`. Required to be non-empty when the registry marks the type `evidence_required`. |
| `assumptions` | List of `{id, statement, validation}`. An assumption without a validation method is rejected. |
| `open_questions` | List of `{id, question, owner}`. |
| `review_required` | Boolean. Must be `true` when the registry marks the type `human_required`. |
| `unsatisfied_inputs` | List of `{type, reason}`. See below. |

## Dependency coverage

The registry gives each artefact type a `requires` list. The gate checks that

```
set(inputs.type) ∪ set(unsatisfied_inputs.type)  ⊇  requires
```

A dependency can therefore be **deferred**, but never silently **dropped**. If
an upstream artefact was not produced, it must be declared explicitly:

```yaml
unsatisfied_inputs:
- type: kpi-model
  reason: The KPI model was not available at execution time, so this
    recommendation has no agreed baseline to be judged against.
```

Declaring a type that the artefact does not actually require is also rejected,
so the field cannot be used as a catch-all.

## What this contract does not do

It validates **structure**, not **quality**. A conformant artefact is
well-formed and honest about its gaps. It is not thereby correct, evidenced, or
approved. Tiers 1–4 of `ontology/gates/README.md` do not exist yet.
