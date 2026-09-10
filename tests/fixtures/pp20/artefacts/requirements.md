---
id: PP20-A04
type: requirements
schema_version: 1
produced_by: skill:requirements
inputs:
- id: PP20-A01
  type: problem-frame
- id: PP20-A02
  type: evidence-brief
- id: PP20-A03
  type: current-state-assessment
unsatisfied_inputs:
- type: business-objectives
  reason: No Skill currently produces business-objectives. Objectives are inferred from the intake rather
    than derived from an accepted artefact.
- type: stakeholder-map
  reason: No Skill currently produces stakeholder-map. Requirement ownership is therefore unattributed.
status: proposed
evidence:
- claim: Requirements are derived from the current-state assessment and problem frame, not from confirmed
    internal discovery.
  class: derived
  source: PP20-A01, PP20-A03
  confidence: low
- claim: Exact verification thresholds cannot be set until a baseline is measured.
  class: assumed
  source: No baseline measurement supplied with the intake.
  confidence: medium
assumptions:
- id: A6
  statement: A single cross-domain use case can be agreed as the pilot scope.
  validation: Confirm the pilot use case and accountable owner before acceptance criteria are frozen.
open_questions:
- id: Q12
  question: Which measurable baseline will thresholds be set against?
  owner: CDIO / Enterprise Architect (intake buyer)
review_required: false
---
# Requirements — PP20

## Business requirements
- BR-01: Enable a defined cross-domain use case with less manual reconciliation.
- BR-02: Establish accountable ownership for the pilot data product and semantic definitions.
- BR-03: Provide measurable evidence of value before wider rollout.

## Functional requirements
- FR-01: Resolve defined business entities to canonical identifiers.
- FR-02: Expose governed semantic mappings through reusable interfaces.
- FR-03: Capture lineage from source system to canonical representation and consuming product.
- FR-04: Support change/versioning of semantic definitions.
- FR-05: Provide data-quality status for the pilot product.

## Non-functional requirements
- NFR-01: All mappings must be attributable to a source system and owner.
- NFR-02: Access must be policy-controlled and auditable.
- NFR-03: The architecture must support incremental onboarding of additional domains.
- NFR-04: Failure of the semantic layer must not silently corrupt authoritative source systems.

## Verification
Every requirement requires a corresponding acceptance test or review condition. Exact thresholds are intentionally deferred until baseline measurement is obtained.
