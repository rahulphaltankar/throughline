from pathlib import Path

from throughline.engine import build_blueprint, load_archetypes, load_registry

ROOT = Path(__file__).resolve().parents[1]


def test_registry_loads():
    r = load_registry(ROOT)
    assert "problem-frame" in r
    assert "wbs" in r
    assert "budget-plan" in r


def test_pp20_selects_data_archetype():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert "data-platform" in bp.archetypes
    assert "ontology" in bp.artifacts
    assert "api-contracts" in bp.artifacts
    assert "wbs" in bp.artifacts
    assert "delivery-schedule" in bp.artifacts


def test_graph_is_acyclic():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert len(bp.artifacts) >= 35
    assert bp.artifacts.index("requirements") < bp.artifacts.index("acceptance-criteria")
    assert bp.artifacts.index("wbs") < bp.artifacts.index("estimation")
