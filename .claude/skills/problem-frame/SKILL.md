---
name: produce-problem-frame
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
Create a markdown artefact with YAML frontmatter containing `id`, `type`, `status`, `evidence_classes`, `assumptions`, `open_questions`, and `inputs`. Then use these sections: Source statement; Problem; Who is affected; Evidence; Impact; Desired outcomes; In scope; Out of scope; Hypotheses; Unknowns; Falsification questions.

## Gate readiness
The artefact must have at least one evidence item, one explicit assumption or an explicit statement that none are required, and at least one falsification question.
