---
id: PP20-A05
type: solution-options
status: proposed
evidence_classes: derived, assumed
inputs: [PP20-A02, PP20-A04]
---
# Solution Options — PP20

## Evaluation criteria
Value to pilot use case; semantic expressiveness; time to first value; integration burden; governance; scalability; skills; lock-in; cost; reversibility.

## Option A — Lakehouse/data-product semantic layer
Use a governed analytical/data platform plus a canonical model and reusable data products. Strong for analytics and data engineering; weaker where deep relationship traversal is the core requirement.

## Option B — Knowledge graph-first layer
Represent entities/relationships explicitly in a graph with ontology controls and expose graph/API access. Strong semantic traversal and traceability; higher modelling/governance burden.

## Option C — Hybrid semantic integration layer (recommended candidate)
Use a governed data platform for data products and lineage, an ontology/knowledge graph for cross-domain semantics, and APIs/events for operational integration. Keep authoritative source systems unchanged.

## Comparison matrix
| Criterion | A | B | C |
|---|---:|---:|---:|
| Pilot value | High | High | High |
| Semantic depth | Medium | High | High |
| Integration flexibility | High | Medium | High |
| Governance complexity | Medium | High | High |
| Reversibility | High | Medium | High |
| Strategic fit | Medium-High | High | High |

## Sensitivities
If the pilot use case is primarily analytics, A may be sufficient. If relationship traversal/traceability dominates, B may outperform. C is preferable when both operational integration and analytical/data-product needs matter.
