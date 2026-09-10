"""Regression tests for the provider-independent execution layer."""
from __future__ import annotations

import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from pipeline import FixtureProducer, PipelineRunner, ProducerResult  # noqa: E402


FIXTURES = ROOT / "tests" / "fixtures" / "pp20" / "artefacts"
INTAKE = ROOT / "projects" / "pp20" / "problem.yaml"


class RecordingFixtureProducer(FixtureProducer):
    name = "recording-local-fixture"

    def __init__(self) -> None:
        super().__init__(FIXTURES)
        self.requests = []

    def produce(self, request):
        self.requests.append(request)
        return super().produce(request)


class InvalidProducer:
    name = "invalid-local"

    def produce(self, request):
        output = Path(request.output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# deliberately invalid\n", encoding="utf-8")
        return ProducerResult(True, "wrote invalid controlled output")


def make_runner(tmp_path, producer):
    return PipelineRunner(ROOT, INTAKE, tmp_path / "run", producer)


def test_only_the_real_frontier_target_is_sent_to_producer(tmp_path):
    producer = RecordingFixtureProducer()
    state = make_runner(tmp_path, producer).run(max_attempts=1)

    assert [request.target_type for request in producer.requests] == ["problem-frame"]
    assert state["artifacts"]["problem-frame"]["status"] == "ACCEPTED"
    assert state["status"] == "BLOCKED"  # bounded by the explicit one-attempt budget


def test_accepted_artifact_unlocks_and_is_passed_upstream_on_resume(tmp_path):
    producer = RecordingFixtureProducer()
    runner = make_runner(tmp_path, producer)
    runner.run(max_attempts=1)
    state = runner.run(max_attempts=11)

    evidence_request = next(request for request in producer.requests if request.target_type == "evidence-brief")
    upstream = evidence_request.upstream_artifacts
    assert len(upstream) == 1
    assert upstream[0].type == "problem-frame"
    assert Path(upstream[0].path).is_file()
    assert state["artifacts"]["evidence-brief"]["status"] == "ACCEPTED"


def test_gate_failure_rejects_and_does_not_unlock_downstream(tmp_path):
    rejected = make_runner(tmp_path, InvalidProducer()).run()

    assert rejected["status"] == "REJECTED"
    assert rejected["artifacts"]["problem-frame"]["status"] == "REJECTED"
    assert rejected["attempts"][0]["gate_result"]["passed"] is False

    producer = RecordingFixtureProducer()
    resumed = make_runner(tmp_path, producer).run(max_attempts=1)
    assert [request.target_type for request in producer.requests] == ["problem-frame"]
    assert "evidence-brief" not in resumed["artifacts"]


def test_missing_accepted_output_is_a_structured_blocker(tmp_path):
    producer = RecordingFixtureProducer()
    runner = make_runner(tmp_path, producer)
    state = runner.run(max_attempts=1)
    Path(state["artifacts"]["problem-frame"]["output"]).unlink()

    blocked = runner.run(max_attempts=1)
    assert blocked["status"] == "BLOCKED"
    assert blocked["blockers"][0]["type"] == "assumption-register"
    assert blocked["blockers"][0]["reason"] == "missing required inputs"
    assert blocked["blockers"][0]["inputs"] == [
        {"type": "problem-frame", "reason": "accepted output is missing"}
    ]


def test_unbound_dependency_frontier_is_explicitly_blocked(tmp_path):
    producer = RecordingFixtureProducer()
    state = make_runner(tmp_path, producer).run()

    assert state["status"] == "BLOCKED"
    assert state["artifacts"]["current-state-assessment"]["status"] == "ACCEPTED"
    for artifact_type in (
        "assumption-register", "business-objectives", "open-questions",
        "stakeholder-map", "kpi-model",
    ):
        assert state["artifacts"][artifact_type]["status"] == "ACCEPTED"
    assert state["blockers"]
    assert all(item["reason"] == "ready but has no Skill binding" for item in state["blockers"])


def test_run_manifest_carries_work_order_gate_and_timestamps(tmp_path):
    state = make_runner(tmp_path, RecordingFixtureProducer()).run(max_attempts=1)
    manifest = state["attempts"][0]

    assert state["run_id"] == "run"
    assert state["project"] == "projects/pp20/problem.yaml"
    assert manifest["target"] == {"id": "PP20-A01", "type": "problem-frame"}
    assert manifest["producer"] == "recording-local-fixture"
    assert manifest["inputs"] == []
    assert Path(manifest["output"]).is_file()
    assert manifest["gate_result"] == {"passed": True, "failures": []}
    assert manifest["status"] == "ACCEPTED"
    assert manifest["attempt_number"] == 1
    assert manifest["started_at"] and manifest["finished_at"]
    assert (tmp_path / "run" / "run.json").is_file()


def test_execution_layer_has_no_llm_or_network_imports():
    banned = {
        "anthropic", "openai", "cohere", "google", "litellm", "langchain",
        "requests", "httpx", "urllib", "http", "socket", "aiohttp",
    }
    for path in (ROOT / "scripts" / "pipeline.py", ROOT / "scripts" / "run_pipeline.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [item.name for item in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            assert all(name.split(".")[0] not in banned for name in names), path
