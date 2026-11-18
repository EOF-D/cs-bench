"""One call per model API, each returning a Response."""

import os
import time

from anthropic import Anthropic
from anthropic.types import TextBlock
from openai import OpenAI

from . import config
from .records import Model, Response


def call_anthropic(model: Model, prompt: str, schema: dict[str, object]) -> Response:
    client = Anthropic()
    with client.messages.stream(
        model=model.model_id,
        max_tokens=config.MAX_TOKENS,
        output_config={
            "effort": "high",
            "format": {"type": "json_schema", "schema": schema},
        },
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        message = stream.get_final_message()

    return Response(
        model_id=model.model_id,
        text="".join(
            block.text for block in message.content if isinstance(block, TextBlock)
        ),
        stop_reason=message.stop_reason,
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
        request_id=getattr(message, "_request_id", None),
    )


def call_omlx(model: Model, prompt: str, schema: dict[str, object]) -> Response:
    # TODO: Find how to turn on Nemotron reasoning in its model card.
    # TODO: Check that oMLX honors response_format.
    client = OpenAI(base_url=os.environ["OMLX_URL"], api_key="local")

    completion = client.chat.completions.create(
        model=model.model_id,
        max_tokens=config.MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "submission", "schema": schema, "strict": True},
        },
    )

    choice = completion.choices[0]
    usage = completion.usage

    return Response(
        model_id=model.model_id,
        text=choice.message.content or "",
        stop_reason=choice.finish_reason,
        input_tokens=usage.prompt_tokens if usage else 0,
        output_tokens=usage.completion_tokens if usage else 0,
        request_id=completion.id,
    )


def call_model(key: str, prompt: str, schema: dict[str, object]) -> Response:
    model = config.MODELS[key]
    start = time.perf_counter()

    if model.api == "anthropic":
        response = call_anthropic(model, prompt, schema)
    else:
        response = call_omlx(model, prompt, schema)

    response.latency_s = time.perf_counter() - start
    return response
