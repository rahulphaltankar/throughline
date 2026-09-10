---
name: solution-blueprint
description: Build a complete, decision-ready solution blueprint from a problem statement, pain point, opportunity, hypothesis, or transformation request. Use when the user asks how a solution should be defined, designed, architected, costed, planned, governed, deployed, operated, or handed over without executing production changes.
---

# Solution Blueprint

## Purpose

Turn an imperfect business or technical problem into a structured, traceable, first-pass solution blueprint.

Do **not** jump directly to technology choices. The work must establish the problem, evidence, requirements, solution options, architecture, data, AI applicability, security/privacy/regulatory considerations, commercial case, delivery plan, project-management model, deployment approach, operating model, change plan, and evidence needs.

This Skill is a **solutioning Skill**, not an implementation/deployment Skill.

## Operating rules

1. Treat the input as an intake hypothesis, not truth.
2. Preserve the user's source claims and label their evidential status.
3. Never invent OEM-specific facts, system names, interfaces, costs, regulations, vendors, or constraints. Mark them `assumed` or `requires validation`.
4. Start with the smallest useful problem frame.
5. Identify the likely solution archetypes before generating detailed artefacts.
6. Use dependency order rather than narrative phase order.
7. Produce a coherent first draft even when information is incomplete; expose the missing information explicitly.
8. Compare at least two plausible solution approaches before selecting a recommendation when the decision is material.
9. For architecture, distinguish logical design from physical implementation choices.
10. Assess whether AI/GenAI is actually justified; do not force AI into a conventional problem.
11. Include delivery/project-management outputs: WBS, estimation basis, resource/skills plan, dependencies, schedule, critical-path assumptions, budget and RAID.
12. Include deployment and BAU outputs even when the user only asked for “architecture”.
13. Treat security, privacy, regulatory and governance as design inputs, not a final checklist.
14. Separate facts, derived conclusions, assumptions, recommendations and open questions.
15. Never represent an LLM judgement as legal/regulatory attestation.

## Canonical workflow

Work through the artefact dependency graph in this order of intent:

### 1. Frame
Produce or refine:
- Problem Frame
- Evidence Brief
- Stakeholder Map
- Current-State Assessment
- Business Objectives & Outcomes
- KPI Model
- Assumption Register
- Open Questions

### 2. Define
Produce:
- Requirements Catalogue
- Acceptance Criteria
- Traceability Matrix

Freeze acceptance criteria before making downstream recommendations.

### 3. Evaluate
Produce:
- Solution Option Set
- Solution Recommendation
- Decision Records as needed

Always explain why the recommendation wins and what could make it wrong.

### 4. Architect
Select the required architecture artefacts:
- Target-State Architecture
- Logical Architecture
- Physical / Deployment Architecture
- Data Domain Model
- Canonical Ontology
- Data Products
- Data Flow / Lineage
- Integration Catalogue
- API / Interface Contracts
- AI Applicability Assessment
- AI Architecture
- AI Evaluation Plan

Only include specialised artefacts when the problem warrants them.

### 5. Trust / Assurance
Assess:
- Threat Model / Security Architecture
- Privacy Assessment
- Regulatory Applicability / Classification
- Controls & Compliance Matrix
- Risk Register

For regulated decisions, prepare evidence and decision questions for the responsible human; do not attest on their behalf.

### 6. Commercialise
Produce:
- Business Case
- TCO / Cost Model
- ROI / Benefits Model
- Vendor / Technology Evaluation
- Build / Buy / Partner Assessment

Technology recommendations must include rationale, trade-offs, lock-in, skills impact and indicative economics.

### 7. Plan delivery
Produce:
- Delivery Strategy
- WBS
- Effort / Estimation Model
- Resource / Skills Plan
- Dependency Map
- Delivery Schedule / Roadmap
- Budget / Funding Plan
- RAID Log

Use ranges and confidence levels instead of false precision.

