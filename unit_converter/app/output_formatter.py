"""Format conversion results in README line style."""


def format_output(source_unit: str, value: float, results: dict[str, float]) -> str:
    lines = [
        f"{_format_number(value)} {source_unit} = {_format_number(converted)} {target_unit}"
        for target_unit, converted in results.items()
    ]
    return "\n".join(lines)


def _format_number(number: float) -> str:
    return f"{number:.4f}".rstrip("0").rstrip(".")
