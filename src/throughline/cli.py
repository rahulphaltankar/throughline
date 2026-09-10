from __future__ import annotations

import argparse
from pathlib import Path

from .engine import build_blueprint, load_registry, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(prog="tl", description="Throughline artefact-plan compiler")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan", help="Compile an intake into an artefact plan")
    p.add_argument("intake")
    p.add_argument("--out", default="blueprint")
    args = parser.parse_args()

    if args.command == "plan":
        root = Path(__file__).resolve().parents[2]
        bp = build_blueprint(root, args.intake)
        registry = load_registry(root)
        out_dir = Path(args.out)
        write_outputs(bp, root, out_dir, registry=registry)
        print(f"Generated artefact plan: {out_dir}")
        print(f"Archetypes: {', '.join(bp.archetypes)}")
        print(f"Artefacts planned: {len(bp.artifacts)} "
              f"({len(bp.seeded_artifacts)} seeded, {len(bp.closure_added)} added by closure)")
        print(f"Ready now (frontier): {', '.join(bp.frontier)}")
        print(f"Skill-bound: {len(bp.generatable)}  |  no producer: {len(bp.ungeneratable)}")
        if bp.mvp_unsatisfied:
            print("Unsatisfiable upstream inputs in the executable sequence:")
            for aid, gaps in sorted(bp.mvp_unsatisfied.items()):
                print(f"  {aid} <- {', '.join(gaps)}")


if __name__ == "__main__":
    main()
