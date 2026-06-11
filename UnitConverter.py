"""Backward-compatible entry point."""

from unit_converter.app.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
