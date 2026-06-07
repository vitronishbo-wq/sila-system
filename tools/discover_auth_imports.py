#!/usr/bin/env python3
"""
Discover all module-level auth imports that need consolidation.
Phase 2 of IAM consolidation: Find all imports to consolidate.
"""

import re
from collections import defaultdict
from pathlib import Path

# Define the old auth import patterns to find
AUTH_PATTERNS = {
    # Group 1: JWT (Most Specific)
    "jwt": [
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth_gateway.*jwt",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth\s+import.*jwt",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth\s+import.*JWT",
    ],
    # Group 2: Policies
    "policy": [
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth_gateway.*policy",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth_gateway.*policy_engine",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth.*policy",
    ],
    # Group 3: Guards/Permissions
    "guard": [
        r"from\s+(?:apps\.backend\.)?(?:app\.)?(?:shared|app)\.auth\s+import",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth_gateway.*permission",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth.*guard",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth.*permission",
    ],
    # Group 4: Roles (Least Specific)
    "role": [
        r"from\s+(?:apps\.backend\.)?(?:app\.)?modules\.identity.*role",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.access_control",
        r"from\s+(?:apps\.backend\.)?(?:app\.)?core\.auth.*role",
    ],
}


def find_module_files_with_auth_imports() -> dict[str, list[tuple[str, str, str]]]:
    """
    Scan all modules for auth imports.
    Returns: {group: [(file_path, line_number, import_statement), ...]}
    """
    modules_path = Path("/home/dev03wsl/sila-system/apps/backend/app/modules")
    results = defaultdict(list)

    # Walk through all Python files in modules
    for py_file in modules_path.rglob("*.py"):
        # Skip test and pycache directories
        if "__pycache__" in str(py_file) or "/.pytest_cache/" in str(py_file):
            continue

        try:
            with open(py_file, encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")

                # Check each pattern
                for group, patterns in AUTH_PATTERNS.items():
                    for pattern in patterns:
                        for line_num, line in enumerate(lines, 1):
                            if re.search(pattern, line, re.IGNORECASE):
                                rel_path = str(py_file.relative_to(modules_path.parent.parent))
                                results[group].append((rel_path, line_num, line.strip()))
                                break  # Only record once per line
        except Exception:
            pass  # Skip files that can't be read

    return results


def main():
    print("=" * 80)
    print("SILA PHASE 2: MODULE AUTH IMPORT CONSOLIDATION DISCOVERY")
    print("=" * 80)
    print()

    results = find_module_files_with_auth_imports()

    # Summary
    total_files = 0
    group_order = ["jwt", "policy", "guard", "role"]

    for group in group_order:
        files = results.get(group, [])
        unique_files = len(set(f[0] for f in files))
        total_files += unique_files

        print(f"\n{'GROUP ' + group.upper() + ':':40} {len(files)} imports in {unique_files} files")
        print("-" * 80)

        # Group by file
        by_file = defaultdict(list)
        for filepath, line_num, stmt in files:
            by_file[filepath].append((line_num, stmt))

        for filepath in sorted(by_file.keys()):
            print(f"  {filepath}")
            for line_num, stmt in by_file[filepath]:
                print(f"    Line {line_num}: {stmt[:70]}")

    print()
    print("=" * 80)
    print(f"TOTAL: {total_files} unique files need consolidation")
    print("=" * 80)

    # Save results to file
    output_path = Path("/home/dev03wsl/sila-system/PHASE2_AUTH_IMPORTS_DISCOVERED.txt")
    with open(output_path, "w") as f:
        f.write("PHASE 2: Module Auth Imports to Consolidate\n")
        f.write("=" * 80 + "\n\n")

        for group in group_order:
            files = results.get(group, [])
            by_file = defaultdict(list)
            for filepath, line_num, stmt in files:
                by_file[filepath].append((line_num, stmt))

            f.write(f"\n{group.upper()} IMPORTS:\n")
            f.write("-" * 80 + "\n")
            for filepath in sorted(by_file.keys()):
                f.write(f"{filepath}\n")
                for line_num, stmt in by_file[filepath]:
                    f.write(f"  {line_num}: {stmt}\n")

    print("\nFull results saved to: PHASE2_AUTH_IMPORTS_DISCOVERED.txt")


if __name__ == "__main__":
    main()
