# Claude integration

## Skills in this repository

```text
.claude/skills/<name>/SKILL.md
```

Claude Code discovers project Skills from that layout and addresses them by
**directory name**. The `name:` in each SKILL.md frontmatter must match its
directory; `tests/test_bindings.py` enforces this.

Seven Skills exist:

| Skill | Produces |
|---|---|
| `problem-frame` | `problem-frame` |
| `evidence-brief` | `evidence-brief` |
| `current-state-assessment` | `current-state-assessment` |
| `requirements` | `requirements` **and** `acceptance-criteria` |
| `solution-options` | `solution-options` |
| `solution-recommendation` | `solution-recommendation` |
| `solution-blueprint` | umbrella narrative Skill; produces no single typed artefact |

`requirements` is the only chain Skill bound to two artefact types.

## What a Skill binding is

The registry field `produced_by: skill:<dir>` records **which Skill knows how to
write which artefact type**. It is a declaration, checked by tests. It is not a
dispatch mechanism: no code reads a binding and invokes anything.

A human or an agent must read the Skill and do the work. Throughline neither
calls a model nor writes an artefact.

## Output contract

All Skills emit artefacts conforming to the single canonical contract:

- machine-readable: `ontology/artefact-contract.yaml`
- explained: `docs/artefact-contract.md`
- packaged copy inside the umbrella Skill:
  `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

`tests/test_contract.py` keeps the three in sync. Do not introduce a variant.

## Claude.ai

`scripts/package_skill.py` zips the `solution-blueprint` Skill for upload as a
custom Skill. The six chain Skills have no packaging path today; they are
repository-native only.

## Trust boundary

Do not assume that mounting a repository makes its contents safe. Repository
Skills are executable instructions. Review them as code, and treat the
repository as part of the agent trust boundary.
