#!/usr/bin/env python3
"""Deterministic gate for Throughline markdown artefacts."""
from __future__ import annotations
import re, sys
from pathlib import Path

REQUIRED_SECTIONS = {
  "problem-frame": ["## Problem", "## Evidence", "## Hypotheses", "## Falsification questions"],
  "evidence-brief": ["## Claim ledger", "## Supporting evidence", "## Evidence gaps"],
  "current-state-assessment": ["## Current business process", "## Current systems landscape", "## Current data landscape", "## Validation questions"],
  "requirements": ["## Business requirements", "## Functional requirements", "## Non-functional requirements", "## Verification"],
  "solution-options": ["## Evaluation criteria", "## Option A", "## Option B", "## Comparison matrix"],
  "solution-recommendation": ["## Executive recommendation", "## Recommended solution", "## Architecture", "## Delivery plan", "## Budget", "## Operating model", "## Human decisions required"],
}

def main() -> int:
    if len(sys.argv) != 3:
        print("usage: validate_artifact.py <type> <file>")
        return 2
    typ, path = sys.argv[1], Path(sys.argv[2])
    text = path.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SECTIONS.get(typ, []) if s not in text]
    evidence_tags = re.findall(r"\b(observed|cited|derived|assumed)\b", text, flags=re.I)
    failures=[]
    if missing: failures.append("missing sections: " + ", ".join(missing))
    if not evidence_tags: failures.append("no evidence-class tags found")
    if typ == "problem-frame" and "falsification" not in text.lower(): failures.append("no falsification material")
    if failures:
        print("FAIL")
        for f in failures: print("-", f)
        return 1
    print(f"PASS: {typ}")
    print(f"evidence-class tags: {len(evidence_tags)}")
    return 0

if __name__ == "__main__": raise SystemExit(main())
