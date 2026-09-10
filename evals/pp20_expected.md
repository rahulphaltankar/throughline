# PP20 benchmark

## What is checked today (automated)

`scripts/run_pp20_pipeline.py` gates the twelve hand-written PP20 fixtures for
structural conformance: canonical frontmatter, known artefact type, dependency
coverage, evidence shape, human-review flags, registry-declared sections.

`tests/test_engine.py` checks that the kernel plans the expected artefact graph
for PP20 and that every dependency edge is honoured by the ordering.

## What is NOT checked (requires human judgement)

The criteria below are the standard a real PP20 solution should be held to. None
of them are machine-verified, and Tier-0 conformance is not evidence of any of
them:

- preserves the supplied pain point without inventing OEM internals;
- surfaces evidence gaps;
- proposes multiple coherent solution options;
- separates logical architecture from physical choices;
- produces a usable data flow;
- treats AI as optional unless justified;
- includes PMO estimates, resources, dependencies, schedule logic and budget;
- identifies human decisions and assumptions;
- does not claim regulatory or production readiness without evidence.

Note that the last-but-one item cannot currently be satisfied by the system at
all: no PMO artefact has a producer, and nothing computes an estimate. The PP20
fixture's effort and duration figures are hand-written planning hypotheses,
declared as `assumed` evidence with no supporting model.
