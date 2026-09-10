---
name: requirements
description: Produce a traceable requirements catalogue and frozen draft acceptance criteria from the problem, evidence, stakeholders, current state, and objectives. Use when converting an opportunity into testable requirements.
---
# Produce Requirements

This Skill produces **two** artefact types, and the registry binds both to it:
`requirements` and `acceptance-criteria`. Write them as two separate files, each
with its own frontmatter. Every other chain Skill produces exactly one artefact.

## Method
Create business, functional, data, integration, security, privacy, operational, and quality requirements only where justified. Give every requirement an ID, priority, rationale, source/evidence, and verification method.

## Acceptance criteria
Use testable conditions. Do not use adjectives like scalable, secure, intuitive, or real-time without a measurable definition. Treat the resulting acceptance criteria as a draft that requires human freeze/approval before downstream work is considered committed.

## Output contract
Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

For the catalogue set `type: requirements` and `produced_by: skill:requirements`.
For the criteria set `type: acceptance-criteria` and the same `produced_by`.

Body sections for `requirements`: Business requirements; Functional requirements;
Non-functional requirements; Verification.

Body sections for `acceptance-criteria`: Business outcomes; then whatever
categories the solution needs; Freeze rule.

## Gate readiness
No orphan requirement. Every requirement has a source/rationale and verification
method. `requirements` is `evidence_required`, so its `evidence` list must be
non-empty. `acceptance-criteria` is `human_required`, so it must set
`review_required: true`.

The registry requires these headings verbatim:

- `requirements`: `## Business requirements`, `## Functional requirements`, `## Non-functional requirements`, `## Verification`
- `acceptance-criteria`: `## Business outcomes`, `## Freeze rule`

`requirements` also requires `business-objectives` and `stakeholder-map`
upstream. **No Skill currently produces either.** Until one does, declare them in
`unsatisfied_inputs` with a reason — do not pretend the requirement set is
properly sourced.

The gate checks structure only. Passing it does not make the requirements right,
and it does not freeze the acceptance criteria. Only an accountable human can.
