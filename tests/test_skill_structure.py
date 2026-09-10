from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"


def skill_files():
    return sorted(SKILLS.glob("*/SKILL.md"))


def test_all_skills_have_valid_frontmatter():
    """Previously only solution-blueprint was checked."""
    files = skill_files()
    assert len(files) == 7
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n"), path
        assert re.search(r"^name: [a-z0-9-]+$", text, re.M), path
        assert re.search(r"^description: .+", text, re.M), path
        assert len(text.splitlines()) < 500, path


def test_skill_frontmatter_parses_as_yaml():
    for path in skill_files():
        text = path.read_text(encoding="utf-8")
        end = text.find("\n---\n", 3)
        assert end != -1, f"{path} frontmatter unterminated"
        fm = yaml.safe_load(text[4:end + 1])
        assert isinstance(fm, dict)
        assert set(fm) >= {"name", "description"}


def test_no_skill_claims_autonomous_execution():
    """Skills describe how to write an artefact. They do not deploy anything."""
    banned = [
        "deploy to production",
        "execute the deployment",
        "apply the terraform",
        "push to production",
    ]
    for path in skill_files():
        text = path.read_text(encoding="utf-8").lower()
        for phrase in banned:
            assert phrase not in text, f"{path} claims execution: {phrase}"


def test_solution_blueprint_reference_is_present():
    assert (SKILLS / "solution-blueprint" / "reference" / "artefact-output-contract.md").is_file()
