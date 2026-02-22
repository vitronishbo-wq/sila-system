#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System Health & Integrity Checker
==================================

Diagnóstico automático de:
1. Symlinks quebrados (M2 - Integridade)
2. Referências órfãs (M3 - Confiabilidade)
3. Métricas de performance (M1 - Performance)
4. Snapshots estáveis do core

Autor: Truman + ChatGPT
Data: 2025-11-18
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


# ========================================
# COLORED OUTPUT
# ========================================


def c(text, color):
    """Add ANSI color codes."""
    COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "cyan": "\033[36m",
        "magenta": "\033[35m",
        "reset": "\033[0m",
    }
    return COLORS.get(color, "") + text + COLORS["reset"]


# ========================================
# DIAGNOSIS FUNCTIONS
# ========================================


def find_broken_symlinks(project_dir: Path) -> List[Dict]:
    """Identify broken symlinks in the project."""
    broken = []

    for root, dirs, files in os.walk(project_dir):
        # Skip venv and node_modules
        dirs[:] = [
            d for d in dirs if d not in ["venv", "node_modules", "__pycache__", ".git"]
        ]

        root_path = Path(root)
        for f in files:
            file_path = root_path / f

            # Check if it's a symlink
            if file_path.is_symlink():
                target = file_path.resolve()
                if not target.exists():
                    broken.append(
                        {
                            "symlink": str(file_path),
                            "target": str(file_path.readlink()),
                            "resolved_target": str(target),
                            "exists": False,
                        }
                    )
                else:
                    broken.append(
                        {
                            "symlink": str(file_path),
                            "target": str(file_path.readlink()),
                            "resolved_target": str(target),
                            "exists": True,
                        }
                    )

    return broken


def find_orphan_references(project_dir: Path, symlink_files: List[str]) -> Dict:
    """Find references to files that don't exist."""
    orphans = {}

    # Extract just filenames
    filenames = [Path(f).name for f in symlink_files]

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [
            d for d in dirs if d not in ["venv", "node_modules", "__pycache__", ".git"]
        ]

        for file in files:
            if not file.endswith(".py"):
                continue

            file_path = Path(root) / file
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for orphan_file in filenames:
                    if orphan_file in content:
                        if orphan_file not in orphans:
                            orphans[orphan_file] = []
                        orphans[orphan_file].append(str(file_path))
            except Exception:
                continue

    return orphans


def count_core_files(project_dir: Path) -> Tuple[int, float]:
    """Count core Python files (excluding venv, etc)."""
    count = 0
    total_size = 0

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [
            d for d in dirs if d not in ["venv", "node_modules", "__pycache__", ".git"]
        ]

        for f in files:
            if f.endswith(".py"):
                file_path = Path(root) / f
                try:
                    total_size += file_path.stat().st_size
                    count += 1
                except Exception:
                    pass

    return count, total_size / (1024 * 1024)  # Convert to MB


