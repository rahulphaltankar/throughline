"""The frontier must be a real dependency-readiness predicate.

Before the repair, `frontier` was `order[:6]` -- a slice of the topological
order. That put `evidence-brief` on the PP20 frontier even though it depends on
`problem-frame`, which had not been produced.
"""
from pathlib import Path

import pytest

from throughline.engine import build_blueprint, compute_frontier, load_registry

ROOT = Path(__file__).resolve().parents[1]


def test_pp20_initial_frontier_is_exactly_problem_frame():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert bp.frontier == ["problem-frame"]


def test_pp20_frontier_excludes_evidence_brief():
    """The specific regression: evidence-brief requires problem-frame."""
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    registry = load_registry(ROOT)
    assert "problem-frame" in registry["evidence-brief"].requires
    assert "evidence-brief" not in bp.frontier


def test_every_frontier_member_has_all_dependencies_satisfied():
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    registry = load_registry(ROOT)
    for aid in bp.frontier:
        assert not registry[aid].requires, (
            f"{aid} is on the initial frontier but requires {list(registry[aid].requires)}"
        )


def test_frontier_is_not_a_slice_of_the_topological_order():
    """Guards against a regression to `order[:n]`."""
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    n = len(bp.frontier)
    assert bp.frontier != bp.artifacts[:n] or n == 1
    assert len(bp.frontier) < len(bp.artifacts)


def test_frontier_advances_as_artefacts_are_satisfied():
    registry = load_registry(ROOT)
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")

    satisfied: list[str] = []
    frontier = compute_frontier(bp.artifacts, registry, satisfied)
    assert frontier == ["problem-frame"]

    satisfied.append("problem-frame")
    frontier = compute_frontier(bp.artifacts, registry, satisfied)
    assert "evidence-brief" in frontier
    assert "stakeholder-map" in frontier
    assert "business-objectives" in frontier
    # still not ready: needs evidence-brief too
    assert "current-state-assessment" not in frontier

    satisfied.append("evidence-brief")
    frontier = compute_frontier(bp.artifacts, registry, satisfied)
    assert "current-state-assessment" in frontier


def test_draining_the_frontier_covers_the_whole_plan():
    """Repeatedly taking the frontier must schedule every artefact exactly once."""
    registry = load_registry(ROOT)
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")

    satisfied: list[str] = []
    waves = 0
    while len(satisfied) < len(bp.artifacts):
        frontier = compute_frontier(bp.artifacts, registry, satisfied)
        assert frontier, "frontier went empty before the plan was complete"
        for aid in frontier:
            for req in registry[aid].requires:
                assert req in satisfied
        satisfied.extend(frontier)
        waves += 1
        assert waves < 100, "runaway loop"

    assert sorted(satisfied) == sorted(bp.artifacts)
    assert len(set(satisfied)) == len(satisfied)
    assert waves > 1, "a multi-layer graph must take more than one wave"


def test_satisfied_artefacts_must_be_in_the_plan():
    registry = load_registry(ROOT)
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    with pytest.raises(ValueError, match="outside the selected set"):
        compute_frontier(bp.artifacts, registry, ["not-in-this-plan"])


def test_completed_plan_has_an_empty_frontier():
    registry = load_registry(ROOT)
    bp = build_blueprint(ROOT, ROOT / "projects/pp20/problem.yaml")
    assert compute_frontier(bp.artifacts, registry, bp.artifacts) == []
