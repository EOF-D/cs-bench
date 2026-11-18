import attrs


@attrs.frozen
class Model:
    api: str  # Either "anthropic" or "omlx".
    model_id: str
    usd_per_mtok_in: float
    usd_per_mtok_out: float

    def cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * self.usd_per_mtok_in + output_tokens * self.usd_per_mtok_out
        ) / 1_000_000


@attrs.frozen
class ProblemSettings:
    """Harness settings for one problem, kept out of the problem folder."""

    human_minutes: float | None = None
    banned_imports: list[str] = attrs.field(factory=list[str])


@attrs.define
class Problem:
    """One line of problem_set_v1.jsonl."""

    id: str
    instructions: str
    files: list[str]
    reference: dict[str, str]
    test_file: str
    tests: str
    human_minutes: float | None
    banned_imports: list[str]


@attrs.define
class Response:
    """Contents of responses/<model>/<problem>/<sample>.json."""

    model_id: str
    text: str
    stop_reason: str | None
    input_tokens: int
    output_tokens: int
    request_id: str | None
    latency_s: float = 0.0


@attrs.define
class TestRun:
    passed: bool
    failed: list[str]
    timed_out: bool
    tail: str


@attrs.define
class Row:
    """One graded sample in results.json."""

    model: str
    problem: str
    sample: int
    status: str = ""  # One of pass, test_fail, timeout or no_code.
    stop_reason: str | None = None
    failed_tests: list[str] = attrs.field(factory=list[str])
    tail: str = ""
    pep8: int | None = None
    banned: list[str] = attrs.field(factory=list[str])
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float = 0.0
    latency_s: float | None = None
