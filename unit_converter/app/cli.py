"""CLI orchestration — parse input, convert, and report errors."""

import sys

from unit_converter.app.input_parser import FormatError, NegativeValueError, parse
from unit_converter.app.output_formatter import format_output
from unit_converter.domain.converter import Converter
from unit_converter.domain.unit_registry import default_registry


def run(input_line: str) -> int:
    try:
        unit_name, value = parse(input_line)
    except FormatError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except NegativeValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    registry = default_registry()
    try:
        source_unit = registry.get(unit_name)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    converter = Converter(registry)
    results = converter.convert_all(source_unit, value)
    print(format_output(source_unit.name, value, results))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    input_line = args[0] if args else sys.stdin.readline().rstrip("\n")
    return run(input_line)
