import json

import attrs

from . import config
from .records import Problem
from .sandbox import run_tests


def load_problems() -> dict[str, Problem]:
    lines = config.PROBLEM_SET_FILE.read_text(encoding="utf-8").splitlines()
    problems = [Problem(**json.loads(line)) for line in lines if line]
    return {problem.id: problem for problem in problems}


def prepare() -> None:
    if config.RESPONSES_DIR.exists() and config.PROBLEM_SET_FILE.exists():
        raise SystemExit("v1 is frozen (responses/ exists); bump to v2.")

    kept: list[Problem] = []
    dropped = 0
    for problem_id, settings in config.PROBLEMS.items():
        problem_dir = config.PROBLEMS_DIR / problem_id

        test_file = next(problem_dir.glob("*_test.py")).name
        tests = (problem_dir / test_file).read_text(encoding="utf-8")

        reference = {
            path.name: path.read_text(encoding="utf-8")
            for path in sorted(problem_dir.glob("*.py"))
            if path.name != test_file
        }

        result = run_tests(reference, test_file, tests)
        if not result.passed:
            print(f"drop {problem_id}: {result.failed or result.tail}")
            dropped += 1
            continue

        instructions_file = problem_dir / "instructions.txt"
        kept.append(
            Problem(
                id=problem_id,
                instructions=instructions_file.read_text(encoding="utf-8"),
                files=list(reference),
                reference=reference,
                test_file=test_file,
                tests=tests,
                human_minutes=settings.human_minutes,
                banned_imports=settings.banned_imports,
            )
        )

    config.PROBLEM_SET_FILE.write_text(
        "".join(json.dumps(attrs.asdict(p), ensure_ascii=False) + "\n" for p in kept),
        encoding="utf-8",
    )

    print(f"kept {len(kept)}, dropped {dropped}")
