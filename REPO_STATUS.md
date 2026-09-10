# Repository status

`v0.2 artefact planner`. This is a foundation, not a product.

## Implemented and tested

- Canonical artefact registry: 58 typed artefacts with dependency edges.
- Archetype routing: 11 solution classes, deterministic keyword rules.
- **Transitive dependency closure.** Archetype manifests declare intent; the
  registry owns every dependency edge. All 11 archetypes resolve to a valid,
  acyclic graph — verified exhaustively by `scripts/validate_ontology.py`.
- **Real dependency-ready frontier.** An artefact is on the frontier only when
  every artefact it requires is satisfied.
- **Skill bindings.** `produced_by` in the registry; 12 artefact bindings resolve to a
  real `.claude/skills/<dir>/SKILL.md`, enforced by tests.
- **One canonical artefact output contract**, machine-readable in
  `ontology/artefact-contract.yaml`.
- **Tier-0 gate** that parses frontmatter, validates against the ontology,
  rejects unknown artefact types, and enforces dependency coverage.
- Deliberately-broken fixtures proving the gate rejects false positives.
- Intake contract (as a dataclass), artefact plan as JSON + Markdown.
- PP20 benchmark fixtures, local execution runner, and pipeline.
- Tests and CI, including the gate suite and ontology validation.

## Not implemented

- **Real artefact generation.** The provider-independent runner's only adapter
  copies controlled fixtures; no model/provider adapter exists.
- **Producers for 46 of 58 artefact types.** Twelve are bound to a Skill.
- Gate tiers 1–4: structural predicates over content, adversarial review,
  calibrated rubric judgement, human validation.
- Persistent ledger, artefact versioning, content-hash staleness propagation,
  acceptance hashes.
- Human approval objects and an approval inbox. The plan names the human
  decisions; it does not model or record them.
- Calibrated judge; enforcement of principle 6 (author ≠ evaluator).
- PMO calculation engine. WBS, estimation, resource plan, schedule and budget
  are artefact *types* in the registry. Nothing computes them.
- Technology research adapters; architecture diagram generation.
- Intake schema enforcement (`schemas/intake.schema.json` is not read).
- Any deployment or execution adapter. Out of scope for the blueprint layer.

## Deliberate non-goals for this version

No autonomy. No production access. No LLM call inside `src/throughline/`.
The artefact graph should be provably correct before anything is built on it.
