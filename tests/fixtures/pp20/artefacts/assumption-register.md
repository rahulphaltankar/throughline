---
id: PP20-AR01
type: assumption-register
schema_version: 1
produced_by: skill:assumption-register
inputs:
- id: PP20-A01
  type: problem-frame
status: proposed
evidence:
- claim: The intake does not provide measured reconciliation delay or source-system capability data.
  class: observed
  source: projects/pp20/problem.yaml
  confidence: high
assumptions:
- id: AR-A1
  statement: Identifier inconsistency is a material source of operational delay.
  validation: Measure identifier conflicts and their impact in a selected pilot flow.
- id: AR-A2
  statement: Relevant source systems expose sufficient metadata and interfaces for the pilot.
  validation: Inventory interfaces, metadata, access constraints, and licensing with system owners.
open_questions:
- id: AR-Q1
  question: What is the impact if source-system access is unavailable during pilot discovery?
  owner: Enterprise Architect
review_required: false
---
# Assumption Register — PP20

## Assumption register

| ID | Assumption | Owner | Blast radius |
|---|---|---|---|
| AR-A1 | Identifier inconsistency materially affects the pilot flow | Enterprise Architect | Value case and scope |
| AR-A2 | Source systems expose usable metadata and interfaces | Integration Lead | Technical feasibility |

## Evidence boundary

The intake supplies the problem statement but no independent operational measurements or interface inventory.

## Validation plan

- Measure conflict frequency and impact in the selected pilot flow.
- Confirm interface, metadata, access, and licensing conditions with accountable owners.

## Expiry and impact

Reassess both assumptions before scope freeze; invalidate the pilot design if either is materially false.
