---
id: PP20-A03
type: current-state-assessment
schema_version: 1
produced_by: skill:current-state-assessment
inputs:
- id: PP20-A01
  type: problem-frame
- id: PP20-A02
  type: evidence-brief
status: proposed
evidence:
- claim: Cross-domain questions require reconciliation across multiple lifecycle systems.
  class: derived
  source: Derived from the problem frame; exact workflows unconfirmed.
  confidence: low
- claim: PLM, ERP, ALM, MES and service form the relevant integration landscape.
  class: assumed
  source: Assumed for blueprinting. Confirm actual products, versions, interfaces, regions, owners and
    data residency.
  confidence: low
- claim: Likely entities include part/product, requirement, software item, manufacturing operation, serial/vehicle,
    change, supplier, service event and evidence.
  class: derived
  source: Derived from the named system classes; canonical identifiers and relationships are unknown.
  confidence: low
assumptions:
- id: A5
  statement: The named systems are the authoritative sources for the pilot entities.
  validation: Confirm system-of-record ownership per entity with the domain owners.
open_questions:
- id: Q7
  question: Which identifiers are inconsistent across engineering and manufacturing?
  owner: Enterprise Architect
- id: Q8
  question: Which systems are authoritative for each key entity?
  owner: Data Governance Lead
- id: Q9
  question: Where do APIs/events exist today?
  owner: Integration Lead
- id: Q10
  question: What data is governed centrally versus by domain?
  owner: Data Governance Lead
- id: Q11
  question: Which single data product would produce measurable value fastest?
  owner: CDIO / Enterprise Architect (intake buyer)
review_required: false
---
# Current-State Assessment — PP20

## Current business process
Cross-domain questions likely require engineers, manufacturing teams, or analysts to reconcile information from multiple lifecycle systems. Exact workflows must be confirmed.

## Current systems landscape
```mermaid
flowchart LR
  PLM[PLM] --- ERP[ERP]
  ERP --- MES[MES]
  PLM --- ALM[ALM]
  ALM --- SVC[Service]
  MES --- SVC
  GAP[[Semantic / identifier gap]]
  PLM -. inconsistent meaning .-> GAP
  ERP -. inconsistent meaning .-> GAP
  ALM -. inconsistent meaning .-> GAP
  MES -. inconsistent meaning .-> GAP
  SVC -. inconsistent meaning .-> GAP
```

All named systems above are `assumed` as the relevant integration landscape for blueprinting; confirm actual products, versions, interfaces, regions, owners, and data residency.

## Current data landscape
Likely entities include part/product, requirement, software item, manufacturing operation, serial/vehicle, change, supplier, service event, and evidence. The precise canonical identifiers and relationships are unknown.

## Validation questions
1. Which identifiers are inconsistent across engineering and manufacturing?
2. Which systems are authoritative for each key entity?
3. Where do APIs/events exist today?
4. What data is governed centrally vs by domain?
5. Which single data product would produce measurable value fastest?
