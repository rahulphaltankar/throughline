from pathlib import Path

import pytest

from throughline.engine import (
    build_blueprint,
    close_dependencies,
    load_archetypes,
    load_registry,
    seed_artifacts,
    topological_order,
)

ROOT = Path(__file__).resolve().parents[1]


def test_registry_loads():
    r = load_registry(ROOT)
    assert "problem-frame" in r
    assert "wbs" in r
    assert "budget-plan" in r
    assert len(r) == 58


def test_pp20_selects_data_archetype():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert "data-platform" in bp.archetypes
    assert "ontology" in bp.artifacts
    assert "api-contracts" in bp.artifacts
    assert "wbs" in bp.artifacts
    assert "delivery-schedule" in bp.artifacts


def test_graph_is_acyclic_and_ordered():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert len(bp.artifacts) >= 35
    assert bp.artifacts.index("requirements") < bp.artifacts.index("acceptance-criteria")
    assert bp.artifacts.index("wbs") < bp.artifacts.index("estimation")


def test_topological_order_respects_every_edge():
    """Not just a few spot checks: every dependency edge must be honoured."""
    registry = load_registry(ROOT)
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    position = {aid: i for i, aid in enumerate(bp.artifacts)}
    for aid in bp.artifacts:
        for req in registry[aid].requires:
            assert position[req] < position[aid], f"{req} must precede {aid}"


def test_topological_order_rejects_incomplete_set():
    registry = load_registry(ROOT)
    with pytest.raises(ValueError, match="requires missing artefacts"):
        topological_order(["evidence-brief"], registry)


def test_closure_pulls_in_transitive_dependencies():
    registry = load_registry(ROOT)
    closed, added = close_dependencies(["security-threat-model"], registry)
    # security-threat-model -> target-architecture, data-lineage -> ... -> problem-frame
    for expected in ("data-lineage", "data-products", "ontology", "data-model", "problem-frame"):
        assert expected in closed
    assert "security-threat-model" in closed
    assert "data-lineage" in added
    # the closed set must now sort cleanly
    topological_order(closed, registry)


def test_closure_rejects_unknown_artefact():
    registry = load_registry(ROOT)
    with pytest.raises(ValueError, match="Unknown artefact id"):
        close_dependencies(["not-a-real-artefact"], registry)


def test_seed_and_closure_are_reported_separately():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert set(bp.seeded_artifacts).issubset(set(bp.artifacts))
    assert set(bp.closure_added).issubset(set(bp.artifacts))
    assert not set(bp.seeded_artifacts) & set(bp.closure_added)
    assert len(bp.seeded_artifacts) + len(bp.closure_added) == len(bp.artifacts)


def test_kernel_imports_no_llm_or_network_library():
    """CONSTITUTION.md principle 2: the kernel must stay deterministic.

    Checks real imports via the AST, not prose, so the module docstrings may
    discuss the boundary without tripping the test.
    """
    import ast

    banned = {
        "anthropic", "openai", "cohere", "google", "litellm", "langchain",
        "requests", "httpx", "urllib", "http", "socket", "aiohttp", "subprocess",
    }
    for path in (ROOT / "src" / "throughline").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                root_pkg = name.split(".")[0]
                assert root_pkg not in banned, (
                    f"{path.name} imports {name!r}; the kernel must not reach "
                    f"an LLM, the network, or a subprocess"
                )


def test_non_data_intake_resolves(tmp_path):
    """The pre-repair kernel crashed on any intake without a data archetype."""
    intake = tmp_path / "plain.yaml"
    intake.write_text(
        "id: PLAIN\n"
        "title: Improve expense approval turnaround\n"
        "organisation: Acme\n"
        "problem: Expense approvals take too long and managers chase paperwork.\n",
        encoding="utf-8",
    )
    bp = build_blueprint(ROOT, intake)
    assert "general-solution" in bp.archetypes
    assert "security-threat-model" in bp.artifacts
    assert "data-lineage" in bp.artifacts  # pulled in by closure
    assert "data-lineage" in bp.closure_added


def test_every_archetype_resolves():
    """Exhaustive: no archetype may produce an unresolvable graph."""
    registry = load_registry(ROOT)
    archetypes = load_archetypes(ROOT)
    assert len(archetypes) == 11
    for aid in archetypes:
        combo = [aid] if aid == "general-solution" else [aid, "general-solution"]
        seeds = seed_artifacts(combo, archetypes)
        closed, _ = close_dependencies(seeds, registry)
        order = topological_order(closed, registry)
        assert order, f"{aid} produced an empty plan"


def test_every_archetype_names_only_known_artefacts():
    registry = load_registry(ROOT)
    for aid, arch in load_archetypes(ROOT).items():
        for artefact in arch.get("required_artifacts", []):
            assert artefact in registry, f"archetype {aid} names unknown artefact {artefact}"


def test_registry_requires_edges_all_resolve():
    registry = load_registry(ROOT)
    for aid, spec in registry.items():
        for req in spec.requires:
            assert req in registry, f"{aid} requires unknown artefact {req}"
