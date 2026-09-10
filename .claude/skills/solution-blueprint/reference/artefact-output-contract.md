# Artefact Output Contract

Each artefact should be returned with:

```yaml
id: ART-XXXX
type: <artefact-type>
status: draft | proposed | accepted | stale | rejected
produced_by: skill:solution-blueprint
inputs: []
evidence:
  - claim: "..."
    class: observed | cited | derived | assumed
    source: "..."
    confidence: 0.0
assumptions: []
open_questions: []
recommendation: "..."
review_required: true
```

Rules:

- One artefact has one clear purpose.
- Claims are separated from recommendations.
- Sources are explicit.
- Assumptions expire or are tied to a validation action.
- A downstream artefact must identify its upstream inputs.
