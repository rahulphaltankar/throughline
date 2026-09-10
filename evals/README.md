# Evaluation strategy

## What exists

1. **Seed problem with an expected artefact graph** — `projects/pp20/problem.yaml`,
   asserted in `tests/test_engine.py`.
2. **Deliberately broken artefacts for false-pass testing** — `tests/fixtures/broken/`,
   asserted in `tests/test_gate.py`. Each fixture must fail, and must fail for a
   specific declared reason.
3. **Regression checks for ontology, gate and Skill changes** — `tests/`, plus
   `scripts/validate_ontology.py`, which resolves all 11 archetypes exhaustively.

## What does not exist

4. **Human-labelled examples for an LLM-judge rubric.** There is no judge.
5. **Published gate failure rates and judge calibration metrics.** There is no
   generation, so there is no failure rate to publish. Tier-0 pass/fail over a
   fixed fixture set is not a calibration metric and must not be reported as one.

## Note on the PP20 fixtures

`tests/fixtures/pp20/` is hand-written test data. Passing the gate against it
demonstrates that the gate works. It does **not** demonstrate that Throughline
can produce artefacts — nothing in this repository does.
