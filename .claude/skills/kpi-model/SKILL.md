---
name: kpi-model
description: Define outcome-linked measures, baselines, targets, measurement methods, and owners from agreed business objectives. Use before evaluating a solution recommendation.
---
# Produce KPI Model

Produce exactly one artefact: `kpi-model`.

## Method

Use `business-objectives` as the sole required upstream source. Map each metric
to an objective and state its baseline, target, unit, source, measurement
method, owner, and review cadence. Do not invent baselines or targets: mark
them as assumptions with a validation method or as open questions with an owner
when they are not agreed.

## Output contract

Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: kpi-model` and `produced_by: skill:kpi-model`. Its only
registry-required input is `business-objectives`.

Body sections: Outcome-to-metric mapping; Baselines; Targets; Measurement
method; Owners and cadence.

## Gate readiness

Every assumption needs a validation method and every open question needs an
owner. The registry requires these headings verbatim:
`## Outcome-to-metric mapping`, `## Baselines`, `## Targets`,
`## Measurement method`, `## Owners and cadence`.

The gate checks structure only. Passing it does not establish a validated KPI.