def run_master_index(project_dir: Path, quick: bool = True) -> Dict:
    """Run master_index_generator and capture metrics."""
    script_path = project_dir / "master_index_generator.py"

    if not script_path.exists():
        return {"error": "master_index_generator.py not found"}

    cmd = ["python3", str(script_path), str(project_dir), "--ext", "py"]

    if quick:
        cmd.extend(["--exclude", "venv", "node_modules", "__pycache__", ".git"])

    cmd.extend(["--sort", "size", "--json"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        # Read the JSON output
        json_file = project_dir / "all_code_index.json"
        if json_file.exists():
            data = json.loads(json_file.read_text())
            return {
                "file_count": len(data),
                "total_size_mb": sum(d.get("size_mb", 0) for d in data),
                "success": True,
            }
    except Exception as e:
        return {"error": str(e)}

    return {"error": "Could not parse index"}


# ========================================
# REPAIR FUNCTIONS
# ========================================


def fix_broken_symlinks(broken_links: List[Dict], project_dir: Path) -> Dict:
    """Fix broken symlinks by updating targets or removing them."""
    results = {"removed": [], "fixed": [], "unchanged": []}

    for link_info in broken_links:
        symlink = Path(link_info["symlink"])

        if not link_info["exists"]:
            # Try to find the correct target
            target_name = symlink.name

            # Search for the correct file
            found_target = None
            for root, dirs, files in os.walk(project_dir):
                dirs[:] = [d for d in dirs if d not in ["venv", "node_modules"]]
                if target_name in files:
                    found_target = Path(root) / target_name
                    break

            if found_target:
                # Remove old symlink and create new one
                try:
                    symlink.unlink()
                    symlink.symlink_to(found_target)
                    results["fixed"].append(
                        {"symlink": str(symlink), "new_target": str(found_target)}
                    )
                except Exception as e:
                    results["unchanged"].append(
                        {"symlink": str(symlink), "reason": str(e)}
                    )
            else:
                # Remove broken symlink
                try:
                    symlink.unlink()
                    results["removed"].append(str(symlink))
                except Exception as e:
                    results["unchanged"].append(
                        {"symlink": str(symlink), "reason": str(e)}
                    )

    return results


# ========================================
# REPORTING
# ========================================


def generate_report(project_dir: Path, auto_fix: bool = False) -> None:
    """Generate comprehensive health report."""

    print(c("\n" + "=" * 80, "cyan"))
    print(c("  🏥 SYSTEM HEALTH & INTEGRITY CHECK", "cyan"))
    print(c("=" * 80, "cyan"))

    # === STEP 1: Check Symlinks ===
    print(c("\n[1/4] Checking Symlinks...", "blue"))
    broken = find_broken_symlinks(project_dir)

    broken_only = [b for b in broken if not b["exists"]]

    if broken_only:
        print(c(f"\n⚠️  Found {len(broken_only)} broken symlink(s):\n", "yellow"))
        for link in broken_only:
            print(f"  • {c(link['symlink'], 'red')}")
            print(f"    Target: {link['target']}")
            print(f"    Resolved: {link['resolved_target']}")

        if auto_fix:
            print(c("\n🔧 Auto-fixing broken symlinks...", "magenta"))
            fix_results = fix_broken_symlinks(broken_only, project_dir)

            if fix_results["fixed"]:
                print(c(f"✓ Fixed {len(fix_results['fixed'])} symlink(s)", "green"))
            if fix_results["removed"]:
                print(
                    c(
                        f"✓ Removed {len(fix_results['removed'])} broken symlink(s)",
                        "green",
                    )
                )
    else:
        print(c("✓ All symlinks are valid", "green"))

    # === STEP 2: Check Orphan References ===
    print(c("\n[2/4] Checking Orphan References...", "blue"))
    broken_files = [b["symlink"] for b in broken_only]
    orphans = find_orphan_references(project_dir, broken_files)

    if orphans:
        print(c(f"\n⚠️  Found references to {len(orphans)} orphan file(s):\n", "yellow"))
        for orphan, references in orphans.items():
            print(f"  • {c(orphan, 'red')} (referenced in {len(references)} file(s))")
            for ref in references[:3]:  # Show first 3
                print(f"    - {ref}")
            if len(references) > 3:
                print(f"    ... and {len(references)-3} more")
    else:
        print(c("✓ No orphan references found", "green"))

    # === STEP 3: Core File Count ===
    print(c("\n[3/4] Measuring Core Code...", "blue"))
    core_count, core_size = count_core_files(project_dir)
    print(f"  Total Python files (core): {c(str(core_count), 'cyan')}")
    print(f"  Total size: {c(f'{core_size:.2f} MB', 'cyan')}")

    # === STEP 4: Performance Metrics ===
    print(c("\n[4/4] Running Performance Metrics...", "blue"))

    # M1: Quick scan time
    import time

    start = time.time()
    index_result = run_master_index(project_dir, quick=True)
    elapsed = time.time() - start

    print(f"\n  M1 (Performance):")
    print(f"    Scan time: {c(f'{elapsed:.2f}s', 'cyan')}")
    print(f"    Files indexed: {c(str(index_result.get('file_count', 0)), 'cyan')}")

    print(f"\n  M2 (Integrity):")
    if broken_only:
        print(
            f"    Status: {c('⚠️  WARNINGS PRESENT', 'red')} ({len(broken_only)} broken symlinks)"
        )
    else:
        print(f"    Status: {c('✓ CLEAN', 'green')} (0 warnings)")

    print(f"\n  M3 (Reliability):")
    print(f"    Core files: {c(str(core_count), 'cyan')} (expected: ~1099)")
    print(f"    Core size: {c(f'{core_size:.2f} MB', 'cyan')} (expected: ~8.11 MB)")

    # === SUMMARY ===
    print(c("\n" + "=" * 80, "cyan"))
    print(c("  SUMMARY", "cyan"))
    print(c("=" * 80, "cyan"))

    status = "✅ HEALTHY" if not broken_only else "⚠️  NEEDS REPAIR"
    print(f"Overall Status: {c(status, 'green' if not broken_only else 'red')}")

    print(c("\nMetrics Overview:", "blue"))
    metrics = {
        "M1 (Scan Time)": f"{elapsed:.2f}s",
        "M2 (Warnings)": "0" if not broken_only else str(len(broken_only)),
        "M3 (Core Stability)": (
            "✓ Stable" if abs(core_count - 1099) < 10 else "⚠ Drifting"
        ),
    }

    for metric, value in metrics.items():
        print(f"  • {metric}: {c(value, 'cyan')}")

    # === RECOMMENDATIONS ===
    if broken_only or orphans:
        print(c("\n📋 RECOMMENDED ACTIONS:", "yellow"))
        if broken_only:
            print(f"  1. Fix broken symlinks (run with --auto-fix)")
        if orphans:
            print(f"  2. Remove orphan references from code")
        print(f"  3. Re-run health check to verify")

    print()


# ========================================
# MAIN
# ========================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="System health and integrity checker for code projects"
    )
    parser.add_argument(
        "project", nargs="?", default=".", help="Project directory (default: current)"
    )
    parser.add_argument(
        "--auto-fix", action="store_true", help="Automatically fix broken symlinks"
    )
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()
    project_dir = Path(args.project).resolve()

    if not project_dir.exists():
        print(c(f"✗ Project directory not found: {project_dir}", "red"))
        exit(1)

    generate_report(project_dir, auto_fix=args.auto_fix)
