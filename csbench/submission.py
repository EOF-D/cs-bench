import json

PROMPT = """Solve the following programming assignment in Python 3.12.

<assignment>
{instructions}
</assignment>

Reply with only a JSON object. Its keys must be exactly these file names:
{files}. Each value is the complete contents of that file as a string.
Do not include tests.
"""


def build_prompt(instructions: str, files: list[str]) -> str:
    return PROMPT.format(instructions=instructions, files=", ".join(files))


def submission_schema(files: list[str]) -> dict[str, object]:
    """JSON schema for an answer: one string of code per required file."""
    return {
        "type": "object",
        "properties": {name: {"type": "string"} for name in files},
        "required": files,
        "additionalProperties": False,
    }


def parse_submission(text: str, files: list[str]) -> dict[str, str]:
    """Read the JSON answer and keep only the required files that hold code."""
    try:
        answer = json.loads(text)
        found = {name: answer.get(name) for name in files}
    except (json.JSONDecodeError, AttributeError):
        return {}

    return {name: code for name, code in found.items() if isinstance(code, str)}
