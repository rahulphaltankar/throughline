from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude/skills/solution-blueprint/SKILL.md"


def test_claude_skill_exists_and_has_frontmatter():
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert re.search(r"^name: [a-z0-9-]+$", text, re.M)
    assert re.search(r"^description: .+", text, re.M)
    assert len(text.splitlines()) < 500
