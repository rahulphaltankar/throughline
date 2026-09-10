"""The gate must accept conformant artefacts and reject malformed ones.

Every file in tests/fixtures/broken/ is a deliberate false-positive probe. Each
one passed some earlier, weaker version of the gate, or would pass a gate that
only grepped for headings and evidence-class words.
"""
from pathlib import Path
import importlib.util
import sys

import pytest

from throughline.engine import build_blueprint

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "pp20" / "artefacts"
BROKEN = ROOT / "tests" / "fixtures" / "broken"


def _load_gate():
    path = ROOT / "scripts" / "gates" / "validate_artifact.py"
    spec = importlib.util.spec_from_file_location("tl_gate", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["tl_gate"] = module
    spec.loader.exec_module(module)
    return module


gate = _load_gate()


# --------------------------------------------------------------------------
# Good fixtures
# --------------------------------------------------------------------------

def pp20_fixture_paths():
    return sorted(FIXTURES.glob("*.md"))


def test_pp20_fixtures_exist():
    assert len(pp20_fixture_paths()) == 7


@pytest.mark.parametrize("path", pp20_fixture_paths(), ids=lambda p: p.stem)
def test_pp20_fixtures_pass_the_gate(path):
    failures = gate.validate(path)
    assert failures == [], f"{path.name}: {failures}"


@pytest.mark.parametrize("path", pp20_fixture_paths(), ids=lambda p: p.stem)
def test_pp20_fixture_type_matches_filename(path):
    assert gate.validate(path, path.stem) == []


# --------------------------------------------------------------------------
# Broken fixtures -- every one must be rejected
# --------------------------------------------------------------------------

def broken_fixture_paths():
    return sorted(BROKEN.glob("*.md"))


def test_broken_fixtures_exist():
    assert len(broken_fixture_paths()) >= 15


@pytest.mark.parametrize("path", broken_fixture_paths(), ids=lambda p: p.stem)
def test_every_broken_fixture_is_rejected(path):
    failures = gate.validate(path)
    assert failures, f"FALSE POSITIVE: {path.name} was accepted by the gate"


# The specific reason each probe must fail. This stops a fixture from passing
# the "must fail" test for an accidental, unrelated reason.
EXPECTED_REASON = {
    "headings-only-no-frontmatter": "does not begin with a '---' frontmatter block",
    "unknown-type": "unknown artefact type",
    "malformed-yaml": "not valid YAML",
    "frontmatter-not-a-mapping": "must be a YAML mapping",
    "missing-required-input": "neither supplied in `inputs` nor declared",
    "bad-evidence-class": "not one of ['observed', 'cited', 'derived', 'assumed']",
    "evidence-required-but-empty": "evidence_required in the registry but carries no",
    "evidence-item-missing-keys": "`evidence[1]` is missing",
    "human-required-not-reviewed": "`review_required` must be true",
    "unresolvable-skill": "does not resolve",
    "producer-contradicts-registry": "but the registry binds",
    "substring-heading-false-positive": "missing required sections: ## Evidence",
    "bogus-unsatisfied-input": "declares types that `problem-frame` does not require",
    "bad-status": "is not one of ['draft', 'proposed', 'accepted', 'stale', 'rejected']",
    "bad-schema-version": "schema_version must be 1",
    "missing-required-field": "missing required frontmatter field",
    "missing-required-section": "missing required sections",
}


@pytest.mark.parametrize("path", broken_fixture_paths(), ids=lambda p: p.stem)
def test_broken_fixture_fails_for_the_right_reason(path):
    expected = EXPECTED_REASON.get(path.stem)
    assert expected is not None, f"{path.stem} has no declared expected reason"
    blob = " | ".join(gate.validate(path))
    assert expected in blob, f"{path.stem} failed, but not for {expected!r}: {blob}"


def test_the_original_false_positive_is_dead():
    """The exact decoy that the pre-repair gate accepted as a valid artefact."""
    decoy = BROKEN / "headings-only-no-frontmatter.md"
    text = decoy.read_text(encoding="utf-8")
    # It still contains every heading the old gate looked for, plus an
    # evidence-class word -- and it must still be rejected.
    for heading in ("## Executive recommendation", "## Architecture", "## Budget"):
        assert heading in text
    assert "assumed" in text
    assert gate.validate(decoy)


# --------------------------------------------------------------------------
# Gate wiring
# --------------------------------------------------------------------------

def test_gate_rejects_a_missing_file(tmp_path):
    assert gate.validate(tmp_path / "nope.md")


def test_gate_knows_every_registry_type():
    """The gate must not carry its own artefact list."""
    registry = gate.load_registry()
    assert len(registry) == 58
    assert "problem-frame" in registry
    assert "executive-summary" not in registry


def test_unknown_type_is_rejected_not_skipped(tmp_path):
    """The pre-repair gate gave unrecognised types a free pass."""
    f = tmp_path / "x.md"
    f.write_text(
        "---\nid: X\ntype: not-a-type\nschema_version: 1\n"
        "produced_by: skill:problem-frame\ninputs: []\nstatus: draft\n"
        "evidence: []\nassumptions: []\nopen_questions: []\nreview_required: false\n"
        "---\n# X\n",
        encoding="utf-8",
    )
    failures = gate.validate(f)
    assert any("unknown artefact type" in x for x in failures)


def test_every_gateable_pp20_artefact_has_a_fixture():
    """The pipeline and the fixture set must not drift apart."""
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    for aid in bp.mvp_sequence:
        assert (FIXTURES / f"{aid}.md").is_file(), f"no fixture for {aid}"
