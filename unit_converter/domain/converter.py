"""Meter-hub conversion to all registered units."""

from unit_converter.domain.length_unit import LengthUnit
from unit_converter.unit_registry import UnitRegistry


class Converter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert_all(self, source_unit: LengthUnit, value: float) -> dict[str, float]:
        meters = source_unit.to_meter(value)
        return {
            unit.name: unit.from_meter(meters)
            for unit in self._registry.all_units()
        }
