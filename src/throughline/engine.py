"""Deterministic Throughline kernel.

CONSTITUTION.md principle 2: this module, and every module under
src/throughline/, must remain free of LLM calls. Routing, dependency
resolution and frontier calculation are plain code over the ontology.
"""
from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable
import json
import re
import yaml

from .model import ArtifactSpec, Blueprint, Intake


def load_yaml(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_registry(root: Path) -> dict[str, ArtifactSpec]:
    result: dict[str, ArtifactSpec] = {}
    for p in sorted((root / "ontology" / "artefacts").glob("*.yaml")):
        raw = load_yaml(p)
        records = raw if isinstance(raw, list) else [raw]
        for item in records:
            spec = ArtifactSpec(
                id=item["id"],
                name=item["name"],
                purpose=item["purpose"],
                capability=item["capability"],
                requires=tuple(item.get("requires", [])),
                optional=bool(item.get("optional", False)),
                human_required=bool(item.get("human_required", False)),
                evidence_required=bool(item.get("evidence_required", False)),
                produced_by=item.get("produced_by"),
                required_sections=tuple(item.get("required_sections", [])),
            )
            result[spec.id] = spec
    return result


def load_archetypes(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for p in sorted((root / "ontology" / "archetypes").glob("*.yaml")):
        raw = load_yaml(p)
        out[raw["id"]] = raw
    return out


def load_contract(root: Path) -> dict[str, Any]:
    """Load the canonical artefact output contract."""
    return load_yaml(root / "ontology" / "artefact-contract.yaml")


def intake_from_dict(raw: dict[str, Any]) -> Intake:
    return Intake(
        id=str(raw["id"]),
        title=str(raw.get("title", raw["id"])),
        organisation=str(raw.get("organisation", "unknown")),
        segment=raw.get("segment"),
        domain=raw.get("domain"),
        problem=str(raw["problem"]),
        evidence_signal=raw.get("evidence_signal"),
        opportunity=raw.get("opportunity"),
        buyer=raw.get("buyer"),
        components=list(raw.get("components", [])),
        constraints=list(raw.get("constraints", [])),
        source_key=raw.get("source_key"),
        evidence_confidence=raw.get("evidence_confidence"),
        metadata=dict(raw.get("metadata", {})),
    )


def classify(intake: Intake, archetypes: dict[str, dict[str, Any]]) -> list[str]:
    hay = " ".join([
        intake.title, intake.problem, intake.opportunity or "", intake.domain or "",
        " ".join(intake.components), " ".join(intake.constraints)
    ]).lower()

    scores: list[tuple[int, str]] = []
    for aid, a in archetypes.items():
        score = 0
        for term in a.get("match_terms", []):
            pattern = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
            if re.search(pattern, hay):
                score += int(a.get("term_weight", 1))
        if a.get("always"):
            score += int(a.get("always_score", 1))
        if score:
            scores.append((score, aid))

    # General solutioning is always present; domain archetypes are additive.
    scores.append((1, "general-solution"))
    scores = sorted(set(scores), reverse=True)
    selected = [aid for score, aid in scores if score > 0]
    return selected


def seed_artifacts(archetype_ids: list[str], archetypes: dict[str, dict[str, Any]]) -> list[str]:
    """Artefacts named directly by the selected archetype manifests."""
    ids: list[str] = []
    for aid in archetype_ids:
        ids.extend(archetypes[aid].get("required_artifacts", []))
    return list(dict.fromkeys(ids))


def close_dependencies(
    seeds: Iterable[str], registry: dict[str, ArtifactSpec]
) -> tuple[list[str], list[str]]:
    """Expand a seed manifest to its transitive dependency closure.

    Archetype manifests declare intent ("this class of problem needs a threat
    model"). The dependency edges live in ontology/artefacts/core.yaml and are
    the single source of truth. Closing over them here means an archetype can
    never produce an unresolvable graph, and no archetype file has to restate a
    dependency that the registry already owns.

    Returns (closed_ids_in_seed_order_then_sorted, ids_added_by_closure).
    """
    selected: list[str] = []
    seen: set[str] = set()
    queue: deque[str] = deque()

    for s in seeds:
        if s not in registry:
            raise ValueError(f"Unknown artefact id in archetype manifest: {s!r}")
        if s not in seen:
            seen.add(s)
            selected.append(s)
            queue.append(s)

    added: list[str] = []
    while queue:
        node = queue.popleft()
        for req in registry[node].requires:
            if req not in registry:
                raise ValueError(
                    f"Artefact {node} requires unknown artefact id {req!r}"
                )
            if req not in seen:
                seen.add(req)
                selected.append(req)
                added.append(req)
                queue.append(req)

    return selected, sorted(added)


def topological_order(artifact_ids: Iterable[str], registry: dict[str, ArtifactSpec]) -> list[str]:
    """Kahn topological sort over the selected artefact set.

    Raises if a dependency is missing from the set (callers should pass a
    dependency-closed set) or if the graph contains a cycle.
    """
    selected = set(artifact_ids)
    indegree: dict[str, int] = {a: 0 for a in selected}
    dependents: dict[str, list[str]] = defaultdict(list)
    for aid in sorted(selected):
        missing = []
        for req in registry[aid].requires:
            if req in selected:
                indegree[aid] += 1
                dependents[req].append(aid)
            else:
                missing.append(req)
        if missing:
            raise ValueError(f"Artefact {aid} requires missing artefacts: {missing}")

    q = deque(sorted([a for a, d in indegree.items() if d == 0]))
    order: list[str] = []
    while q:
        node = q.popleft()
        order.append(node)
        for nxt in sorted(dependents[node]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    if len(order) != len(selected):
        raise ValueError("Artefact dependency graph contains a cycle")
    return order


def compute_frontier(
    artifact_ids: Iterable[str],
    registry: dict[str, ArtifactSpec],
    satisfied: Iterable[str] = (),
) -> list[str]:
    """Return the artefacts that are genuinely ready to be produced now.

    An artefact is on the frontier only when every artefact it `requires` is
    already satisfied and it is not itself satisfied. This is a real readiness
    predicate, not a slice of the topological order: two artefacts adjacent in
    the topological order are frequently NOT concurrently workable.
    """
    selected = set(artifact_ids)
    done = set(satisfied)
    unknown = done - selected
    if unknown:
        raise ValueError(f"Satisfied artefacts outside the selected set: {sorted(unknown)}")
    return sorted(
        aid for aid in selected
        if aid not in done and all(req in done for req in registry[aid].requires)
    )


def skill_for(aid: str, registry: dict[str, ArtifactSpec]) -> str | None:
    return registry[aid].skill


def split_by_binding(
    artifact_ids: Iterable[str], registry: dict[str, ArtifactSpec]
) -> tuple[list[str], list[str]]:
    """Split selected artefacts into (bound to a Skill, not bound)."""
    bound, unbound = [], []
    for aid in artifact_ids:
        (bound if registry[aid].produced_by else unbound).append(aid)
    return bound, unbound


def derive_mvp_sequence(
    order: list[str], registry: dict[str, ArtifactSpec]
) -> tuple[list[str], dict[str, list[str]]]:
    """Derive the currently-executable sequence from the ontology.

    The sequence is every selected artefact that has a Skill binding, in
    dependency order. `unsatisfied` records, per artefact, the registry-required
    upstream artefacts that no Skill can currently produce. This is derived, not
    documented: there is no second source of truth for the pipeline.
    """
    bound = [aid for aid in order if registry[aid].produced_by]
    bound_set = set(bound)
    unsatisfied: dict[str, list[str]] = {}
    for aid in bound:
        gaps = [r for r in registry[aid].requires if r not in bound_set]
        if gaps:
            unsatisfied[aid] = sorted(gaps)
    return bound, unsatisfied


def build_blueprint(root: Path, intake_path: str | Path) -> Blueprint:
    raw = load_yaml(intake_path)
    intake = intake_from_dict(raw)
    registry = load_registry(root)
    archetypes = load_archetypes(root)
    selected_archetypes = classify(intake, archetypes)

    seeds = seed_artifacts(selected_archetypes, archetypes)
    closed, added = close_dependencies(seeds, registry)
    order = topological_order(closed, registry)
    frontier = compute_frontier(order, registry)
    generatable, ungeneratable = split_by_binding(order, registry)
    mvp, mvp_unsatisfied = derive_mvp_sequence(order, registry)

    human = [registry[a].name for a in order if registry[a].human_required]
    assumptions = [
        f"Validate all material claims in {intake.title} against independent evidence.",
        "Confirm current-state system/data landscape with the accountable owner.",
        "Freeze acceptance criteria before detailed solution selection.",
    ]
    if intake.evidence_confidence and intake.evidence_confidence.lower() != "high":
        assumptions.append("Evidence confidence is not high; do not treat opportunity economics or architecture constraints as verified facts.")
    notes = [
        "This is an artefact plan, not a solution and not a commitment to build.",
        f"{len(generatable)} of {len(order)} planned artefacts have a Skill binding; "
        f"{len(ungeneratable)} have no producer and remain manual work.",
        "The kernel plans and sequences artefacts. It does not write them, does not "
        "call an LLM, and does not execute anything.",
    ]
    return Blueprint(
        intake=intake,
        archetypes=selected_archetypes,
        seeded_artifacts=seeds,
        artifacts=order,
        closure_added=added,
        frontier=frontier,
        generatable=generatable,
        ungeneratable=ungeneratable,
        mvp_sequence=mvp,
        mvp_unsatisfied=mvp_unsatisfied,
        human_decisions=human,
        assumptions_to_validate=assumptions,
        notes=notes,
    )


def write_outputs(bp: Blueprint, root: Path, out_dir: Path, registry: dict[str, ArtifactSpec] | None = None) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    registry = registry if registry is not None else load_registry(root)

    payload = {
        "version": "0.2",
        "intake": bp.intake.__dict__,
        "archetypes": bp.archetypes,
        "seeded_artifacts": bp.seeded_artifacts,
        "closure_added": bp.closure_added,
        "artifact_order": bp.artifacts,
        "frontier": bp.frontier,
        "generatable": bp.generatable,
        "ungeneratable": bp.ungeneratable,
        "mvp_sequence": bp.mvp_sequence,
        "mvp_unsatisfied_dependencies": bp.mvp_unsatisfied,
        "human_decisions": bp.human_decisions,
        "assumptions_to_validate": bp.assumptions_to_validate,
        "notes": bp.notes,
    }
    (out_dir / "plan.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        f"# Artefact Plan — {bp.intake.title}",
        "",
        f"**Intake:** `{bp.intake.id}`  ",
        f"**Organisation:** {bp.intake.organisation}  ",
        f"**Domain:** {bp.intake.domain or 'unspecified'}  ",
        f"**Opportunity:** {bp.intake.opportunity or 'not yet defined'}",
        "",
        "This document is a **plan for work**, not the work. It lists which artefacts",
        "are required, in what order, and which of them a Skill can currently produce.",
        "",
        "## Problem",
        bp.intake.problem,
        "",
        "## Selected archetypes",
        *[f"- `{a}`" for a in bp.archetypes],
        "",
        f"## Artefact plan ({len(bp.artifacts)} artefacts)",
        "",
        f"{len(bp.seeded_artifacts)} named directly by the archetype manifests; "
        f"{len(bp.closure_added)} pulled in by transitive dependency closure.",
        "",
        "| Order | Artefact | Capability | Producer | Human? | Evidence? |",
        "|---:|---|---|---|:---:|:---:|",
    ]
    for i, aid in enumerate(bp.artifacts, 1):
        a = registry[aid]
        producer = f"`{a.skill}`" if a.produced_by else "_no Skill — manual_"
        lines.append(
            f"| {i} | `{a.id}` — {a.name} | {a.capability} | {producer} | "
            f"{'Yes' if a.human_required else 'No'} | {'Yes' if a.evidence_required else 'No'} |"
        )

    lines += [
        "",
        "## Ready now (dependency-satisfied frontier)",
        "",
        "Every artefact below has all of its required upstream artefacts satisfied.",
        "Nothing else can start yet.",
        "",
        *[f"- `{a}` — {registry[a].name}" for a in bp.frontier],
        "",
        "## Currently executable sequence",
        "",
        f"{len(bp.mvp_sequence)} of {len(bp.artifacts)} planned artefacts have a Skill binding.",
        "This sequence is derived from the ontology, not documented separately.",
        "",
        *[f"{i}. `{a}` → skill `{registry[a].skill}`" for i, a in enumerate(bp.mvp_sequence, 1)],
        "",
        "### Upstream dependencies this sequence cannot satisfy",
        "",
    ]
    if bp.mvp_unsatisfied:
        lines.append("These artefacts have registry-required upstream inputs that no Skill can")
        lines.append("currently produce. The sequence is therefore incomplete by construction.")
        lines.append("")
        for aid, gaps in sorted(bp.mvp_unsatisfied.items()):
            lines.append(f"- `{aid}` is missing: {', '.join(f'`{g}`' for g in gaps)}")
    else:
        lines.append("- None.")

    lines += [
        "",
        f"### Artefacts with no producer ({len(bp.ungeneratable)})",
        "",
        "These are planned but cannot be generated today. They are manual work.",
        "",
        "  " + ", ".join(f"`{a}`" for a in bp.ungeneratable) if bp.ungeneratable else "- None.",
        "",
        "## Human decisions",
        *([f"- {x}" for x in bp.human_decisions] if bp.human_decisions else ["- None explicitly encoded in the current archetype set."]),
        "",
        "## Validation / assumptions",
        *[f"- {x}" for x in bp.assumptions_to_validate],
        "",
        "## Guardrails",
        *[f"- {x}" for x in bp.notes],
    ]
    (out_dir / "plan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
