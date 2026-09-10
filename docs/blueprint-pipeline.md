# Blueprint Pipeline

The first real Throughline pipeline is an artefact-producing chain:

`problem-frame -> evidence-brief -> current-state-assessment -> requirements -> solution-options -> solution-recommendation`

Each step produces one typed artefact, and each downstream step consumes upstream artefacts. Claude Skills are procedural packaging; the repository ontology and gate scripts are the control layer.

## Human freeze points

- Problem significance / truth: human accountable owner
- Acceptance criteria: human freeze before material downstream commitment
- Material solution recommendation: human decision
- Regulatory/legal attestation: human only

## Benchmark

`examples/pp20/` is a benchmark instance of the generic pipeline. It does not change the generality of the engine.
