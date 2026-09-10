#!/usr/bin/env python3
"""Tier-0 deterministic gate for Throughline markdown artefacts.

The gate validates STRUCTURE, not quality. It parses YAML frontmatter and
checks it against two ontology files, which are the single sources of truth:

  ontology/artefact-contract.yaml  -- required frontmatter fields and enums
  ontology/artefacts/core.yaml     -- known types, `requires` edges,
                                      evidence_required, human_required,
                                      required_sections, produced_by

It has no hardcoded artefact knowledge of its own. An unknown artefact type is
rejected rather than silently passed. Heading checks are a secondary,
line-anchored check driven by the registry -- never the primary mechanism.

Usage:
    validate_artifact.py <file>                 # type read from frontmatter
    validate_artifact.py <expected-type> <file> # also assert the type matches
Exit codes: 0 pass, 1 fail, 2 usage error.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------
# Ontology loading
# --------------------------------------------------------------------------

def load_contract() -> dict[str, Any]:
    with open(ROOT / "ontology" / "artefact-contract.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_registry() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for p in sorted((ROOT / "ontology" / "artefacts").glob("*.yaml")):
        with open(p, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or []
        for item in (raw if isinstance(raw, list) else [raw]):
            registry[item["id"]] = item
    return registry


# --------------------------------------------------------------------------
# Frontmatter parsing
# --------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body). Raises ValueError on malformed input."""
    if not text.startswith("---\n"):
        raise ValueError("file does not begin with a '---' frontmatter block")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ValueError("frontmatter block is not terminated by '---'")
    raw = text[4:end + 1]
    body = text[end + 5:]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValueError(f"frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, body


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def _check_item_list(
    fm: dict[str, Any], field: str, required_keys: list[str], failures: list[str]
) -> list[dict[str, Any]]:
    """Validate that `field` is a list of mappings carrying `required_keys`."""
    value = fm.get(field)
    if value is None:
        value = []
    if not isinstance(value, list):
        failures.append(f"`{field}` must be a list, got {type(value).__name__}")
        return []
    items: list[dict[str, Any]] = []
    for n, item in enumerate(value, 1):
        if not isinstance(item, dict):
            failures.append(f"`{field}[{n}]` must be a mapping, got {type(item).__name__}")
            continue
        missing = [k for k in required_keys if k not in item or item[k] in (None, "")]
        if missing:
            failures.append(f"`{field}[{n}]` is missing: {', '.join(missing)}")
        items.append(item)
    return items


def validate(path: Path, expected_type: str | None = None) -> list[str]:
    """Return a list of failure strings. Empty list means the artefact passes."""
    contract = load_contract()
    registry = load_registry()
    failures: list[str] = []

    if not path.is_file():
        return [f"file not found: {path}"]

    text = path.read_text(encoding="utf-8")

    # --- structural: frontmatter must parse -------------------------------
    try:
        fm, body = split_frontmatter(text)
    except ValueError as exc:
        return [f"malformed artefact: {exc}"]

    # --- contract: required fields present --------------------------------
    for field in contract["required_fields"]:
        if field not in fm:
            failures.append(f"missing required frontmatter field: `{field}`")

    known_fields = set(contract["required_fields"]) | set(contract.get("optional_fields", []))
    for field in fm:
        if field not in known_fields:
            failures.append(f"unknown frontmatter field: `{field}`")

    # --- type must be known -----------------------------------------------
    atype = fm.get("type")
    if not atype:
        failures.append("frontmatter `type` is missing or empty")
        return failures
    if atype not in registry:
        failures.append(
            f"unknown artefact type: `{atype}` is not defined in ontology/artefacts/core.yaml"
        )
        return failures
    if expected_type is not None and atype != expected_type:
        failures.append(f"type mismatch: expected `{expected_type}`, frontmatter says `{atype}`")

    spec = registry[atype]

    # --- schema version ----------------------------------------------------
    if fm.get("schema_version") != contract["schema_version"]:
        failures.append(
            f"schema_version must be {contract['schema_version']}, got {fm.get('schema_version')!r}"
        )

    # --- status enum -------------------------------------------------------
    if fm.get("status") not in contract["statuses"]:
        failures.append(
            f"status `{fm.get('status')}` is not one of {contract['statuses']}"
        )

    # --- id ----------------------------------------------------------------
    if not isinstance(fm.get("id"), str) or not fm.get("id", "").strip():
        failures.append("`id` must be a non-empty string")

    # --- produced_by must resolve to a real Skill --------------------------
    produced_by = fm.get("produced_by")
    if not isinstance(produced_by, str) or not produced_by.startswith("skill:"):
        failures.append(f"`produced_by` must be 'skill:<dir>', got {produced_by!r}")
    else:
        skill_dir = produced_by[len("skill:"):]
        skill_md = ROOT / ".claude" / "skills" / skill_dir / "SKILL.md"
        if not skill_md.is_file():
            failures.append(f"`produced_by` does not resolve: {skill_md} does not exist")
        registry_producer = spec.get("produced_by")
        if registry_producer and registry_producer != produced_by:
            failures.append(
                f"`produced_by` is {produced_by!r} but the registry binds "
                f"`{atype}` to {registry_producer!r}"
            )

    # --- inputs must cover the registry `requires` edges -------------------
    intake_type = contract["intake_input_type"]
    inputs = _check_item_list(fm, "inputs", contract["item_fields"]["inputs"], failures)
    unsat = _check_item_list(
        fm, "unsatisfied_inputs", contract["item_fields"]["unsatisfied_inputs"], failures
    )

    input_types: set[str] = set()
    for item in inputs:
        t = item.get("type")
        if t == intake_type:
            continue
        if t not in registry:
            failures.append(f"`inputs` references unknown artefact type: `{t}`")
        else:
            input_types.add(t)

    unsat_types: set[str] = set()
    for item in unsat:
        t = item.get("type")
        if t not in registry:
            failures.append(f"`unsatisfied_inputs` references unknown artefact type: `{t}`")
        else:
            unsat_types.add(t)

    required = set(spec.get("requires", []))
    uncovered = sorted(required - input_types - unsat_types)
    if uncovered:
        failures.append(
            "required upstream artefacts are neither supplied in `inputs` nor "
            f"declared in `unsatisfied_inputs`: {', '.join(uncovered)}"
        )
    bogus = sorted(unsat_types - required)
    if bogus:
        failures.append(
            f"`unsatisfied_inputs` declares types that `{atype}` does not require: "
            f"{', '.join(bogus)}"
        )
    both = sorted(unsat_types & input_types)
    if both:
        failures.append(
            f"types appear in both `inputs` and `unsatisfied_inputs`: {', '.join(both)}"
        )

    # --- evidence structure ------------------------------------------------
    evidence = _check_item_list(fm, "evidence", contract["item_fields"]["evidence"], failures)
    for n, item in enumerate(evidence, 1):
        cls = item.get("class")
        if cls is not None and cls not in contract["evidence_classes"]:
            failures.append(
                f"`evidence[{n}].class` is `{cls}`, not one of {contract['evidence_classes']}"
            )
        conf = item.get("confidence")
        if conf is not None and conf not in contract["confidence_levels"]:
            failures.append(
                f"`evidence[{n}].confidence` is `{conf}`, not one of {contract['confidence_levels']}"
            )
    if spec.get("evidence_required") and not evidence:
        failures.append(
            f"`{atype}` is evidence_required in the registry but carries no `evidence` entries"
        )

    # --- assumptions / open questions --------------------------------------
    _check_item_list(fm, "assumptions", contract["item_fields"]["assumptions"], failures)
    _check_item_list(fm, "open_questions", contract["item_fields"]["open_questions"], failures)

    # --- human review ------------------------------------------------------
    review = fm.get("review_required")
    if not isinstance(review, bool):
        failures.append(f"`review_required` must be a boolean, got {review!r}")
    elif spec.get("human_required") and review is not True:
        failures.append(
            f"`{atype}` is human_required in the registry, so `review_required` must be true"
        )

    # --- secondary: registry-declared section headings, line-anchored ------
    # Matching is whole-line, never substring: "## Evidence" must not be
    # satisfied by "## Evidence gaps". A registry entry may opt into prefix
    # matching with a trailing "*" (e.g. "## Option A*" matches
    # "## Option A - Lakehouse"), which stays explicit rather than global.
    body_lines = [line.rstrip() for line in body.splitlines()]
    missing_sections = []
    for required in spec.get("required_sections", []):
        if required.endswith("*"):
            stem = required[:-1].rstrip()
            found = any(line == stem or line.startswith(stem + " ") for line in body_lines)
        else:
            found = required in body_lines
        if not found:
            missing_sections.append(required)
    if missing_sections:
        failures.append("missing required sections: " + ", ".join(missing_sections))

    if not body.strip():
        failures.append("artefact body is empty")

    return failures


def main() -> int:
    args = sys.argv[1:]
    if len(args) == 1:
        expected, path = None, Path(args[0])
    elif len(args) == 2:
        expected, path = args[0], Path(args[1])
    else:
        print(__doc__)
        return 2

    failures = validate(path, expected)
    label = expected or "artefact"
    if failures:
        print(f"FAIL: {label} — {path}")
        for f in failures:
            print("  -", f)
        return 1
    print(f"PASS: {label} — {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
