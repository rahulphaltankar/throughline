---
name: problem-frame
description: Produce a traceable problem-frame artefact from a business pain point, idea, hypothesis, or opportunity. Use when defining what problem is being solved, who is affected, what evidence exists, what is assumed, and what outcomes matter.
---
# Produce Problem Frame

Produce exactly one artefact: `problem-frame`.

## Inputs
- Raw user/problem statement
- Any source row, document, interview notes, or evidence supplied by the user

## Method
1. Preserve the source wording before interpreting it.
2. Separate observed/cited facts from derived conclusions and assumptions.
3. Define the affected actors, trigger, business impact, desired outcome, boundaries, and hypotheses.
4. Identify what is unknown and how each material unknown could be tested.
5. Do not invent organisation-specific systems, figures, regulations, vendors, or constraints.
6. State at least one falsification question for the central hypothesis.

## Output contract
Conform to the canonical artefact contract. Do not invent a frontmatter variant.

- Machine-readable: `ontology/artefact-contract.yaml`
- Explained: `docs/artefact-contract.md`
- Packaged copy: `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

Set `type: problem-frame` and `produced_by: skill:problem-frame`. Reference the
originating intake as an input of type `intake`.

Body sections: Source statement; Problem; Who is affected; Evidence; Impact;
Desired outcomes; In scope; Out of scope; Hypotheses; Unknowns; Falsification
questions.

## Gate readiness
`problem-frame` is `evidence_required`, so the `evidence` list must be non-empty
and every entry needs a class, source and confidence. Every assumption needs a
validation method. The registry requires these headings to be present verbatim:
`## Problem`, `## Evidence`, `## Hypotheses`, `## Falsification questions`.

The gate checks structure only. Passing it does not make the frame correct.