### 8. Assure and release-plan
Produce:
- Test Strategy
- Test Plan / Test Suite
- Migration / Cutover Plan where needed
- Release Plan
- Operational Readiness Assessment

### 9. Operate and transition
Produce:
- Service / Operating Model
- Runbook
- Observability Specification
- Change Management Plan
- Training / Adoption Plan where appropriate
- Benefits Realisation Plan
- Evidence Pack
- Handover Pack
- Continuous Improvement Plan
- Retirement / Decommission Plan when relevant

## Output format

Unless the user requests otherwise, deliver a professional solution blueprint with these sections:

1. Executive summary
2. Problem and evidence
3. Objectives and success measures
4. Scope / out of scope
5. Assumptions / unknowns
6. Stakeholders and operating context
7. Requirements
8. Solution options
9. Recommended solution
10. Architecture overview
11. Data architecture and flows
12. AI/GenAI assessment and architecture where relevant
13. Integration architecture
14. Security / privacy / regulatory
15. Technology / tooling options
16. Commercial case: TCO, ROI logic, pricing assumptions
17. Delivery approach
18. WBS
19. Resource and skills plan
20. Schedule and critical path
21. Budget
22. Risks / RAID
23. Test and assurance approach
24. Deployment / migration
25. Operating model / support / SRE
26. Change / training / adoption
27. Governance and decision points
28. Evidence and traceability
29. Open questions requiring client input
30. Recommended next actions

## Artefact contract

When you emit a typed artefact rather than a narrative document, conform to the
canonical contract in `reference/artefact-output-contract.md`. There is exactly
one contract; do not invent a variant. `scripts/gates/validate_artifact.py`
enforces it and rejects unknown artefact types.

## Relationship to the kernel

The deterministic kernel decides *which* artefacts a problem needs and in what
order. Run `python -m throughline.cli plan <intake>` to get that plan rather than
inventing a workflow order here. Six artefact types currently have a Skill
binding; the rest of the plan is manual work. Do not present a subset as a
complete blueprint.

## Evidence discipline

Every material claim should be classified as:

- `observed` — supplied directly or directly verified
- `cited` — supported by an external source
- `derived` — logically derived from accepted evidence
- `assumed` — necessary working assumption, with a validation method

Do not hide uncertainty in polished prose.

## Human decision discipline

Escalate rather than silently decide when the question concerns:
- business priority;
- legal/regulatory attestation;
- residual-risk acceptance;
- production-data access;
- money/contracts/suppliers;
- regulated decisions;
- irreversible production actions;
- decommissioning or retention obligations.

Present the human with a concise decision request: decision, options, recommendation, evidence, uncertainty, consequence, and reversal cost.

## Technology recommendation discipline

Never output a “shopping list” of tools. For every material technology choice, state:

- role in the architecture;
- alternatives considered;
- fit against requirements;
- integration implications;
- delivery complexity;
- skills implications;
- operating burden;
- security/privacy implications;
- vendor lock-in;
- indicative cost category;
- reason for recommendation;
- what evidence would change the recommendation.

## PMO estimation discipline

Do not present AI-generated durations as facts. Use:

- effort range;
- calendar-duration range;
- confidence;
- assumptions;
- dependencies;
- resource profile;
- critical path;
- contingency;
- basis of estimate.

For budget, distinguish one-time implementation from recurring run costs.

## Completion criterion

The blueprint is “complete enough for review” when:

- the problem and objective are explicit;
- major unknowns are surfaced;
- acceptance criteria exist and are frozen for the current draft;
- at least one coherent solution is described;
- architecture and data flow can be understood;
- major risks and governance constraints are identified;
- delivery, resource, schedule and budget logic exists;
- deployment and operating model are addressed;
- the human decisions required are explicit;
- every material uncertainty is visible.

Do not claim the solution is validated, approved, production-ready, or legally compliant merely because this Skill generated a blueprint.
