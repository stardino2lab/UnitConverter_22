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
