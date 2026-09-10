from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from typing import Any
import json
import re
import yaml

from .model import ArtifactSpec, Blueprint, Intake


def load_yaml(path: str | Path) -> dict[str, Any]:
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
            )
            result[spec.id] = spec
    return result


def load_archetypes(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for p in sorted((root / "ontology" / "archetypes").glob("*.yaml")):
        raw = load_yaml(p)
        out[raw["id"]] = raw
    return out


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


def compose_artifacts(archetype_ids: list[str], archetypes: dict[str, dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for aid in archetype_ids:
        ids.extend(archetypes[aid].get("required_artifacts", []))
    # preserve order, de-duplicate
    return list(dict.fromkeys(ids))


def resolve_frontier(artifact_ids: list[str], registry: dict[str, ArtifactSpec]) -> list[str]:
    selected = set(artifact_ids)
    indegree: dict[str, int] = {a: 0 for a in selected}
    dependents: dict[str, list[str]] = defaultdict(list)
    for aid in selected:
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


def build_blueprint(root: Path, intake_path: str | Path) -> Blueprint:
    raw = load_yaml(intake_path)
    intake = intake_from_dict(raw)
    registry = load_registry(root)
    archetypes = load_archetypes(root)
    selected_archetypes = classify(intake, archetypes)
    artifacts = compose_artifacts(selected_archetypes, archetypes)
    order = resolve_frontier(artifacts, registry)
    human = [registry[a].name for a in order if registry[a].human_required]
    assumptions = [
        f"Validate all material claims in {intake.title} against independent evidence.",
        "Confirm current-state system/data landscape with the accountable owner.",
        "Freeze acceptance criteria before detailed solution selection.",
    ]
    if intake.evidence_confidence and intake.evidence_confidence.lower() != "high":
        assumptions.append("Evidence confidence is not high; do not treat opportunity economics or architecture constraints as verified facts.")
    notes = [
        "This is a first-pass solution blueprint, not a commitment to build.",
        "Architecture and technology selections remain hypotheses until constraints and evidence are validated.",
        "The PMO artefacts generated here are planning inputs; estimates must carry ranges and confidence.",
    ]
    return Blueprint(
        intake=intake,
        archetypes=selected_archetypes,
        artifacts=order,
        frontier=order[: min(6, len(order))],
        human_decisions=human,
        assumptions_to_validate=assumptions,
        notes=notes,
    )


def write_outputs(bp: Blueprint, root: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "0.1",
        "intake": bp.intake.__dict__,
        "archetypes": bp.archetypes,
        "artifact_order": bp.artifacts,
        "frontier": bp.frontier,
        "human_decisions": bp.human_decisions,
        "assumptions_to_validate": bp.assumptions_to_validate,
        "notes": bp.notes,
    }
    (out_dir / "plan.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    registry = load_registry(root)
    lines = [
        f"# Solution Blueprint — {bp.intake.title}",
        "",
        f"**Intake:** `{bp.intake.id}`  ",
        f"**Organisation:** {bp.intake.organisation}  ",
        f"**Domain:** {bp.intake.domain or 'unspecified'}  ",
        f"**Opportunity:** {bp.intake.opportunity or 'not yet defined'}",
        "",
        "## Problem",
        bp.intake.problem,
        "",
        "## Selected archetypes",
        *[f"- `{a}`" for a in bp.archetypes],
        "",
        "## Artefact plan",
        "| Order | Artefact | Capability | Purpose | Human? | Evidence? |",
        "|---:|---|---|---|:---:|:---:|",
    ]
    for i, aid in enumerate(bp.artifacts, 1):
        a = registry[aid]
        lines.append(f"| {i} | `{a.id}` — {a.name} | {a.capability} | {a.purpose} | {'Yes' if a.human_required else 'No'} | {'Yes' if a.evidence_required else 'No'} |")
    lines += [
        "",
        "## Immediate frontier",
        *[f"- Produce `{a}`" for a in bp.frontier],
        "",
        "## Human decisions",
        *( [f"- {x}" for x in bp.human_decisions] if bp.human_decisions else ["- None explicitly encoded in the current archetype set."] ),
        "",
        "## Validation / assumptions",
        *[f"- {x}" for x in bp.assumptions_to_validate],
        "",
        "## Guardrails",
        *[f"- {x}" for x in bp.notes],
    ]
    (out_dir / "plan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
