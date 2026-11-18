import json
from collections import Counter, defaultdict
from statistics import mean

import attrs

from . import config
from .grading import grade
from .prepare import load_problems
from .records import Problem, Response, Row
from .submission import parse_submission

HUMAN = "human"
MISSING = "-"
COLUMNS = [
    "model",
    "pass@1",
    f"pass@{config.NUM_SAMPLES}",
    "PEP 8 issues",
    "banned hits",
    "$ per solved",
    "time per solved",
]


def grade_all(problems: dict[str, Problem]) -> list[Row]:
    rows = [
        grade(HUMAN, 0, problem, problem.reference) for problem in problems.values()
    ]

    for path in sorted(config.RESPONSES_DIR.glob("*/*/*.json")):
        model, problem_id = path.parent.parent.name, path.parent.name
        if model not in config.MODELS or problem_id not in problems:
            print(f"warning: skipping {path} (unknown model or problem)")
            continue

        problem = problems[problem_id]
        response = Response(**json.loads(path.read_text(encoding="utf-8")))
        files = parse_submission(response.text, problem.files)
        rows.append(grade(model, int(path.stem), problem, files, response))

    return rows


def per_solved(total: float, solved: int) -> float | None:
    return total / solved if solved else None


def format_time(seconds: float | None) -> str:
    if seconds is None:
        return MISSING

    if seconds < 120:
        return f"{seconds:.0f}s"

    return f"{seconds / 60:.1f}min"


def summarize(model: str, rows: list[Row]) -> list[str]:
    """One report row: pass rates, style, cost and time for one model."""
    passes: defaultdict[str, list[bool]] = defaultdict(list)
    for row in rows:
        passes[row.problem].append(row.status == "pass")

    pass_at_1 = mean(sum(p) / len(p) for p in passes.values())
    pass_at_k = mean(float(any(p)) for p in passes.values())
    pep8 = [row.pep8 for row in rows if row.pep8 is not None]
    banned_hits = sum(1 for row in rows if row.banned)

    solved = sum(row.status == "pass" for row in rows)
    cost = per_solved(sum(row.cost_usd for row in rows), solved)

    # NOTE: Rows without a time (human with unknown minutes) are left out.
    timed = [row for row in rows if row.latency_s is not None]
    seconds = per_solved(
        sum(row.latency_s or 0.0 for row in timed),
        sum(row.status == "pass" for row in timed),
    )

    return [
        model,
        f"{pass_at_1:.2f}",
        f"{pass_at_k:.2f}",
        f"{mean(pep8):.1f}" if pep8 else MISSING,
        str(banned_hits),
        f"${cost:.2f}" if cost is not None and model != HUMAN else MISSING,
        format_time(seconds),
    ]


def missing_sample_warnings(
    model: str, rows: list[Row], problems: dict[str, Problem]
) -> list[str]:
    expected = config.NUM_SAMPLES
    counts = Counter(row.problem for row in rows)

    return [
        f"warning: {model}/{problem_id} has {counts[problem_id]} of {expected} samples"
        for problem_id in problems
        if counts[problem_id] < expected
    ]


def markdown_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def build_report(rows: list[Row], problems: dict[str, Problem]) -> str:
    table = [markdown_row(COLUMNS), markdown_row(["---"] * len(COLUMNS))]
    warnings: list[str] = []

    for model in [*config.MODELS, HUMAN]:
        model_rows = [row for row in rows if row.model == model]
        if not model_rows:
            continue

        if model != HUMAN:
            warnings += missing_sample_warnings(model, model_rows, problems)

        table.append(markdown_row(summarize(model, model_rows)))

    report = "\n".join(table)
    if warnings:
        report += "\n\n" + "\n".join(warnings)

    return report


def score() -> None:
    problems = load_problems()
    if not problems:
        raise SystemExit("problem set is empty; run prepare first")

    rows = grade_all(problems)
    config.RESULTS_FILE.write_text(
        json.dumps([attrs.asdict(row) for row in rows], indent=2),
        encoding="utf-8",
    )

    report = build_report(rows, problems)
    config.REPORT_FILE.write_text(report + "\n", encoding="utf-8")

    print(report)
