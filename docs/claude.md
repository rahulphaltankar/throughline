# Claude integration

## Skills in this repository

```text
.claude/skills/<name>/SKILL.md
```

Claude Code discovers project Skills from that layout and addresses them by
**directory name**. The `name:` in each SKILL.md frontmatter must match its
directory; `tests/test_bindings.py` enforces this.

Twelve Skills exist:

| Skill | Produces |
|---|---|
| `problem-frame` | `problem-frame` |
| `assumption-register` | `assumption-register` |
| `business-objectives` | `business-objectives` |
| `evidence-brief` | `evidence-brief` |
| `open-questions` | `open-questions` |
| `stakeholder-map` | `stakeholder-map` |
| `kpi-model` | `kpi-model` |
| `current-state-assessment` | `current-state-assessment` |
| `requirements` | `requirements` **and** `acceptance-criteria` |
| `solution-options` | `solution-options` |
| `solution-recommendation` | `solution-recommendation` |
| `solution-blueprint` | umbrella narrative Skill; produces no single typed artefact |

`requirements` is the only chain Skill bound to two artefact types.

## What a Skill binding is

The registry field `produced_by: skill:<dir>` records **which Skill knows how to
write which artefact type**. It is checked by tests and consumed by the
provider-independent runner when it creates a work order. The runner's local
adapter copies fixtures only; it does not invoke a model.

A real provider adapter will eventually interpret the Skill and do the work.
Throughline currently neither calls a model nor generates content.

## Output contract

All Skills emit artefacts conforming to the single canonical contract:

- machine-readable: `ontology/artefact-contract.yaml`
- explained: `docs/artefact-contract.md`
- packaged copy inside the umbrella Skill:
  `.claude/skills/solution-blueprint/reference/artefact-output-contract.md`

`tests/test_contract.py` keeps the three in sync. Do not introduce a variant.

## Claude.ai

`scripts/package_skill.py` zips the `solution-blueprint` Skill for upload as a
custom Skill. The eleven chain Skills have no packaging path today; they are
repository-native only.

## Trust boundary

Do not assume that mounting a repository makes its contents safe. Repository
Skills are executable instructions. Review them as code, and treat the
repository as part of the agent trust boundary.
