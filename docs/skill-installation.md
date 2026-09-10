# Installing the Skills

## Claude Code

Clone or copy this repository into a project. Skills are discovered from:

```text
.claude/skills/<name>/SKILL.md
```

The directory name is the Skill's address, and must match the `name:` in the
file's frontmatter.

## Claude.ai

```bash
make skill
```

This packages `.claude/skills/solution-blueprint/` (including its `reference/`
directory) as `dist/solution-blueprint-skill.zip` for upload through Claude's
custom Skill interface.

The six chain Skills are not packaged. They depend on repository paths
(`ontology/artefact-contract.yaml`, `docs/artefact-contract.md`) that do not
exist outside a checkout.

## Scope

The Skills are blueprint-only. They describe how to write an artefact. They do
not authorise production changes, and nothing in this repository executes
anything.
