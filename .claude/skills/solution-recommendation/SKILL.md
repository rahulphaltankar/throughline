---
name: solution-recommendation
description: Produce a decision-ready end-to-end solution recommendation from validated upstream artefacts, including architecture, data flows, technology choices, delivery plan, PMO estimate, deployment, operations, risks, and decision points. Use when an executive or delivery team needs a coherent first-pass solution blueprint without implementing it.
---
# Produce Solution Recommendation

Produce exactly one artefact: `solution-recommendation`.

This is the principal solutioning Skill. It must synthesize upstream artefacts rather than independently inventing them.

## Required coverage
1. Executive recommendation
2. Problem and evidence boundary
3. Scope / out of scope
4. Target capabilities
5. Recommended solution and alternatives
6. Context, logical, data, integration, security and deployment architecture
7. Data flows and ownership
8. AI/GenAI applicability and architecture, only if justified
9. Technology/platform options with rationale
10. Build/buy/partner approach
11. Delivery workstreams and WBS
12. Effort and duration ranges with confidence and assumptions
13. Resource / skill profile
14. Dependencies and critical path
15. Budget ranges and recurring run-cost logic
16. Test and assurance approach
17. Deployment / migration / cutover
18. Operating model, SLOs, support and runbooks
19. Security/privacy/regulatory considerations
20. Change, training and adoption
21. RAID and decision log
22. Human decisions required
23. Evidence gaps
24. Recommended next actions

## Architecture rule
Use Mermaid diagrams where useful. Keep logical and physical architecture separate. Never imply an internal OEM integration is confirmed unless it is evidenced.

## PMO rule
Provide ranges, not false precision. Separate one-time implementation cost from recurring run cost. Explain the estimation basis and major cost drivers.

## Evidence rule
Every material external fact must be cited. Every internal/OEM-specific inference must be marked as assumption or requires validation.

## Output contract
Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: solution-recommendation` and `produced_by: skill:solution-recommendation`.

## Gate readiness
Every `evidence` entry needs a class, source and confidence. Every assumption
needs a validation method. Every open question needs an owner. This artefact is
`human_required`, so it must set `review_required: true`.

The registry requires these headings verbatim: `## Executive recommendation`,
`## Recommended solution`, `## Architecture`, `## Delivery plan`, `## Budget`,
`## Operating model`, `## Human decisions required`.

This artefact also requires `kpi-model` upstream. Resolve the accepted model
before writing the recommendation; a recommendation with no agreed baseline or
target measure cannot be judged.

## Scope honesty
This Skill produces one artefact in a much larger plan. Run
`python -m throughline.cli plan <intake>` to see the full artefact set the
problem actually requires. Do not describe this artefact, or the bound artefact
slice it belongs to, as a complete solution blueprint.

The gate checks structure only. Passing it does not make the recommendation
correct, evidenced, approved, or production-ready.
