#!/usr/bin/env python3
"""Run the artefact gate over the PP20 benchmark fixtures.

The sequence is DERIVED from the ontology, not listed here. The kernel plans
PP20, works out which planned artefacts have a Skill binding, and orders them by
dependency. This script then gates the corresponding fixture for each one.

There is deliberately no second source of truth for the pipeline order: change
`produced_by` or `requires` in ontology/artefacts/core.yaml and this script
follows automatically.

The fixtures under tests/fixtures/pp20/ are TEST DATA. They are hand-written
reference artefacts used to exercise the gate. Nothing in this repository
generates them, and they must never be treated as system output.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from throughline.engine import build_blueprint, load_registry  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "pp20" / "artefacts"
GATE = ROOT / "scripts" / "gates" / "validate_artifact.py"


def main() -> int:
    registry = load_registry(ROOT)
    bp = build_blueprint(ROOT, ROOT / "projects" / "pp20" / "problem.yaml")

    print(f"PP20 plans {len(bp.artifacts)} artefacts across archetypes: "
          f"{', '.join(bp.archetypes)}")
    print(f"Skill-bound and therefore gateable: {len(bp.mvp_sequence)}")
    print()

    failures = 0
    checked = 0
    for aid in bp.mvp_sequence:
        path = FIXTURES / f"{aid}.md"
        if not path.is_file():
            print(f"MISSING FIXTURE: {aid} -> {path}")
            failures += 1
            continue
        result = subprocess.run(
            [sys.executable, str(GATE), aid, str(path)], text=True
        )
        checked += 1
        if result.returncode:
            failures += 1

    print()
    if bp.mvp_unsatisfied:
        print("DEPENDENCY DEFICIT — this sequence is incomplete by construction.")
        print("These artefacts have registry-required upstream inputs that no Skill")
        print("can currently produce:")
        for aid, gaps in sorted(bp.mvp_unsatisfied.items()):
            print(f"  {aid} <- {', '.join(gaps)}")
        print()

    ungenerated = len(bp.artifacts) - len(bp.mvp_sequence)
    print(f"{ungenerated} of {len(bp.artifacts)} planned PP20 artefacts have no producer "
          f"and are not covered by these fixtures.")
    print("The bound artefact slice is an MVP slice, not the PP20 solution.")
    print()

    if failures:
        print(f"PP20 benchmark pipeline: FAIL ({failures} of {len(bp.mvp_sequence)} gates failed)")
        return 1
    print(f"PP20 benchmark pipeline: PASS ({checked} artefact gates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
