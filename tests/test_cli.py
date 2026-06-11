"""Track A — CLI boundary tests."""

import pytest


def test_u_in_01_empty_input_format_error(capsys):
    """U-IN-01: empty input → format error."""
    # Given: ""
    # When: CLI processes input
    # Then: format error message and non-zero exit code
    from unit_converter.cli import run

    exit_code = run("")
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "format" in captured.err.lower()


def test_u_in_02_missing_colon_format_error(capsys):
    """U-IN-02: 'meter' (no colon) → format error."""
    # Given: "meter"
    # When: CLI processes input
    # Then: format error message
    from unit_converter.cli import run

    exit_code = run("meter")
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "format" in captured.err.lower()


def test_u_in_03_negative_value_rejected(capsys):
    """U-IN-03: 'meter:-1' → negative value rejected."""
    # Given: "meter:-1"
    # When: CLI processes input
    # Then: rejection with error message
    from unit_converter.cli import run

    exit_code = run("meter:-1")
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "negative" in captured.err.lower()


def test_u_out_01_meter_input_prints_three_or_more_lines(capsys):
    """U-OUT-01: 'meter:2.5' → README-style output (golden master)."""
    # Given: "meter:2.5"
    # When: CLI runs successfully
    # Then: stdout matches tests/golden/u_out_01_meter_2_5.approved.txt
    from tests._approval import assert_matches_golden
    from unit_converter.cli import run

    exit_code = run("meter:2.5")
    captured = capsys.readouterr()
    assert exit_code == 0
    assert_matches_golden(captured.out, "u_out_01_meter_2_5.approved.txt")


def test_pfr_03_unregistered_unit_cubit_error(capsys):
    """PFR-03: 'cubit:1' (unregistered) → clear error."""
    # Given: "cubit:1"
    # When: CLI processes input
    # Then: clear error message and non-zero exit code
    from unit_converter.cli import run

    exit_code = run("cubit:1")
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "unknown unit" in captured.err.lower()
    assert "cubit" in captured.err.lower()
