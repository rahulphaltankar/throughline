---
id: PP20-A01
type: problem-frame
status: proposed
evidence_classes: observed, cited, derived, assumed
inputs: [PP20]
assumptions: [A1, A2, A3]
open_questions: [Q1, Q2, Q3]
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
