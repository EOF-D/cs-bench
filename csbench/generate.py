import json
import os

import attrs

from . import config
from .clients import call_model
from .prepare import load_problems
from .submission import build_prompt, submission_schema


def generate(
    models: list[str] | None,
    problem_ids: list[str] | None,
    n_samples: int,
) -> None:
    problems = load_problems()

    for model in models or config.MODELS:
        for problem_id in problem_ids or problems:
            problem = problems[problem_id]
            prompt = build_prompt(problem.instructions, problem.files)
            schema = submission_schema(problem.files)

            for sample in range(n_samples):
                tag = f"{model}/{problem_id}/{sample}"

                path = config.RESPONSES_DIR / model / problem_id / f"{sample}.json"
                if path.exists():
                    continue

                try:
                    response = call_model(model, prompt, schema)
                except Exception as error:
                    print(f"{tag}: {type(error).__name__}: {error}")
                    continue

                # Write then rename, so resume never skips a half file.
                path.parent.mkdir(parents=True, exist_ok=True)
                tmp = path.with_suffix(".tmp")
                tmp.write_text(
                    json.dumps(attrs.asdict(response), ensure_ascii=False),
                    encoding="utf-8",
                )

                os.replace(tmp, path)
                print(f"{tag}: {response.stop_reason}")
