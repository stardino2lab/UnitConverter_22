"""Length unit contract and P0 implementations (meter hub)."""

METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361


class LengthUnit:
    """Convert values to and from the meter hub."""

    @property
    def name(self) -> str:
        raise NotImplementedError

    def to_meter(self, value: float) -> float:
        raise NotImplementedError

    def from_meter(self, meters: float) -> float:
        raise NotImplementedError


class Meter(LengthUnit):
    @property
    def name(self) -> str:
        return "meter"

    def to_meter(self, value: float) -> float:
        return value

    def from_meter(self, meters: float) -> float:
        return meters


class Feet(LengthUnit):
    @property
    def name(self) -> str:
        return "feet"

    def to_meter(self, value: float) -> float:
        return value / METER_TO_FEET

    def from_meter(self, meters: float) -> float:
        return meters * METER_TO_FEET


class Yard(LengthUnit):
    @property
    def name(self) -> str:
        return "yard"

    def to_meter(self, value: float) -> float:
        return value / METER_TO_YARD

    def from_meter(self, meters: float) -> float:
        return meters * METER_TO_YARD
