---
name: produce-solution-recommendation
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
