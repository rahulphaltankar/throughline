---
name: solution-options
description: Produce and compare materially different solution approaches from requirements and evidence. Use when selecting architecture, technology, sourcing, or delivery approaches.
---
# Produce Solution Options

Produce exactly one artefact: `solution-options`.

## Method
Generate at least two credible alternatives for a material decision. Compare them against the frozen requirements, implementation complexity, data implications, security/privacy, operating burden, skills, vendor dependence, cost range, delivery duration, reversibility, and strategic fit.

Do not create a shopping list. Evaluate architectures as coherent systems.

## Output contract
Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: solution-options` and `produced_by: skill:solution-options`.
Its registry-required inputs are `requirements` and `evidence-brief`.

Body sections: Decision to make; Evaluation criteria; Option A; Option B; Option C/Hybrid when justified; Comparison matrix; Sensitivities; Recommendation candidate; Information needed before commitment.

## Gate readiness
Every `evidence` entry needs a class, source and confidence. Every assumption needs a validation method. Every open question needs an owner.
The registry requires these headings to be present verbatim: `## Evaluation criteria`, `## Option A...`, `## Option B...`, `## Comparison matrix`

If a registry-required upstream artefact was not produced, declare it in
`unsatisfied_inputs` with a reason. Never drop a dependency silently.

The gate checks structure only. Passing it does not make the content correct.
