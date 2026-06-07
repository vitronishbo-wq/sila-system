#!/usr/bin/env python3
"""
Test runner script for SILA System.

This script provides a consistent way to run tests with proper configuration
and reporting. It can be used both locally and in CI environments.
"""

import sys
from pathlib import Path

# Resolve project root and ensure scripts is importable
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    # Import the main function from the canonical runner
    import run_tests as canonical_runner  # type: ignore
except Exception as exc:  # pragma: no cover
    print(f"Failed to import scripts/run_tests.py: {exc}")
    sys.exit(1)

if __name__ == "__main__":
    try:
        sys.exit(canonical_runner.main())
    except KeyboardInterrupt:
        print("\nTest run cancelled by user")
        sys.exit(1)
