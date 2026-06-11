"""Track B — Domain conversion tests (no mocks)."""

import pytest


def test_d_cnv_01_feet_to_meter():
    """D-CNV-01: 1 feet → 0.3048 m (±ε)."""
    # Given: 1 feet
    # When: to_meter(feet, 1)
    # Then: result ≈ 0.3048 within tolerance
    pytest.fail("RED: D-CNV-01")


def test_d_cnv_02_meter_to_feet_five_decimals():
    """D-CNV-02: 2.5 m → 8.20210 ft (5 decimal places)."""
    # Given: 2.5 meter input
    # When: convert_all from meter
    # Then: feet ≈ 8.20210 (5 decimal places)
    pytest.fail("RED: D-CNV-02")
