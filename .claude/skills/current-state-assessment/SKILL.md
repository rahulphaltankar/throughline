---
name: current-state-assessment
description: Produce a current-state assessment of processes, systems, data, interfaces, ownership, constraints, and maturity from a problem frame and evidence brief. Use before designing a target solution.
---
# Produce Current-State Assessment

Produce exactly one artefact: `current-state-assessment`.

## Method
Map the current state without pretending unavailable internal detail is known. Use a confidence label on every materially uncertain system, process, data-flow, or ownership statement. Distinguish confirmed public evidence from working hypotheses that must be validated with the client.

## Output contract
Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: current-state-assessment` and `produced_by: skill:current-state-assessment`.
Its registry-required inputs are `problem-frame` and `evidence-brief`.

Body sections: Current business process; Current systems landscape; Current data landscape; Current integration landscape; Ownership/accountability; Current pain points; Constraints; Maturity observations; Known gaps; Validation questions; Implications. Include an ASCII or Mermaid context diagram when enough information exists.

## Gate readiness
`current-state-assessment` is `evidence_required`, so the `evidence` list must be non-empty and
every entry needs a class, source and confidence. Every assumption needs a validation method. Every open question needs an owner.
The registry requires these headings to be present verbatim: `## Current business process`, `## Current systems landscape`, `## Current data landscape`, `## Validation questions`

If a registry-required upstream artefact was not produced, declare it in
`unsatisfied_inputs` with a reason. Never drop a dependency silently.

The gate checks structure only. Passing it does not make the content correct.
