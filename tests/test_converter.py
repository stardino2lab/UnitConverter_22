"""Track B — Domain conversion tests (no mocks)."""

import pytest


def test_d_cnv_01_feet_to_meter():
    """D-CNV-01: 1 feet → 0.3048 m (±ε)."""
    # Given: 1 feet
    # When: to_meter(feet, 1)
    # Then: result ≈ 0.3048 within tolerance
    from unit_converter.domain.length_unit import Feet

    feet = Feet()
    assert feet.to_meter(1) == pytest.approx(0.3048, rel=1e-4)


def test_d_cnv_02_meter_to_feet_five_decimals():
    """D-CNV-02: 2.5 m → 8.20210 ft (5 decimal places)."""
    # Given: 2.5 meter input
    # When: convert_all from meter
    # Then: feet ≈ 8.20210 (5 decimal places)
    from unit_converter.domain.converter import Converter
    from unit_converter.domain.unit_registry import default_registry

    registry = default_registry()
    converter = Converter(registry)
    meter = registry.get("meter")
    results = converter.convert_all(meter, 2.5)
    assert round(results["feet"], 5) == 8.20210


def test_d_cnv_03_feet_yard_meter_consistency_via_meter_hub():
    """D-CNV-03: feet↔yard conversions agree when routed through meter."""
    # Given: a value in feet
    # When: convert_all to yard and meter
    # Then: yard and meter results are mutually consistent via meter hub
    from unit_converter.domain.converter import Converter
    from unit_converter.domain.unit_registry import default_registry

    registry = default_registry()
    converter = Converter(registry)
    feet = registry.get("feet")
    yard = registry.get("yard")

    value = 10.0
    results = converter.convert_all(feet, value)
    hub_meters = feet.to_meter(value)

    assert results["meter"] == pytest.approx(hub_meters)
    assert results["yard"] == pytest.approx(yard.from_meter(hub_meters))
    assert yard.to_meter(results["yard"]) == pytest.approx(hub_meters)
