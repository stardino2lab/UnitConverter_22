"""Parse and validate unit:value input strings."""


class ParseError(ValueError):
    """Base class for input parsing failures."""


class FormatError(ParseError):
    """Invalid unit:value format."""


class NegativeValueError(ParseError):
    """Negative numeric values are not allowed."""


def parse(text: str) -> tuple[str, float]:
    stripped = text.strip()
    if not stripped:
        raise FormatError("Invalid format: expected unit:value")

    if ":" not in stripped:
        raise FormatError("Invalid format: expected unit:value")

    parts = stripped.split(":")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise FormatError("Invalid format: expected unit:value")

    unit, value_str = parts[0], parts[1]
    try:
        value = float(value_str)
    except ValueError as exc:
        raise FormatError("Invalid format: value must be a number") from exc

    if value < 0:
        raise NegativeValueError("Negative values are not allowed")

    return unit, value
