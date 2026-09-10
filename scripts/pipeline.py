"""Provider-independent execution layer for Throughline artefact plans.

This module intentionally lives outside ``src/throughline``.  The kernel owns
planning; this layer owns persisted work orders, producer invocation and gate
admission.  It contains no LLM client or provider-specific code.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
import json
import shutil

from throughline.engine import (
    build_blueprint,
    compute_frontier,
    load_contract,
    load_registry,
)


STATUSES = {"READY", "RUNNING", "ACCEPTED", "REJECTED", "BLOCKED", "FAILED"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class UpstreamArtifact:
    id: str
    type: str
    path: str


@dataclass(frozen=True)
class ProducerRequest:
    """The complete, provider-neutral work order sent to a producer."""

    target_type: str
    target_id: str
    skill_path: str
    upstream_artifacts: tuple[UpstreamArtifact, ...]
    intake_path: str
    output_path: str
    contract: dict[str, Any]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ProducerResult:
    success: bool
    message: str = ""
    details: dict[str, Any] | None = None


class ProducerAdapter(Protocol):
    """A provider adapter writes exactly the requested output, or fails."""

    name: str

    def produce(self, request: ProducerRequest) -> ProducerResult: ...


class FixtureProducer:
    """Local test adapter that copies controlled fixture artefacts.

    It proves execution mechanics only.  It never synthesizes content and is
    deliberately unsuitable for real project work.
    """

    name = "local-fixture"

    def __init__(self, fixture_root: Path):
        self.fixture_root = fixture_root

    def produce(self, request: ProducerRequest) -> ProducerResult:
        source = self.fixture_root / f"{request.target_type}.md"
        if not source.is_file():
            return ProducerResult(False, "fixture not found", {"fixture": str(source)})
        destination = Path(request.output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        return ProducerResult(True, "copied controlled fixture", {"fixture": str(source)})


class PipelineRunner:
    """Persisted, resumable executor for Skill-bound, frontier-ready artefacts."""

    def __init__(
        self,
        root: Path,
        intake_path: Path,
        out_dir: Path,
        producer: ProducerAdapter,
    ):
        self.root = root.resolve()
        self.intake_path = intake_path.resolve()
        self.out_dir = out_dir.resolve()
        self.producer = producer
        self.registry = load_registry(self.root)
        self.contract = load_contract(self.root)
        self.blueprint = build_blueprint(self.root, self.intake_path)
        self.state_path = self.out_dir / "run.json"

    def _relative_or_absolute(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def _new_state(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "run_id": self.out_dir.name,
            "project": self._relative_or_absolute(self.intake_path),
            "status": "READY",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "artifacts": {},
            "attempts": [],
            "blockers": [],
        }

    def load_state(self) -> dict[str, Any]:
        if not self.state_path.is_file():
            return self._new_state()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        if state.get("schema_version") != 1:
            raise ValueError("unsupported run manifest schema_version")
        if state.get("project") != self._relative_or_absolute(self.intake_path):
            raise ValueError("run manifest belongs to a different intake")
        return state

    def save_state(self, state: dict[str, Any]) -> None:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        state["updated_at"] = utc_now()
        self.state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def _accepted_types(state: dict[str, Any]) -> list[str]:
        return sorted(
            artifact_type
            for artifact_type, record in state["artifacts"].items()
            if record.get("status") == "ACCEPTED"
        )

    def _target_id(self, artifact_type: str) -> str:
        try:
            import yaml
            raw = yaml.safe_load(self.intake_path.read_text(encoding="utf-8"))
            project_id = str(raw["id"])
        except Exception as exc:  # kernel has already validated enough to plan
            raise ValueError(f"could not read intake id: {exc}") from exc
        index = self.blueprint.artifacts.index(artifact_type) + 1
        return f"{project_id}-A{index:02d}"

    def _resolve_inputs(
        self, target: str, state: dict[str, Any]
    ) -> tuple[list[UpstreamArtifact], list[dict[str, str]]]:
        inputs: list[UpstreamArtifact] = []
        missing: list[dict[str, str]] = []
        for upstream_type in self.registry[target].requires:
            record = state["artifacts"].get(upstream_type)
            if not record or record.get("status") != "ACCEPTED":
                missing.append({"type": upstream_type, "reason": "not accepted"})
                continue
            path = Path(record["output"])
            if not path.is_file():
                missing.append({"type": upstream_type, "reason": "accepted output is missing"})
                continue
            inputs.append(UpstreamArtifact(record["id"], upstream_type, str(path)))
        return inputs, missing

    def _gate(self, output: Path, target: str) -> list[str]:
        # Import the real gate rather than recreating its semantics here.
        import importlib.util

        gate_path = self.root / "scripts" / "gates" / "validate_artifact.py"
        spec = importlib.util.spec_from_file_location("throughline_tier0_gate", gate_path)
        if not spec or not spec.loader:
            raise RuntimeError("could not load Tier-0 gate")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.validate(output, target)

    def _block(self, state: dict[str, Any], blockers: list[dict[str, Any]]) -> None:
        state["status"] = "BLOCKED"
        state["blockers"] = blockers
        self.save_state(state)

    def run(self, max_attempts: int = 100) -> dict[str, Any]:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        state = self.load_state()
        state["status"] = "RUNNING"
        state["blockers"] = []
        self.save_state(state)

        attempts_this_run = 0
        while attempts_this_run < max_attempts:
            accepted = self._accepted_types(state)
            frontier = compute_frontier(self.blueprint.artifacts, self.registry, accepted)
            if not frontier:
                state["status"] = "ACCEPTED"
                self.save_state(state)
                return state

            ready_bound = [a for a in self.blueprint.artifacts if a in frontier and self.registry[a].produced_by]
            if not ready_bound:
                blockers = [
                    {"type": a, "reason": "ready but has no Skill binding"}
                    for a in frontier
                ]
                self._block(state, blockers)
                return state

            target = ready_bound[0]
            skill = self.registry[target].skill
            assert skill is not None
            skill_path = self.root / ".claude" / "skills" / skill / "SKILL.md"
            if not skill_path.is_file():
                state["status"] = "FAILED"
                state["blockers"] = [{"type": target, "reason": "bound Skill path is missing"}]
                self.save_state(state)
                return state

            upstream, missing = self._resolve_inputs(target, state)
            if missing:
                self._block(state, [{"type": target, "reason": "missing required inputs", "inputs": missing}])
                return state

            attempt_number = len(state["attempts"]) + 1
            target_id = self._target_id(target)
            output = self.out_dir / "artefacts" / f"{target}.md"
            started = utc_now()
            request = ProducerRequest(
                target_type=target,
                target_id=target_id,
                skill_path=str(skill_path),
                upstream_artifacts=tuple(upstream),
                intake_path=str(self.intake_path),
                output_path=str(output),
                contract=self.contract,
                metadata={
                    "run_id": state["run_id"],
                    "attempt_number": attempt_number,
                    "project": state["project"],
                },
            )
            state["artifacts"][target] = {"id": target_id, "status": "RUNNING", "output": str(output)}
            self.save_state(state)
            result = self.producer.produce(request)

            manifest: dict[str, Any] = {
                "run_id": state["run_id"],
                "project": state["project"],
                "target": {"id": target_id, "type": target},
                "producer": self.producer.name,
                "skill_path": str(skill_path),
                "inputs": [asdict(item) for item in upstream],
                "output": str(output),
                "attempt_number": attempt_number,
                "started_at": started,
                "finished_at": utc_now(),
                "status": "FAILED",
                "gate_result": {"passed": False, "failures": []},
                "producer_result": asdict(result),
            }
            attempts_this_run += 1

            if not result.success or not output.is_file():
                message = result.message or "producer did not write requested output"
                state["artifacts"][target].update({"status": "FAILED", "message": message})
                manifest["message"] = message
                state["attempts"].append(manifest)
                state["status"] = "FAILED"
                self.save_state(state)
                return state

            failures = self._gate(output, target)
            manifest["gate_result"] = {"passed": not failures, "failures": failures}
            if failures:
                state["artifacts"][target].update({"status": "REJECTED", "gate_failures": failures})
                manifest["status"] = "REJECTED"
                state["attempts"].append(manifest)
                state["status"] = "REJECTED"
                self.save_state(state)
                return state

            state["artifacts"][target].update({"status": "ACCEPTED", "accepted_at": utc_now()})
            manifest["status"] = "ACCEPTED"
            manifest["gate_result"] = {"passed": True, "failures": []}
            state["attempts"].append(manifest)
            self.save_state(state)

        self._block(state, [{"reason": "attempt limit reached", "limit": max_attempts}])
        return state
