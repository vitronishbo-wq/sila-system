#!/usr/bin/env python3
"""
🧹 SILA-System Root Directory Artifact Cleanup Script
======================================================

Purpose:
  Remove phantom/residual files created by VS Code extensions (Codex/Blackbox)
  when operating outside permitted scopes defined in .ai/AI_FILE_SCOPE.yaml

Logic:
  - Scans root directory for files with invalid shell characters
  - Identifies artifacts: quotes, operators, incomplete commands
  - Removes safely with confirmation and logging

Usage:
  python3 scripts/cleanup_artifacts.py [--dry-run] [--auto]

Options:
  --dry-run    Show what would be removed without actually deleting
  --auto       Remove without confirmation prompts
  -h, --help   Show this help message

Examples:
  # Dry run (preview)
  python3 scripts/cleanup_artifacts.py --dry-run

  # Remove with confirmation
  python3 scripts/cleanup_artifacts.py

  # Auto-remove all artifacts
  python3 scripts/cleanup_artifacts.py --auto
"""

import os
from pathlib import Path


class ArtifactCleaner:
    """Safely identify and remove phantom artifacts from root directory."""

    # Characters that indicate invalid/phantom filenames
    INVALID_CHARS = {
        "'": "Single quote",
        '"': "Double quote",
        "`": "Backtick",
        "$": "Dollar sign",
        ">": "Output redirect",
        "<": "Input redirect",
        "|": "Pipe operator",
        "(": "Opening parenthesis",
        ")": "Closing parenthesis",
        ";": "Semicolon",
        "\\": "Backslash",
    }

    # Known legitimate root files (whitelist)
    LEGITIMATE_ROOT = {
        "Dockerfile.alerts",
        "Makefile",
        "Makefile.db",
        "mypy.ini",
        "openapi.json",
        "pytest.ini",
        "tailwind.config.js",
        "conftest.py",
        "find_broken_imports.py",
        "temp_seed.py",
        "CONSOLIDATION_STATUS_REPORT.json",
        "DUPLICATION_ANALYSIS.csv",
        "DUPLICATION_ANALYSIS.json",
        "DUPLICATION_SUMMARY.csv",
        "startup.log",
    }

    def __init__(self, root_dir=".", dry_run=False, auto_remove=False):
        """Initialize cleaner with options."""
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.auto_remove = auto_remove
        self.artifacts = []
        self.removed_count = 0

    def scan(self):
        """Scan root directory for phantom artifacts."""
        print("🔍 Scanning root directory for phantom artifacts...\n")

        for filename in os.listdir(self.root_dir):
            filepath = self.root_dir / filename

            # Skip directories and legitimate files
            if not filepath.is_file() or filename in self.LEGITIMATE_ROOT:
                continue

            # Check for invalid characters
            if self._is_phantom(filename):
                self.artifacts.append((filename, self._get_reason(filename)))

        return self.artifacts

    @staticmethod
    def _is_phantom(filename):
        """Check if filename contains invalid shell characters."""
        return any(char in filename for char in ArtifactCleaner.INVALID_CHARS.keys())

    @staticmethod
    def _get_reason(filename):
        """Identify which characters make this a phantom file."""
        reasons = []
        for char, description in ArtifactCleaner.INVALID_CHARS.items():
            if char in filename:
                reasons.append(description)
        return ", ".join(reasons)

    def display_results(self):
        """Display scan results."""
        if not self.artifacts:
            print("✅ No phantom artifacts found!")
            return

        print(f"⚠️  Found {len(self.artifacts)} phantom artifact(s):\n")
        for filename, reason in self.artifacts:
            print(f"  • {filename}")
            print(f"    └─ Reason: {reason}\n")

    def remove(self):
        """Remove identified artifacts."""
        if not self.artifacts:
            print("✅ Nothing to remove\n")
            return

        print(
            f"\n🗑️  {'Would remove' if self.dry_run else 'Removing'} "
            f"{len(self.artifacts)} artifact(s)...\n"
        )

        if not self.auto_remove and not self.dry_run:
            response = input("Continue? (y/N): ").strip().lower()
            if response != "y":
                print("❌ Cancelled\n")
                return

        for filename, _ in self.artifacts:
            filepath = self.root_dir / filename

            if self.dry_run:
                print(f"  [DRY-RUN] Would remove: {filename}")
            else:
                try:
                    os.remove(filepath)
                    print(f"  ✓ Removed: {filename}")
                    self.removed_count += 1
                except Exception as e:
                    print(f"  ✗ Error removing {filename}: {e}")

    def summary(self):
        """Print summary report."""
        print("\n" + "=" * 60)
        if self.dry_run:
            print(f"📊 DRY-RUN REPORT: {len(self.artifacts)} artifact(s) would be removed")
        else:
            print(
                f"✅ CLEANUP COMPLETE: {self.removed_count}/{len(self.artifacts)} "
                f"artifact(s) removed successfully"
            )
        print("=" * 60 + "\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean phantom artifacts from SILA-System root directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview removals without deleting")
    parser.add_argument("--auto", action="store_true", help="Remove without confirmation prompts")

    args = parser.parse_args()

    cleaner = ArtifactCleaner(root_dir=".", dry_run=args.dry_run, auto_remove=args.auto)

    artifacts = cleaner.scan()
    cleaner.display_results()

    if artifacts:
        cleaner.remove()
        cleaner.summary()


if __name__ == "__main__":
    main()
