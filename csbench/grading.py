import ast
import subprocess
import sys
import tempfile
from pathlib import Path

from . import config
from .records import Problem, Response, Row
from .sandbox import run_tests


def count_pep8_issues(files: dict[str, str]) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        paths: list[str] = []
        for name, code in files.items():
            path = Path(tmp) / name
            path.write_text(code, encoding="utf-8")
            paths.append(str(path))

        proc = subprocess.run(
            [sys.executable, "-m", "pycodestyle", *paths],
            capture_output=True,
            text=True,
        )

    return len(proc.stdout.splitlines())  # One line per issue.


def find_banned_imports(files: dict[str, str], banned: list[str]) -> list[str]:
    # NOTE: Misses imports made through __import__ or importlib.
    hits: set[str] = set()

    for code in files.values():
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]

            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]

            else:
                continue

            hits |= {module.split(".")[0] for module in modules} & set(banned)

    return sorted(hits)


def grade(
    model: str,
    sample: int,
    problem: Problem,
    files: dict[str, str],
    response: Response | None = None,
) -> Row:
    """Grade one sample. `response` is None for the human baseline."""
    row = Row(model=model, problem=problem.id, sample=sample)

    if response is None:
        if problem.human_minutes is not None:
            row.latency_s = problem.human_minutes * 60

    else:
        row.stop_reason = response.stop_reason

        row.input_tokens = response.input_tokens
        row.output_tokens = response.output_tokens
        row.cost_usd = config.MODELS[model].cost(
            response.input_tokens, response.output_tokens
        )

        row.latency_s = response.latency_s

    if any(name not in files for name in problem.files):
        row.status = "no_code"
        return row

    result = run_tests(files, problem.test_file, problem.tests)
    if result.timed_out:
        row.status = "timeout"

    elif result.passed:
        row.status = "pass"

    else:
        row.status = "test_fail"

    row.failed_tests = result.failed
    row.tail = result.tail
    row.pep8 = count_pep8_issues(files)
    row.banned = find_banned_imports(files, problem.banned_imports)

    return row
