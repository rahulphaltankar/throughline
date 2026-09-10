#!/usr/bin/env python3
"""Exhaustive ontology validation.

Checks, for every archetype in ontology/archetypes/:

  1. every artefact it names exists in the registry;
  2. the archetype (alone, and combined with the always-on general baseline)
     produces a dependency-closed, acyclic, resolvable graph;
  3. the resulting frontier is non-empty and genuinely dependency-ready.

Also checks registry-wide invariants:

  4. every `requires` edge points at a real artefact;
  5. every `produced_by` binding resolves to a real .claude/skills/<dir>/SKILL.md;
  6. the registry graph as a whole is acyclic.

Exit codes: 0 pass, 1 fail.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from throughline.engine import (  # noqa: E402
    close_dependencies,
    compute_frontier,
    load_archetypes,
    load_registry,
    seed_artifacts,
    topological_order,
)

BASELINE = "general-solution"


def main() -> int:
    registry = load_registry(ROOT)
    archetypes = load_archetypes(ROOT)
    failures: list[str] = []

    print(f"Registry: {len(registry)} artefact types")
    print(f"Archetypes: {len(archetypes)}")
    print()

    # --- registry invariants ------------------------------------------------
    for aid, spec in sorted(registry.items()):
        for req in spec.requires:
            if req not in registry:
                failures.append(f"registry: {aid} requires unknown artefact {req!r}")
        if spec.produced_by:
            skill_md = ROOT / ".claude" / "skills" / spec.skill / "SKILL.md"
            if not skill_md.is_file():
                failures.append(
                    f"registry: {aid} produced_by {spec.produced_by!r} does not resolve "
                    f"to {skill_md}"
                )
    try:
        topological_order(registry.keys(), registry)
    except ValueError as exc:
        failures.append(f"registry: whole-graph sort failed: {exc}")

    # --- per-archetype resolution ------------------------------------------
    print(f"{'archetype':22s} {'artefacts':>9s} {'closure':>8s}  frontier")
    print("-" * 70)
    for aid in sorted(archetypes):
        combo = [aid] if aid == BASELINE else [aid, BASELINE]
        try:
            for artefact in archetypes[aid].get("required_artifacts", []):
                if artefact not in registry:
                    raise ValueError(f"names unknown artefact {artefact!r}")
            seeds = seed_artifacts(combo, archetypes)
            closed, added = close_dependencies(seeds, registry)
            order = topological_order(closed, registry)
            frontier = compute_frontier(order, registry)
            if not frontier:
                raise ValueError("frontier is empty; nothing can start")
            for f in frontier:
                if registry[f].requires:
                    raise ValueError(
                        f"frontier member {f} has unmet requires {list(registry[f].requires)}"
                    )
            print(f"{aid:22s} {len(order):9d} {'+' + str(len(added)):>8s}  "
                  f"{', '.join(frontier)}")
        except ValueError as exc:
            failures.append(f"archetype {aid}: {exc}")
            print(f"{aid:22s} {'FAIL':>9s}           {exc}")

    print()
    unreachable = sorted(
        set(registry)
        - {a for arch in archetypes.values() for a in arch.get("required_artifacts", [])}
    )
    # Closure can still pull these in, so report rather than fail.
    if unreachable:
        print(f"Note: {len(unreachable)} artefacts are named by no archetype manifest: "
              f"{', '.join(unreachable)}")
        print()

    if failures:
        print(f"ONTOLOGY VALIDATION: FAIL ({len(failures)} problems)")
        for f in failures:
            print("  -", f)
        return 1
    print(f"ONTOLOGY VALIDATION: PASS (all {len(archetypes)} archetypes resolve)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
