"""There must be exactly one artefact output contract.

The machine-readable contract in ontology/artefact-contract.yaml is the single
source of truth. The prose copy in docs/ and the packaged copy inside the Skill
must not drift away from it.
"""
from pathlib import Path

import yaml

from throughline.engine import load_contract, load_registry

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "ontology" / "artefact-contract.yaml"
DOC = ROOT / "docs" / "artefact-contract.md"
SKILL_COPY = ROOT / ".claude/skills/solution-blueprint/reference/artefact-output-contract.md"
FIXTURES = ROOT / "tests" / "fixtures" / "pp20" / "artefacts"

REQUIRED = [
    "id", "type", "schema_version", "produced_by", "inputs",
    "status", "evidence", "assumptions", "open_questions", "review_required",
]


def test_contract_declares_the_mandated_fields():
    contract = load_contract(ROOT)
    assert contract["required_fields"] == REQUIRED


def test_contract_enums():
    contract = load_contract(ROOT)
    assert contract["evidence_classes"] == ["observed", "cited", "derived", "assumed"]
    assert contract["statuses"] == ["draft", "proposed", "accepted", "stale", "rejected"]
    assert contract["schema_version"] == 1


def test_every_required_field_has_an_item_shape_or_is_scalar():
    contract = load_contract(ROOT)
    for field in ("inputs", "evidence", "assumptions", "open_questions", "unsatisfied_inputs"):
        assert field in contract["item_fields"], f"{field} has no declared item shape"


def test_prose_copies_list_the_same_required_fields():
    """Guards against the three-competing-contracts problem returning."""
    for path in (DOC, SKILL_COPY):
        text = path.read_text(encoding="utf-8")
        for field in REQUIRED:
            assert f"`{field}`" in text, f"{path.name} does not document `{field}`"


def test_prose_copies_document_no_extra_fields():
    contract = load_contract(ROOT)
    known = set(contract["required_fields"]) | set(contract["optional_fields"])
    stale = {"evidence_classes", "produced_by_skill", "recommendation"}
    for path in (DOC, SKILL_COPY):
        text = path.read_text(encoding="utf-8")
        for field in stale - known:
            assert f"`{field}`:" not in text, f"{path.name} still documents `{field}`"


def test_all_chain_skills_point_at_the_canonical_contract():
    for name in ("problem-frame", "evidence-brief", "current-state-assessment",
                 "requirements", "solution-options", "solution-recommendation"):
        text = (ROOT / ".claude/skills" / name / "SKILL.md").read_text(encoding="utf-8")
        assert "ontology/artefact-contract.yaml" in text, f"{name} does not cite the contract"
        assert "docs/artefact-contract.md" in text, f"{name} does not cite the contract doc"


def test_no_skill_defines_a_competing_frontmatter_list():
    """`evidence_classes` was the old, incompatible frontmatter field."""
    for path in (ROOT / ".claude/skills").rglob("SKILL.md"):
        text = path.read_text(encoding="utf-8")
        assert "evidence_classes" not in text, f"{path} references the retired contract"


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---\n", 3)
    return yaml.safe_load(text[4:end + 1])


def test_pp20_fixtures_use_the_canonical_contract():
    registry = load_registry(ROOT)
    contract = load_contract(ROOT)
    known = set(contract["required_fields"]) | set(contract["optional_fields"])
    for path in sorted(FIXTURES.glob("*.md")):
        fm = _frontmatter(path)
        assert set(REQUIRED).issubset(fm), f"{path.name} is missing contract fields"
        assert set(fm).issubset(known), f"{path.name} has non-contract fields"
        assert fm["schema_version"] == 1
        assert fm["type"] in registry
        spec = registry[fm["type"]]
        assert fm["produced_by"] == spec.produced_by
        if spec.human_required:
            assert fm["review_required"] is True, f"{path.name} must require review"


def test_fixture_dependency_deficits_are_declared_not_hidden():
    """The six-step chain skips real upstream artefacts. That must be visible."""
    registry = load_registry(ROOT)
    declared: dict[str, set[str]] = {}
    for path in sorted(FIXTURES.glob("*.md")):
        fm = _frontmatter(path)
        supplied = {i["type"] for i in fm["inputs"]}
        deferred = {u["type"] for u in fm.get("unsatisfied_inputs", [])}
        required = set(registry[fm["type"]].requires)
        assert required <= (supplied | deferred), f"{path.name} hides a dependency"
        if deferred:
            declared[fm["type"]] = deferred

    assert declared["requirements"] == {"business-objectives", "stakeholder-map"}
    assert declared["solution-recommendation"] == {"kpi-model"}
