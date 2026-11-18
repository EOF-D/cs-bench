from pathlib import Path

from .records import Model, ProblemSettings

ROOT = Path(__file__).resolve().parent.parent

ENV_FILE = ROOT / ".env"
PROBLEMS_DIR = ROOT / "problems"
PROBLEM_SET_FILE = ROOT / "problem_set_v1.jsonl"
RESPONSES_DIR = ROOT / "responses"
RESULTS_FILE = ROOT / "results.json"
REPORT_FILE = ROOT / "report.md"

NUM_SAMPLES = 5
MAX_TOKENS = 64_000
TEST_TIMEOUT_S = 60

DOCKER = ["docker", "--context", "orbstack"]
IMAGE = "python:3.12-slim"
SANDBOX_FLAGS = (
    "--rm --pull never --network none --memory 512m --memory-swap 512m "
    "--cpus 1 --pids-limit 128"
).split()

MODELS: dict[str, Model] = {
    "opus-5.5": Model("anthropic", "claude-opus-5-5", 4.0, 20.0),
    "opus-5": Model("anthropic", "claude-opus-5", 5.0, 25.0),
    "nemotron-3.5-bolt": Model("omlx", "TODO/v1/models", 0.0, 0.0),
}

# Problems to benchmark.
PROBLEMS: dict[str, ProblemSettings] = {
    "p2": ProblemSettings(human_minutes=75),
    "p3": ProblemSettings(banned_imports=["heapq", "queue", "networkx"]),
}
