---
id: PP20-SM01
type: stakeholder-map
schema_version: 1
produced_by: skill:stakeholder-map
inputs:
- id: PP20-A01
  type: problem-frame
status: proposed
evidence:
- claim: The intake identifies CDIO / Enterprise Architect as buyer.
  class: observed
  source: projects/pp20/problem.yaml
  confidence: high
assumptions:
- id: SM-A1
  statement: Data owners from the connected lifecycle systems will be needed for a pilot.
  validation: Confirm named domain owners and decision rights during discovery.
open_questions:
- id: SM-Q1
  question: Who is accountable for semantic-definition approval in the pilot domain?
  owner: CDIO / Enterprise Architect
review_required: false
---
# Stakeholder Map — PP20

## Stakeholder register

| Role | Relationship | Confidence |
|---|---|---|
| CDIO / Enterprise Architect | Intake buyer and accountable sponsor candidate | observed |
| Domain data owner | Required for pilot data-product accountability | assumed |
| PLM, ERP, ALM, MES and service representatives | Source-system knowledge contributors | assumed |

## Influence and interests

- The sponsor needs a bounded, evidence-led pilot decision.
- Domain owners need clear semantic-definition and data-quality accountability.

## Accountability

Named approval and data ownership remain unconfirmed; no individual is represented as committed.

## Validation questions

- Confirm pilot sponsor, domain owner, and source-system decision rights.
