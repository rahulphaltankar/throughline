from __future__ import annotations

import argparse
from pathlib import Path

from .engine import build_blueprint, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(prog="tl", description="Throughline blueprint compiler")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan", help="Compile an intake into a solution blueprint skeleton")
    p.add_argument("intake")
    p.add_argument("--out", default="blueprint")
    args = parser.parse_args()

    if args.command == "plan":
        root = Path(__file__).resolve().parents[2]
        bp = build_blueprint(root, args.intake)
        out_dir = Path(args.out)
        write_outputs(bp, root, out_dir)
        print(f"Generated blueprint: {out_dir}")
        print(f"Archetypes: {', '.join(bp.archetypes)}")
        print(f"Artefacts: {len(bp.artifacts)}")

if __name__ == "__main__":
    main()
