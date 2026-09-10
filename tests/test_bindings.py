"""Every Skill binding must resolve, and Skill metadata must be consistent."""
from pathlib import Path
import re

import yaml

from throughline.engine import build_blueprint, load_registry

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"

CHAIN_SKILLS = [
    "assumption-register",
    "business-objectives",
    "problem-frame",
    "evidence-brief",
    "current-state-assessment",
    "kpi-model",
    "open-questions",
    "requirements",
    "solution-options",
    "solution-recommendation",
    "stakeholder-map",
]


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no frontmatter"
    end = text.find("\n---\n", 3)
    assert end != -1, f"{path} frontmatter is unterminated"
    return yaml.safe_load(text[4:end + 1])


def test_expected_skill_set():
    assert [p.name for p in skill_dirs()] == sorted(CHAIN_SKILLS + ["solution-blueprint"])


def test_no_orphan_produce_directories():
    """The pre-repair tree carried empty `produce-*` shells from an old layout."""
    orphans = [p.name for p in SKILLS.iterdir() if p.name.startswith("produce-")]
    assert orphans == []


def test_every_skill_dir_has_a_skill_md():
    for d in skill_dirs():
        assert (d / "SKILL.md").is_file(), f"{d} has no SKILL.md"


def test_frontmatter_name_matches_directory_name():
    """Claude Code addresses a Skill by directory; the two must not disagree."""
    for d in skill_dirs():
        fm = frontmatter(d / "SKILL.md")
        assert fm["name"] == d.name, (
            f"{d.name}/SKILL.md declares name {fm['name']!r}"
        )
        assert re.fullmatch(r"[a-z0-9-]+", fm["name"])
        assert fm.get("description", "").strip(), f"{d.name} has no description"


def test_every_registry_binding_resolves_to_a_real_skill():
    registry = load_registry(ROOT)
    bound = {aid: spec for aid, spec in registry.items() if spec.produced_by}
    assert bound, "no artefact has a produced_by binding"
    for aid, spec in bound.items():
        assert spec.produced_by.startswith("skill:"), aid
        skill_md = SKILLS / spec.skill / "SKILL.md"
        assert skill_md.is_file(), f"{aid} -> {spec.produced_by} does not resolve"


def test_bound_artefacts_are_exactly_the_expected_set():
    registry = load_registry(ROOT)
    bound = sorted(aid for aid, spec in registry.items() if spec.produced_by)
    assert bound == sorted([
        "acceptance-criteria",
        "assumption-register",
        "business-objectives",
        "current-state-assessment",
        "evidence-brief",
        "kpi-model",
        "open-questions",
        "problem-frame",
        "requirements",
        "solution-options",
        "solution-recommendation",
        "stakeholder-map",
    ])


def test_bound_artefacts_declare_required_sections():
    registry = load_registry(ROOT)
    for aid, spec in registry.items():
        if spec.produced_by:
            assert spec.required_sections, f"{aid} is bound but declares no required_sections"


def test_unbound_artefacts_declare_no_sections():
    """required_sections only means something if a producer exists."""
    registry = load_registry(ROOT)
    for aid, spec in registry.items():
        if not spec.produced_by:
            assert not spec.required_sections, f"{aid} is unbound but declares sections"


def test_malformed_produced_by_is_rejected():
    from throughline.model import ArtifactSpec
    import pytest

    spec = ArtifactSpec(
        id="x", name="X", purpose="p", capability="c", produced_by="problem-frame"
    )
    with pytest.raises(ValueError, match="malformed produced_by"):
        _ = spec.skill


def test_pp20_plan_reports_binding_coverage_honestly():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert len(bp.generatable) == 12
    assert len(bp.generatable) + len(bp.ungeneratable) == len(bp.artifacts)
    assert len(bp.ungeneratable) > len(bp.generatable), (
        "most of the plan has no producer; the plan must not imply otherwise"
    )
