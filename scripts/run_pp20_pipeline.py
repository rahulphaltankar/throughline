#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
ARTEFACTS = [
 ("problem-frame", "examples/pp20/artefacts/problem-frame.md"),
 ("evidence-brief", "examples/pp20/artefacts/evidence-brief.md"),
 ("current-state-assessment", "examples/pp20/artefacts/current-state-assessment.md"),
 ("requirements", "examples/pp20/artefacts/requirements.md"),
 ("solution-options", "examples/pp20/artefacts/solution-options.md"),
 ("solution-recommendation", "examples/pp20/artefacts/solution-recommendation.md"),
]
for typ, path in ARTEFACTS:
    r=subprocess.run([sys.executable, str(ROOT/'scripts/gates/validate_artifact.py'), typ, str(ROOT/path)], text=True)
    if r.returncode:
        raise SystemExit(r.returncode)
print(f"PP20 benchmark pipeline: PASS ({len(ARTEFACTS)} artefact gates)")
