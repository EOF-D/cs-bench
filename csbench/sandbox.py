"""Run hidden tests in an offline OrbStack container."""

import subprocess
import tempfile
import uuid
from pathlib import Path

from . import config
from .records import TestRun

TAIL_LINES = 20


def run_tests(
    files: dict[str, str],
    test_file: str,
    tests: str,
    timeout: int = config.TEST_TIMEOUT_S,
) -> TestRun:
    """Run the hidden tests against `files` in an offline container."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, code in {**files, test_file: tests}.items():
            (Path(tmp) / name).write_text(code, encoding="utf-8")

        container = f"bench-{uuid.uuid4().hex}"
        name_args = ["--name", container]
        mount_args = ["-v", f"{tmp}:/work", "-w", "/work"]
        test_args = ["python", "-m", "unittest", Path(test_file).stem]

        cmd = [
            *config.DOCKER,
            "run",
            *config.SANDBOX_FLAGS,
            *name_args,
            *mount_args,
            config.IMAGE,
            *test_args,
        ]

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            remove = [*config.DOCKER, "rm", "-f", container]
            subprocess.run(remove, capture_output=True)
            return TestRun(passed=False, failed=[], timed_out=True, tail="")

    lines = (proc.stdout + proc.stderr).splitlines()
    failed = [
        line.split(": ", 1)[1]
        for line in lines
        if line.startswith(("FAIL: ", "ERROR: "))
    ]

    return TestRun(
        passed=proc.returncode == 0,
        failed=failed,
        timed_out=False,
        tail="\n".join(lines[-TAIL_LINES:]),
    )
