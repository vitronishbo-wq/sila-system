#!/usr/bin/env python3
"""
ALEMBIC MIGRATION HEALTH CHECK
Detects and resolves multiple migration heads
"""

import sys
from pathlib import Path
from collections import defaultdict
import re


def print_box(title="", width=80, char="="):
    """Print a box with title."""
    if title:
        padding_left = (width - len(title) - 2) // 2
        padding_right = width - len(title) - 2 - padding_left
        print(f"{char * padding_left} {title} {char * padding_right}")
    else:
        print(char * width)


def find_migration_files():
    """Find all Alembic migration files."""
    workspace = Path(__file__).parent.parent
    migration_paths = [
        workspace / "migrations" / "versions",
        workspace / "apps" / "backend" / "app" / "db" / "migrations" / "versions"
    ]
    
    migrations = []
    for path in migration_paths:
        if path.exists():
            migrations.extend(path.glob("*.py"))
    
    return sorted(migrations)


def extract_revision_info(file_path):
    """Extract revision info from migration file."""
    try:
        content = file_path.read_text()
        
        # Look for down_revision
        down_match = re.search(r"down_revision\s*=\s*['\"]([^'\"]*)['\"]", content)
        down_revision = down_match.group(1) if down_match else None
        
        # Look for revision
        rev_match = re.search(r"revision\s*=\s*['\"]([^'\"]*)['\"]", content)
        revision = rev_match.group(1) if rev_match else None
        
        return {
            "file": file_path.name,
            "revision": revision,
            "down_revision": down_revision,
            "path": file_path
        }
    except:
        return None


def detect_multiple_heads(migrations_info):
    """Detect multiple migration heads."""
    # A head is a migration with no dependent migration (down_revision not referenced by any other)
    all_revisions = {m["revision"] for m in migrations_info if m["revision"]}
    all_down_revisions = {m["down_revision"] for m in migrations_info if m["down_revision"]}
    
    heads = all_revisions - all_down_revisions
    
    return list(heads) if len(heads) > 1 else []


def check_duplicate_names(migrations_info):
    """Check for duplicate migration names."""
    names = defaultdict(list)
    for m in migrations_info:
        base_name = re.sub(r"^\d+_", "", m["file"])
        names[base_name].append(m["file"])
    
    duplicates = {k: v for k, v in names.items() if len(v) > 1}
    return duplicates


def analyze_migration_chain(migrations_info):
    """Analyze migration dependency chain."""
    by_revision = {m["revision"]: m for m in migrations_info if m["revision"]}
    
    chains = []
    visited = set()
    
    for migration in migrations_info:
        if migration["revision"] in visited:
            continue
        
        # Build chain backwards
        chain = []
        current = migration
        while current and current["revision"] not in visited:
            chain.append(current)
            visited.add(current["revision"])
            
            if current["down_revision"] and current["down_revision"] in by_revision:
                current = by_revision[current["down_revision"]]
            else:
                break
        
        if chain:
            chains.append(chain)
    
    return chains


def main():
    print_box("ALEMBIC MIGRATION HEALTH CHECK", width=80)
    
    # Step 1: Find migrations
    print("\nSTEP 1: Scanning Migration Files")
    print("-" * 80)
    
    migration_files = find_migration_files()
    print(f"Found {len(migration_files)} migration files")
    
    # Extract info
    migrations_info = []
    for mf in migration_files:
        if mf.name.endswith(".py") and mf.name != "__init__.py":
            info = extract_revision_info(mf)
            if info:
                migrations_info.append(info)
    
    print(f"Parsed {len(migrations_info)} migrations")
    print_progress_bar(len(migrations_info), len(migration_files))
    
    # Step 2: Check for duplicate names
    print("\nSTEP 2: Checking for Duplicate Migration Names")
    print("-" * 80)
    
    duplicates = check_duplicate_names(migrations_info)
    if duplicates:
        print(f"⚠️  Found {len(duplicates)} duplicate sets:")
        for dup_name, files in list(duplicates.items())[:5]:
            print(f"\n  {dup_name}")
            for f in files:
                print(f"    - {f}")
        
        print(f"\n⚠️  RISK: Multiple heads likely present")
        print(f"    These files should be merged or renamed:")
        for files in duplicates.values():
            print(f"    → alembic merge {'-m \"merge heads\" ' + ' '.join(files)}")
    else:
        print("✓ No duplicate migration names found")
        print_progress_bar(1, 1)
    
    # Step 3: Detect multiple heads
    print("\nSTEP 3: Detecting Multiple Migration Heads")
    print("-" * 80)
    
    heads = detect_multiple_heads(migrations_info)
    if heads:
        print(f"⚠️  MULTIPLE HEADS DETECTED: {len(heads)} heads found")
        for i, head in enumerate(heads[:5], 1):
            print(f"  {i}. {head}")
        
        print(f"\n✓ SOLUTION: Use alembic merge to consolidate")
        print(f"  Command: alembic merge -m 'consolidate migration heads'")
    else:
        print("✓ Single migration head detected (OK)")
        print_progress_bar(1, 1)
    
    # Step 4: Analyze chains
    print("\nSTEP 4: Migration Dependency Chains")
    print("-" * 80)
    
    chains = analyze_migration_chain(migrations_info)
    print(f"Migration chains: {len(chains)}")
    print(f"Total migrations: {len(migrations_info)}")
    
    if len(chains) > 1:
        print(f"\n⚠️  WARNING: {len(chains)} separate chains detected")
        print(f"   This indicates migration branches that need merging")
    else:
        print(f"\n✓ Single linear chain detected")
    
    # Summary
    print_box("SUMMARY & RECOMMENDATIONS", width=80)
    
    status_checks = [
        ("No duplicate names", not duplicates),
        ("Single head only", len(heads) < 2),
        ("Single chain", len(chains) == 1)
    ]
    
    passed = sum(1 for _, result in status_checks if result)
    
    for check_name, result in status_checks:
        indicator = "[✓]" if result else "[⚠️ ]"
        print(f"  {indicator} {check_name}")
    
    print("\nRECOMMENDED ACTIONS:")
    if duplicates or heads or len(chains) > 1:
        print("  1. Backup current database")
        print("  2. Run: alembic merge -m 'consolidate migration heads'")
        print("  3. Review generated merge migration")
        print("  4. Run: alembic upgrade head")
        print("  5. Verify database state")
    else:
        print("  • Migrations are healthy")
        print("  • No immediate action required")
        print("  • Continue with normal migrations")
    
    print_box()


def print_progress_bar(passed, total, width=40):
    """Print a progress bar."""
    percentage = (passed * 100) // total if total > 0 else 0
    filled = (passed * width) // total
    empty = width - filled
    bar = "█" * filled + "░" * empty
    print(f"  [{bar}] {passed}/{total} ({percentage}%)")


if __name__ == "__main__":
    main()
