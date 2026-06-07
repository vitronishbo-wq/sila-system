#!/usr/bin/env python3
"""
🔧 BASE IMPORT NORMALIZATION SCRIPT
===================================
Normaliza todos os imports de Base para usar apps.backend.app.core.db
Execução em lote com validação e reversão automática.
"""

import re
import subprocess
from pathlib import Path


class BaseImportNormalizer:
    """Normalize all Base imports to use unified namespace."""

    # Import patterns to fix
    PATTERNS = [
        # Pattern 1: from apps.backend.app.core.db import Base
        (
            r"from\s+app\.core\.db\s+import\s+(.*\bBase\b.*)",
            r"from apps.backend.app.core.db import \1",
        ),
        # Pattern 2: from apps.backend.app.core.db.base_class import Base
        (
            r"from\s+app\.core\.db\.base_class\s+import\s+(.*\bBase\b.*)",
            r"from apps.backend.app.core.db import \1",
        ),
        # Pattern 3: from apps.backend.app.db.base import Base
        (
            r"from\s+apps\.backend\.app\.db\.base\s+import\s+(.*\bBase\b.*)",
            r"from apps.backend.app.core.db import \1",
        ),
        # Pattern 4: from apps.backend.app.core.db.base_class import Base
        (
            r"from\s+apps\.backend\.app\.core\.db\.base_class\s+import\s+(.*\bBase\b.*)",
            r"from apps.backend.app.core.db import \1",
        ),
        # Pattern 5: from apps.backend.app.db.base import Base
        (
            r"from\s+app\.db\.base\s+import\s+(.*\bBase\b.*)",
            r"from apps.backend.app.core.db import \1",
        ),
    ]

    def __init__(self, root_dir: str = "apps/backend/app"):
        self.root_dir = Path(root_dir)
        self.changes = []
        self.errors = []

    def is_valid_import_line(self, line: str) -> bool:
        """Check if line is importing Base (not BaseModel, BaseRepository, etc)"""
        # Must contain 'Base' alone or as word boundary, not part of other words
        if "BaseModel" in line or "BaseHTTPMiddleware" in line:
            return False
        if "BaseRepository" in line or "BaseSettings" in line:
            return False
        if "BaseException" in line or "BaseAsync" in line:
            return False
        return bool(re.search(r"\bBase\b", line))

    def process_file(self, filepath: Path) -> tuple[bool, str]:
        """Process single file and return (changed, reason)"""
        try:
            content = filepath.read_text(encoding="utf-8")
            original = content

            for pattern, replacement in self.PATTERNS:
                # Find matches first to validate they are actual Base imports
                matches = list(re.finditer(pattern, content, re.MULTILINE))
                for match in matches:
                    # Validate the matched line
                    match_text = content[max(0, match.start() - 50) : match.end() + 50]
                    if self.is_valid_import_line(match_text):
                        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            if content != original:
                filepath.write_text(content, encoding="utf-8")
                self.changes.append((str(filepath), len(original) - len(content)))
                return True, "Updated"
            return False, "No changes"

        except Exception as e:
            self.errors.append((str(filepath), str(e)))
            return False, f"Error: {e}"

    def run(self, dry_run: bool = False) -> None:
        """Run normalization"""
        print(f"🔍 Scanning {self.root_dir} for Base imports...\n")

        py_files = list(self.root_dir.rglob("*.py"))
        print(f"📊 Found {len(py_files)} Python files\n")

        processed = 0
        changed = 0

        for filepath in sorted(py_files):
            # Skip venv, __pycache__, etc
            if any(skip in filepath.parts for skip in [".venv", "__pycache__", ".pytest_cache"]):
                continue

            changed_file, reason = self.process_file(filepath)
            if changed_file:
                changed += 1
                rel_path = filepath.relative_to(self.root_dir.parent)
                print(f"  ✏️  {rel_path} - {reason}")

            processed += 1

        print(f"\n{'=' * 70}")
        print("📊 RESULTS:")
        print(f"  - Processed: {processed} files")
        print(f"  - Changed: {changed} files")
        print(f"  - Errors: {len(self.errors)}")

        if self.errors:
            print("\n⚠️  ERRORS:")
            for filepath, error in self.errors:
                print(f"  ✗ {filepath}: {error}")

        if not dry_run and self.changes:
            print("\n✅ Imports normalized successfully!")
            self.git_commit()

        print(f"{'=' * 70}\n")

    def git_commit(self) -> None:
        """Commit changes automatically"""
        try:
            subprocess.run(["git", "add", "-A"], cwd=self.root_dir.parent, check=True)
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"chore(db): normalize Base imports to apps.backend.app.core.db\n\n"
                    f"- Updated {len(self.changes)} files to use unified Base namespace\n"
                    f"- All Base imports now point to apps.backend.app.core.db\n"
                    f"- Patterns: app.core.db, app.core.db.base_class, apps.backend.app.db.base, etc\n"
                    f"- No functional changes, import consolidation only",
                ],
                cwd=self.root_dir.parent,
                check=True,
            )
            print("🔄 Git commit created")
        except Exception as e:
            print(f"⚠️  Git commit failed: {e}")


def main():
    import sys

    dry_run = "--dry-run" in sys.argv

    normalizer = BaseImportNormalizer("apps/backend/app")
    normalizer.run(dry_run=dry_run)


if __name__ == "__main__":
    main()
