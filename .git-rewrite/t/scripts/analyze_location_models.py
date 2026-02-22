#!/usr/bin/env python3
"""
Cleanup script for location models duplicate files.

This script identifies and reports on the following issues:
1. Legacy .orig files that should be deleted
2. Import conflicts between models.py and models/ package
3. Architectural inconsistencies

Status: REPORT ONLY (no automatic deletions)
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text):
    print(f"\n{BOLD}{BLUE}═══ {text} ═══{RESET}\n")


def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text):
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")


def analyze_models():
    """Analyze location models structure."""

    # Try multiple paths
    base_path = (
        Path(__file__).parent.parent / "apps" / "backend" / "modules" / "location"
    )

    if not base_path.exists():
        # Fallback: try from current working directory
        base_path = Path.cwd() / "apps" / "backend" / "modules" / "location"

    if not base_path.exists():
        print_error(f"Location module not found at: {base_path}")
        return

    print_header("LOCATION MODELS ANALYSIS")

    # Files to check
    files_to_check = {
        "models.py": base_path / "models.py",
        "models.py.orig": base_path / "models.py.orig",
        "models/__init__.py": base_path / "models" / "__init__.py",
        "models/region.py": base_path / "models" / "region.py",
        "models/region.py.orig": base_path / "models" / "region.py.orig",
    }

    # Check file existence
    print_header("FILE EXISTENCE CHECK")

    existing_files = []
    missing_files = []

    for name, path in files_to_check.items():
        if path.exists():
            size = path.stat().st_size
            existing_files.append(name)
            print_success(f"Found: {name} ({size} bytes)")
        else:
            missing_files.append(name)
            print_warning(f"Missing: {name}")

    # Check for duplicate .orig files
    print_header("LEGACY FILE DETECTION")

    orig_files = [f for f in existing_files if f.endswith(".orig")]
    if orig_files:
        print_error(f"Found {len(orig_files)} legacy .orig files:")
        for f in orig_files:
            path = files_to_check[f]
            print(f"  └─ {f}")
            print_info(f"     Action: DELETE THIS FILE (no longer needed)")
    else:
        print_success("No legacy .orig files found")

    # Check for import conflicts
    print_header("IMPORT CONFLICT DETECTION")

    models_py_exists = "models.py" in existing_files
    models_dir_exists = "models/__init__.py" in existing_files

    if models_py_exists and models_dir_exists:
        print_warning("CRITICAL: Both models.py and models/ package exist!")
        print_info("This creates ambiguity in Python imports:")
        print(f"  • from modules.location.models import X")
        print(f"    └─ Python prefers: models/__init__.py (package)")
        print(f"    └─ Never reaches: models.py (file)")
        print_error("RECOMMENDATION: Delete one of them!")
    elif models_py_exists:
        print_success("Only models.py exists (no conflict)")
    elif models_dir_exists:
        print_success("Only models/ package exists (no conflict)")
    else:
        print_error("Neither models.py nor models/ exists!")

    # Check for architectural consistency
    print_header("ARCHITECTURAL ANALYSIS")

    if "models.py" in existing_files:
        print_info(
            "models.py contains: CountryModel, ProvinceModel, MunicipalityModel, CommuneModel, CityModel, FullAddress"
        )
        print_info("Architecture: Specific hierarchy (6 entity types)")

    if "models/region.py" in existing_files:
        print_info("models/region.py contains: Region")
        print_info("Architecture: Generic recursive model")

    if models_py_exists and "models/region.py" in existing_files:
        print_error("TWO INCOMPATIBLE ARCHITECTURES DETECTED!")
        print_warning("Choose one:")
        print("  A. Keep models.py (specific hierarchy) - RECOMMENDED")
        print("  B. Keep models/region.py (generic recursive)")

    # Cleanup recommendations
    print_header("CLEANUP RECOMMENDATIONS")

    print(f"{BOLD}Priority 1 - DELETE (Immediate):{RESET}")
    if "models.py.orig" in existing_files:
        print(f"  [ ] Delete: models.py.orig")
        path = files_to_check["models.py.orig"]
        print(f"      rm {path}")

    if "models/region.py.orig" in existing_files:
        print(f"  [ ] Delete: models/region.py.orig")
        path = files_to_check["models/region.py.orig"]
        print(f"      rm {path}")

    print(f"\n{BOLD}Priority 2 - CONSOLIDATE (Strategic):{RESET}")
    if models_py_exists and models_dir_exists:
        print(f"  [ ] Choose architecture (A or B)")
        print(f"      Option A: Keep models.py, delete models/ package")
        print(f"      Option B: Keep models/ package, delete models.py")

    # Statistics
    print_header("SUMMARY STATISTICS")

    print(f"Total files checked: {len(files_to_check)}")
    print(f"Files found: {len(existing_files)}")
    print(f"Files missing: {len(missing_files)}")
    print(f"Legacy .orig files: {len(orig_files)}")

    if orig_files:
        print_error(f"ACTION REQUIRED: {len(orig_files)} files can be deleted")
    else:
        print_success("No legacy files to clean up")

    if models_py_exists and models_dir_exists:
        print_warning(f"ACTION REQUIRED: Architecture conflict detected")
    else:
        print_success("No import conflicts detected")


if __name__ == "__main__":
    analyze_models()

    print(f"\n{BOLD}═══ END OF ANALYSIS ═══{RESET}\n")
