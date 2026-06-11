"""CLI orchestration — parse input and report errors."""

import sys

from unit_converter.app.input_parser import FormatError, NegativeValueError, parse


def run(input_line: str) -> int:
    try:
        parse(input_line)
    except FormatError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except NegativeValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    input_line = args[0] if args else sys.stdin.readline().rstrip("\n")
    return run(input_line)
