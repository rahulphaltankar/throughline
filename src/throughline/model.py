from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ArtifactSpec:
    id: str
    name: str
    purpose: str
    capability: str
    requires: tuple[str, ...] = ()
    optional: bool = False
    human_required: bool = False
    evidence_required: bool = False


@dataclass
class Intake:
    id: str
    title: str
    organisation: str
    segment: str | None
    domain: str | None
    problem: str
    evidence_signal: str | None = None
    opportunity: str | None = None
    buyer: str | None = None
    components: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    source_key: str | None = None
    evidence_confidence: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Blueprint:
    intake: Intake
    archetypes: list[str]
    artifacts: list[str]
    frontier: list[str]
    human_decisions: list[str]
    assumptions_to_validate: list[str]
    notes: list[str]
