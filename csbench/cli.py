"""csbench prepare | generate | score."""

import argparse

from dotenv import load_dotenv

from . import config
from .generate import generate
from .prepare import prepare
from .score import score


def main() -> None:
    parser = argparse.ArgumentParser(prog="csbench", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("prepare")
    commands.add_parser("score")

    gen = commands.add_parser("generate")
    gen.add_argument("--models", nargs="+", choices=list(config.MODELS))
    gen.add_argument("--problems", nargs="+")
    gen.add_argument("--n", type=int, default=config.NUM_SAMPLES)

    args = parser.parse_args()
    load_dotenv(config.ENV_FILE)

    match args.command:
        case "prepare":
            prepare()

        case "generate":
            generate(args.models, args.problems, args.n)

        case "score":
            score()

        case _:
            parser.error(f"unknown command: {args.command}")
