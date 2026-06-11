"""Golden Master · Approval Test harness."""

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    """actual 문자열을 tests/golden/{relative}와 비교. UPDATE_GOLDEN=1이면 기준 갱신."""
    golden_path = GOLDEN_DIR / relative

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8", newline="\n")
        return

    if not golden_path.exists():
        raise AssertionError(
            f"Golden file missing: {golden_path}\n"
            f"Run: UPDATE_GOLDEN=1 python -m pytest <test> -v"
        )

    expected = golden_path.read_text(encoding="utf-8")
    if actual == expected:
        return

    raise AssertionError(
        f"Golden mismatch: {relative}\n"
        f"--- expected ({golden_path})\n{expected}"
        f"--- actual\n{actual}"
    )
