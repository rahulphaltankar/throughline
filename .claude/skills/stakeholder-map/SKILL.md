---
name: stakeholder-map
description: Identify affected stakeholders, influence, interests, accountability, and validation gaps from a problem frame. Use before requirements, change planning, or governance decisions.
---
# Produce Stakeholder Map

Produce exactly one artefact: `stakeholder-map`.

## Method

Map people and roles only to the evidence available in the `problem-frame`.
Separate named stakeholders from inferred roles, and never imply that a person
has accepted accountability. Record missing ownership as an open question.
Describe influence and interests as hypotheses where they have not been
observed or confirmed.

## Output contract

Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: stakeholder-map` and `produced_by: skill:stakeholder-map`. Its only
registry-required input is `problem-frame`.

Body sections: Stakeholder register; Influence and interests; Accountability;
Validation questions. Include role, relationship to the problem, decision or
consultation responsibility, and confidence for material entries.

## Gate readiness

Every assumption needs a validation method and every open question needs an
owner. The registry requires these headings verbatim: `## Stakeholder register`,
`## Influence and interests`, `## Accountability`, `## Validation questions`.

The gate checks structure only. Passing it does not appoint an accountable owner.
