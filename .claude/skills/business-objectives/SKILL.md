---
name: business-objectives
description: Define measurable business outcomes, objectives, constraints, and trade-offs from an established problem frame. Use before requirements and KPI design.
---
# Produce Business Objectives

Produce exactly one artefact: `business-objectives`.

## Method

Use the `problem-frame` as the evidence boundary. Translate only supported
desired outcomes into objectives; distinguish an observed constraint from an
assumption that needs validation. Do not invent financial targets, deadlines,
or executive commitments. Where a measurable target is not agreed, name the
decision and validation work needed before setting one.

## Output contract

Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: business-objectives` and `produced_by: skill:business-objectives`.
Its only registry-required input is `problem-frame`.

Body sections: Desired outcomes; Objectives; Constraints and trade-offs;
Validation questions. Give each objective an owner or explicitly record the
owner as unresolved.

## Gate readiness

Every assumption needs a validation method and every open question needs an
owner. List only the supplied `problem-frame` in `inputs`; if it is unavailable,
declare it in `unsatisfied_inputs` rather than reconstructing it from memory.
The registry requires these headings verbatim: `## Desired outcomes`,
`## Objectives`, `## Constraints and trade-offs`, `## Validation questions`.

The gate checks structure only. Passing it does not mean objectives are agreed.
