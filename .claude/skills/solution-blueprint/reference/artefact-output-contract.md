# Artefact Output Contract

This is the canonical Throughline artefact contract. It is defined
machine-readably in `ontology/artefact-contract.yaml` and explained in
`docs/artefact-contract.md`. This copy exists so the packaged Skill is
self-contained; `tests/test_contract.py` keeps all three in sync.

There is exactly one contract. Do not invent a variant.

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

Optional: `unsatisfied_inputs`, `notes`. Any other key is rejected by the gate.

## Shape

```yaml
---
id: ART-0001
type: <artefact type from ontology/artefacts/core.yaml>
schema_version: 1
produced_by: skill:<skill-directory>
inputs:
- id: <upstream artefact id>
  type: <upstream artefact type>      # or `intake` for the originating record
status: draft | proposed | accepted | stale | rejected
evidence:
- claim: "..."
  class: observed | cited | derived | assumed
  source: "..."
  confidence: low | medium | high
assumptions:
- id: A1
  statement: "..."
  validation: "how this gets tested"
open_questions:
- id: Q1
  question: "..."
  owner: "role accountable for answering"
review_required: true | false
---
```

## Rules

- One artefact has one clear purpose.
- Claims are separated from recommendations.
- Every evidence entry carries a class and a source. Sources are explicit.
- Every assumption carries a validation method. An assumption with no way to
  test it is not an assumption, it is an invention.
- A downstream artefact must list its upstream inputs.
- `review_required` must be `true` when the registry marks the type
  `human_required`.
- If a required upstream artefact was not produced, declare it in
  `unsatisfied_inputs` with a reason. Never drop it silently.
- Section headings required by the registry's `required_sections` must appear
  as whole heading lines.
