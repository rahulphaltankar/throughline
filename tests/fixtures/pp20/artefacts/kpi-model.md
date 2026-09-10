---
id: PP20-KPI01
type: kpi-model
schema_version: 1
produced_by: skill:kpi-model
inputs:
- id: PP20-BO01
  type: business-objectives
status: proposed
evidence:
- claim: The intake does not provide a measured baseline for reconciliation effort or digital-thread outcomes.
  class: observed
  source: projects/pp20/problem.yaml
  confidence: high
assumptions:
- id: KPI-A1
  statement: Reconciliation effort can be measured consistently for a selected pilot flow.
  validation: Agree the unit, data source, collection period, and baseline method with the pilot owner.
open_questions:
- id: KPI-Q1
  question: What target improvement is acceptable for the pilot decision?
  owner: CDIO / Enterprise Architect
review_required: false
---
# KPI Model — PP20

## Outcome-to-metric mapping

| Outcome | Metric | Unit |
|---|---|---|
| Reduce reconciliation friction | Manual reconciliation effort in selected pilot flow | effort per case |
| Improve governed interoperability | Mapped entities with accountable semantic ownership | percentage |

## Baselines

No baseline is supplied. Establish one before setting acceptance thresholds.

## Targets

Targets remain open until the sponsor agrees the pilot baseline and value threshold.

## Measurement method

Measure a defined pilot flow over an agreed period using a documented source, calculation, and exclusion rule.

## Owners and cadence

The pilot sponsor owns target approval; the domain data owner should review measurements at an agreed cadence.
