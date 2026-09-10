---
id: PP20-A04b
type: acceptance-criteria
status: proposed
evidence_classes: derived, assumed
inputs: [PP20-A04]
---
# Acceptance Criteria — PP20

## Business outcomes
- AC-01: A named pilot use case has an agreed baseline and target measure.
- AC-02: The pilot demonstrates a measurable reduction in manual reconciliation for the selected use case, threshold to be frozen after baseline measurement.

## Semantic/data
- AC-03: All pilot canonical entities have an accountable owner.
- AC-04: Every source-to-canonical mapping is traceable to a source field and mapping rule.
- AC-05: Data-quality status is visible for the pilot product.

## Integration
- AC-06: Exposed APIs/events conform to approved interface contracts.
- AC-07: No pilot component writes to authoritative source systems without explicit approval and contract.

## Security/governance
- AC-08: Access is authenticated, authorised and auditable.
- AC-09: Material risks and residual risks have named owners.

## Operational
- AC-10: Pipeline/API failure, freshness degradation and data-quality failure produce actionable alerts.

## Freeze rule
Thresholds that depend on the current baseline are intentionally marked `TBD`. A human accountable owner must freeze those thresholds before downstream architecture/delivery commitments are treated as final.
