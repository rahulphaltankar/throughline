---
name: open-questions
description: Record unresolved solutioning questions with priority, accountable owners, and resolution methods from a problem frame. Use when uncertainty must be governed rather than hidden.
---
# Produce Open Questions Register

Produce exactly one artefact: `open-questions`.

## Method

Turn unresolved material points in the `problem-frame` into answerable
questions. Prioritise by decision impact and urgency, not by speculation. Assign
an accountable role where known; otherwise make ownership itself an explicit
question. Specify a practical resolution method such as interview, measurement,
document review, or experiment.

## Output contract

Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: open-questions` and `produced_by: skill:open-questions`. Its only
registry-required input is `problem-frame`.

Body sections: Open questions; Prioritisation; Owners; Resolution methods.
Avoid restating assumptions as questions unless answering them would change a
material decision.

## Gate readiness

Every assumption needs a validation method and every open question needs an
owner. The registry requires these headings verbatim: `## Open questions`,
`## Prioritisation`, `## Owners`, `## Resolution methods`.

The gate checks structure only. Passing it does not resolve the questions.
