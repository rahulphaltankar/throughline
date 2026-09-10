# Claude integration

The project Skill lives at the repository root under:

```text
.claude/skills/solution-blueprint/SKILL.md
```

That layout is intentional. Claude Code discovers project Skills from `.claude/skills/<skill-name>/SKILL.md`. The Skill uses progressive disclosure: the main instructions are kept compact and supporting material lives under `reference/`.

For Claude.ai, the `solution-blueprint-skill.zip` package can be uploaded as a custom Skill.

Do not assume that merely mounting a repository makes its contents safe. Review repository Skills as executable instructions and treat the repository as part of the agent trust boundary.
