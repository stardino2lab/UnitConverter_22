"""Track A — CLI boundary tests."""

import pytest


def test_u_in_01_empty_input_format_error():
    """U-IN-01: empty input → format error."""
    # Given: ""
    # When: CLI processes input
    # Then: format error message and non-zero exit code
    pytest.fail("RED: U-IN-01")


def test_u_in_02_missing_colon_format_error():
    """U-IN-02: 'meter' (no colon) → format error."""
    # Given: "meter"
    # When: CLI processes input
    # Then: format error message
    pytest.fail("RED: U-IN-02")


def test_u_in_03_negative_value_rejected():
    """U-IN-03: 'meter:-1' → negative value rejected."""
    # Given: "meter:-1"
    # When: CLI processes input
    # Then: rejection with error message
    pytest.fail("RED: U-IN-03")


def test_u_out_01_meter_input_prints_three_or_more_lines():
    """U-OUT-01: 'meter:2.5' → README-style output (3+ lines)."""
    # Given: "meter:2.5"
    # When: CLI runs successfully
    # Then: stdout has 3+ lines (meter, feet, yard in README format)
    pytest.fail("RED: U-OUT-01")


def test_pfr_03_unregistered_unit_cubit_error():
    """PFR-03: 'cubit:1' (unregistered) → clear error."""
    # Given: "cubit:1"
    # When: CLI processes input
    # Then: clear error message and non-zero exit code
    pytest.fail("RED: PFR-03")
