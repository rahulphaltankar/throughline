---
name: evidence-brief
description: Produce a cited evidence brief that tests a problem frame, separates facts from inference, records contradictions, and identifies evidence gaps. Use when solution decisions depend on external research or uncertain claims.
---
# Produce Evidence Brief

Produce exactly one artefact: `evidence-brief`.

## Method
1. Read the problem-frame and extract every material claim.
2. For each claim classify it as observed, cited, derived, or assumed.
3. Research only bounded questions that materially affect the solution.
4. Prefer primary sources; record URL, retrieval date, and source scope.
5. Seek at least one disconfirming or contradictory signal for the central hypothesis.
6. Never convert a missing fact into a confident inference.

## Output contract
Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: evidence-brief` and `produced_by: skill:evidence-brief`.
Its only registry-required input is `problem-frame`.

Body sections: Executive finding; Claim ledger; Supporting evidence; Contradicting/disconfirming evidence; Confidence; Evidence gaps; Research questions; Implications for solution design.

## Gate readiness
`evidence-brief` is `evidence_required`, so the `evidence` list must be non-empty and
every entry needs a class, source and confidence. Every assumption needs a validation method. Every open question needs an owner.
The registry requires these headings to be present verbatim: `## Claim ledger`, `## Supporting evidence`, `## Evidence gaps`

If a registry-required upstream artefact was not produced, declare it in
`unsatisfied_inputs` with a reason. Never drop a dependency silently.

The gate checks structure only. Passing it does not make the content correct.
