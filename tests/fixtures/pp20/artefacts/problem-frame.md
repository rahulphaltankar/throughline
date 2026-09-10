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
- claim: The supplied opportunity row identifies the lack of a common semantic layer as the pain point.
  class: observed
  source: projects/pp20/problem.yaml
  confidence: high
- claim: The supplied row links the opportunity to digital-thread interoperability.
  class: cited
  source: 'projects/pp20/problem.yaml (source_key: Tata Automotive Intelligence). Not independently retrieved.'
  confidence: medium
- claim: A canonical semantic model could reduce translation effort between domains if underlying data
    quality and ownership are sufficient.
  class: derived
  source: Derived from the stated pain point; not independently verified.
  confidence: low
- claim: PLM, ERP, ALM, MES and service systems are materially in scope for the pilot.
  class: assumed
  source: Not supplied; requires validation of the actual system landscape.
  confidence: low
assumptions:
- id: A1
  statement: PLM, ERP, ALM, MES and service are the relevant systems for the pilot scope.
  validation: Confirm actual system landscape, versions, owners and integration access with the accountable
    owner.
- id: A2
  statement: Semantic/identifier inconsistency is a material cause of current delay.
  validation: Measure identifier-conflict frequency and its business impact against a baseline.
- id: A3
  statement: Target systems expose enough metadata and APIs/events to support a semantic layer.
  validation: Inventory available APIs, events and metadata per system, including licensing constraints.
open_questions:
- id: Q1
  question: Are identifier mismatches actually a material cause of current engineering/manufacturing delay?
  owner: CDIO / Enterprise Architect (intake buyer)
- id: Q2
  question: Do the target systems expose enough metadata and APIs/events to support a useful semantic
    layer?
  owner: CDIO / Enterprise Architect (intake buyer)
review_required: false
---
# Problem Frame — PP20

## Source statement
No common semantic layer across PLM, ERP, ALM, MES and service. Proposed opportunity: Automotive Data Mesh / Knowledge Layer.

## Problem
Engineering, manufacturing, and service information is likely to use inconsistent identifiers, structures, and semantics across major lifecycle systems. This creates friction for digital-thread traceability and cross-domain use cases.

## Evidence
- `observed`: the supplied opportunity row identifies the lack of a common semantic layer as the pain point.
- `cited`: the supplied row links the opportunity to digital-thread interoperability.
- `derived`: a canonical semantic model could reduce translation effort between domains if the underlying data quality and ownership are sufficient.
- `assumed`: PLM, ERP, ALM, MES and service systems are materially in scope for the pilot; validate actual system landscape and integration access.

## Hypotheses
1. A domain-level semantic layer can reduce manual reconciliation and make cross-system traceability more reusable.
2. Starting with one high-value domain data product is lower-risk than attempting enterprise-wide semantic standardisation at once.

## Falsification questions
- Are identifier mismatches actually a material cause of current engineering/manufacturing delay?
- Do the target systems expose enough metadata and APIs/events to support a useful semantic layer?
