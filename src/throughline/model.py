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
    produced_by: str | None = None
    required_sections: tuple[str, ...] = ()

    @property
    def skill(self) -> str | None:
        """Skill directory name bound to this artefact, or None if unbound."""
        if not self.produced_by:
            return None
        prefix = "skill:"
        if not self.produced_by.startswith(prefix):
            raise ValueError(
                f"Artefact {self.id} has malformed produced_by {self.produced_by!r}; "
                f"expected '{prefix}<skill-directory>'"
            )
        return self.produced_by[len(prefix):]


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
    seeded_artifacts: list[str]
    artifacts: list[str]
    closure_added: list[str]
    frontier: list[str]
    generatable: list[str]
    ungeneratable: list[str]
    mvp_sequence: list[str]
    mvp_unsatisfied: dict[str, list[str]]
    human_decisions: list[str]
    assumptions_to_validate: list[str]
    notes: list[str]
