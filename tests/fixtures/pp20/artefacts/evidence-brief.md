---
id: PP20-A02
type: evidence-brief
schema_version: 1
produced_by: skill:evidence-brief
inputs:
- id: PP20-A01
  type: problem-frame
status: proposed
evidence:
- claim: Cross-domain digital-thread value depends on interoperable data.
  class: cited
  source: Source key supplied with PP20; not independently retrieved. Requires an external primary source
    before this stays classed as cited.
  confidence: medium
- claim: Common semantics can reduce integration/reconciliation friction.
  class: derived
  source: Derived from the problem frame; validate through baseline measurement.
  confidence: medium
- claim: A canonical ontology should cover every enterprise domain.
  class: assumed
  source: Not evidenced. Explicitly tested by scoping the pilot first.
  confidence: low
- claim: No evidence yet shows semantic inconsistency is the dominant source of business loss versus process
    design, data quality or integration latency.
  class: observed
  source: Absence of supplied evidence; recorded as a material evidence gap.
  confidence: high
assumptions:
- id: A4
  statement: The supplied source key represents a retrievable, citable body of evidence.
  validation: Retrieve the underlying source and record URL and retrieval date, or downgrade the claim
    from cited to assumed.
open_questions:
- id: Q3
  question: What is the actual identifier-conflict frequency and its business impact?
  owner: Enterprise Architect
- id: Q4
  question: What API/event availability and licensing constraints exist today?
  owner: Integration Lead
- id: Q5
  question: Who owns data accountability by domain?
  owner: Data Governance Lead
- id: Q6
  question: What existing MDM/metadata/ontology assets are already in place?
  owner: Data Architect
review_required: false
---
# Evidence Brief — PP20

## Claim ledger
| Claim | Class | Confidence | Validation / source |
|---|---|---:|---|
| Cross-domain digital-thread value depends on interoperable data | cited | Medium | Source key supplied with PP20; validate independently |
| Common semantics can reduce integration/reconciliation friction | derived | Medium | Validate through baseline measurement |
| A canonical ontology should cover every enterprise domain | assumed | Low | Explicitly test pilot scope first |

## Supporting evidence
The supplied opportunity describes PLM, ERP, ALM, MES and service as the systems spanning the semantic gap.

## Disconfirming evidence
No direct evidence has yet been supplied showing that semantic inconsistency—not process design, data quality, or integration latency—is the dominant source of business loss. This is a material evidence gap.

## Evidence gaps
- Actual identifier-conflict frequency and business impact.
- Current API/event availability and licensing constraints.
- Data ownership/accountability by domain.
- Existing MDM/metadata/ontology assets.
