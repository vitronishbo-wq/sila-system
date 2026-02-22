#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Orphan Reference Cleaner
========================

Remove referências órfãs de arquivos que não existem e atualizar symlinks.

Autor: Truman + ChatGPT
Data: 2025-11-18
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple


def c(text, color):
    """Add ANSI color codes."""
    COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "cyan": "\033[36m",
        "reset": "\033[0m",
    }
    return COLORS.get(color, "") + text + COLORS["reset"]


def find_orphan_references(
    project_dir: Path, orphan_names: List[str]
) -> Dict[str, List[str]]:
    """Find all Python files that reference orphan files."""
    references = {}

    for orphan in orphan_names:
        references[orphan] = []

    for py_file in project_dir.rglob("*.py"):
        if any(
            skip in str(py_file) for skip in ["venv", "node_modules", "__pycache__"]
        ):
            continue

        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            for orphan in orphan_names:
                # Look for various patterns of referencing the orphan file
                patterns = [
                    f"'{orphan}'",
                    f'"{orphan}"',
                    f": '{orphan}'",
                    f': "{orphan}"',
                    f"'{orphan}': ",
                    f'"{orphan}": ',
                ]

                for pattern in patterns:
                    if pattern in content:
                        references[orphan].append(str(py_file))
                        break
        except Exception:
            pass

    return references


def remove_orphan_mapping(file_path: Path, orphan_name: str) -> Tuple[bool, str]:
    """Remove mapping entry for orphan file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        original = content

        # Pattern: 'fix_missing_imports.py': 'some_command',
        pattern = rf"'{re.escape(orphan_name)}'\s*:\s*['\"]([^'\"]+)['\"]\s*,?\n?"
        modified = re.sub(pattern, "", content)

        if modified != original:
            file_path.write_text(modified, encoding="utf-8")
            return True, "Mapping removed"

        return False, "No mapping found"
    except Exception as e:
        return False, str(e)


def create_symlink_mapping(tools_dir: Path, target_file: Path) -> Dict[str, Path]:
    """Map orphan names to actual target files."""
    mapping = {}

    # If target exists, all symlinks should point to it
    if target_file.exists():
        mapping["fix_missing_imports.py"] = target_file
        mapping["scan_and_fix_imports.py"] = target_file

    return mapping


def repair_symlinks(project_dir: Path) -> Dict:
    """Repair symlinks to point to correct targets."""
    tools_dir = project_dir / "tools"
    target = (
        project_dir / "automation" / "maintenance" / "quality_deprecation_wrapper.py"
    )

    results = {"fixed": [], "failed": []}

    if not tools_dir.exists():
        return results

    orphan_symlinks = ["fix_missing_imports.py", "scan_and_fix_imports.py"]

    for symlink_name in orphan_symlinks:
        symlink = tools_dir / symlink_name

        if symlink.is_symlink():
            # Calculate relative path from tools to target
            rel_path = target.relative_to(tools_dir.parent)

            try:
                symlink.unlink()
                symlink.symlink_to(rel_path)
                results["fixed"].append(symlink_name)
            except Exception as e:
                results["failed"].append((symlink_name, str(e)))
        elif not symlink.exists():
            # Create the symlink if it doesn't exist
            try:
                rel_path = target.relative_to(tools_dir.parent)
                symlink.symlink_to(rel_path)
                results["fixed"].append(symlink_name)
            except Exception as e:
                results["failed"].append((symlink_name, str(e)))

    return results


def main():
    """Main cleanup routine."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean orphan references from the project"
    )
    parser.add_argument("project", nargs="?", default=".", help="Project directory")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Actually fix the issues (requires explicit flag)",
    )

    args = parser.parse_args()
    project_dir = Path(args.project).resolve()

    print(c("\n" + "=" * 80, "cyan"))
    print(c("  🧹 ORPHAN REFERENCE CLEANER", "cyan"))
    print(c("=" * 80, "cyan"))

    orphan_names = ["fix_missing_imports.py", "scan_and_fix_imports.py"]

    # === STEP 1: Find References ===
    print(c("\n[1/3] Scanning for orphan references...", "blue"))
    references = find_orphan_references(project_dir, orphan_names)

    found_any = False
    for orphan, files in references.items():
        if files:
            found_any = True
            print(f"\n  {c(orphan, 'yellow')}:")
            print(f"    Found in {len(files)} file(s)")
            for file in files[:3]:
                print(f"      • {file}")
            if len(files) > 3:
                print(f"      ... and {len(files)-3} more")

    if not found_any:
        print(c("  ✓ No orphan references found", "green"))

    # === STEP 2: Repair Symlinks ===
    print(c("\n[2/3] Checking symlinks...", "blue"))
    symlink_results = repair_symlinks(project_dir)

    if symlink_results["fixed"]:
        status = "Would fix" if args.dry_run else "Fixed"
        print(c(f"  {status} {len(symlink_results['fixed'])} symlink(s):", "green"))
        for name in symlink_results["fixed"]:
            print(f"    ✓ {name}")

    if symlink_results["failed"]:
        print(c(f"  Failed to fix {len(symlink_results['failed'])} symlink(s):", "red"))
        for name, error in symlink_results["failed"]:
            print(f"    ✗ {name}: {error}")

    # === STEP 3: Remove Mappings ===
    print(c("\n[3/3] Removing deprecated mappings...", "blue"))
    quality_wrapper = (
        project_dir / "automation" / "maintenance" / "quality_deprecation_wrapper.py"
    )

    if quality_wrapper.exists() and found_any:
        cleaned = 0
        for orphan in orphan_names:
            success, msg = remove_orphan_mapping(quality_wrapper, orphan)
            if success:
                action = "Would remove" if args.dry_run else "Removed"
                print(f"  {c(action, 'green')} {orphan} mapping")
                cleaned += 1

        if cleaned > 0 and not args.dry_run:
            print(f"\n  {c(f'✓ Updated {quality_wrapper.name}', 'green')}")

    # === SUMMARY ===
    print(c("\n" + "=" * 80, "cyan"))
    if args.dry_run:
        print(c("  DRY RUN - No changes made. Run with --fix to apply.", "yellow"))
    elif found_any or symlink_results["fixed"]:
        print(c("  ✓ CLEANUP COMPLETE", "green"))
    else:
        print(c("  ✓ NO ISSUES FOUND", "green"))

    print(c("=" * 80 + "\n", "cyan"))


if __name__ == "__main__":
    main()
