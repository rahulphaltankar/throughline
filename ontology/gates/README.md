# Gates

A gate is binary, versioned, testable, and linked to at least one regression
case.

## Tier 0 — deterministic structural checks — IMPLEMENTED

`scripts/gates/validate_artifact.py`. Parses artefact frontmatter and validates
it against `ontology/artefact-contract.yaml` and `ontology/artefacts/core.yaml`:

- frontmatter parses and is a mapping
- all contract-required fields present, no unknown fields
- artefact type exists in the registry (unknown types are **rejected**)
- `schema_version` and `status` within their enums
- `produced_by` resolves to a real Skill and agrees with the registry
- `inputs` ∪ `unsatisfied_inputs` covers the registry's `requires`
- evidence entries carry a valid class, source and confidence
- `evidence_required` types carry at least one evidence entry
- `human_required` types set `review_required: true`
- registry-declared section headings present as whole lines

Regression cases: `tests/fixtures/broken/` — every file must be rejected, and
`tests/test_gate.py` asserts each fails for its specific declared reason.

## Tier 1 — structural predicates over content — NOT IMPLEMENTED

## Tier 2 — adversarial review — NOT IMPLEMENTED

## Tier 3 — calibrated rubric judgement — NOT IMPLEMENTED

Requires human-labelled calibration data that does not exist.

## Tier 4 — reality / human validation — NOT IMPLEMENTED

There is no approval object and no inbox.

---

Tier 0 validates **structure, not truth**. Passing it means an artefact is
well-formed and honest about its declared gaps. It does not mean the content is
correct, evidenced, complete or approved.
