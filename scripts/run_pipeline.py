#!/usr/bin/env python3
"""Execute the Skill-bound frontier using a provider-independent adapter.

The only adapter supplied here is ``local-fixture``.  It copies controlled test
fixtures and exists solely to exercise runner mechanics; it does not generate
content and does not call an external model.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pipeline import FixtureProducer, PipelineRunner  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Throughline's local test execution layer")
    parser.add_argument("intake", help="project intake YAML")
    parser.add_argument("--out", help="run directory (default: runs/<intake-stem>)")
    parser.add_argument("--max-attempts", type=int, default=100)
    parser.add_argument(
        "--fixture-root",
        default=str(ROOT / "tests" / "fixtures" / "pp20" / "artefacts"),
        help="controlled fixture directory for the local-fixture adapter",
    )
    args = parser.parse_args()
    intake = Path(args.intake)
    out = Path(args.out) if args.out else ROOT / "runs" / intake.stem
    runner = PipelineRunner(ROOT, intake, out, FixtureProducer(Path(args.fixture_root)))
    state = runner.run(args.max_attempts)
    print(f"Run {state['run_id']}: {state['status']}")
    print(f"Accepted: {', '.join(runner._accepted_types(state)) or 'none'}")
    if state["blockers"]:
        print("Blockers:")
        for blocker in state["blockers"]:
            print(f"  - {blocker}")
    return 1 if state["status"] in {"FAILED", "REJECTED"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
