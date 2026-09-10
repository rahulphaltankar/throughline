---
name: assumption-register
description: Create a falsifiable assumption register with evidence boundaries, owners, validation actions, expiry, and impact. Use when a problem frame contains material unknowns.
---
# Produce Assumption Register

Produce exactly one artefact: `assumption-register`.

## Method

Extract material assumptions from the `problem-frame`; do not convert unknowns
into facts. For each assumption, state why it matters, who owns validation, how
it can be tested, when it expires, and the consequence if it is false. Keep
claims linked to supplied evidence and classify the evidence boundary honestly.

## Output contract

Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: assumption-register` and `produced_by: skill:assumption-register`.
Its only registry-required input is `problem-frame`.

Body sections: Assumption register; Evidence boundary; Validation plan; Expiry
and impact. Give each material assumption an ID, owner, validation method,
expiry trigger or date, and blast radius.

## Gate readiness

`assumption-register` is `evidence_required`, so `evidence` must be non-empty
and every entry needs class, source, and confidence. Every assumption needs a
validation method and every open question needs an owner. The registry requires
these headings verbatim: `## Assumption register`, `## Evidence boundary`,
`## Validation plan`, `## Expiry and impact`.

The gate checks structure only. Passing it does not validate an assumption.
