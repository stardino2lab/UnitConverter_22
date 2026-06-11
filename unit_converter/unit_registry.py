"""Unit registration and lookup (OCP extension point)."""

from unit_converter.domain.length_unit import Feet, LengthUnit, Meter, Yard


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, LengthUnit] = {}

    def register(self, unit: LengthUnit) -> None:
        self._units[unit.name] = unit

    def get(self, name: str) -> LengthUnit:
        if name not in self._units:
            raise KeyError(f"Unknown unit: {name}")
        return self._units[name]

    def all_units(self) -> list[LengthUnit]:
        return list(self._units.values())


def default_registry() -> UnitRegistry:
    registry = UnitRegistry()
    for unit in (Meter(), Feet(), Yard()):
        registry.register(unit)
    return registry
