#!/usr/bin/env python3
"""Find all broken auth/security imports in the codebase."""

import os
import re
from pathlib import Path
from collections import defaultdict

# Patterns we're looking for
OLD_PATTERNS = [
    "from app.core.auth import",
    "from app.core.security import",
]

results = defaultdict(list)
root_path = Path("/home/dev03wsl/sila-system")

# Search in the most relevant directories
search_dirs = [
    root_path / "apps",
    root_path / "scripts",
    root_path / "tests",
    root_path / "src",
]

# Skip these directories to speed up search
SKIP_DIRS = {
    "__pycache__", ".pytest_cache", "node_modules", ".git",
    ".venv", "venv", "dist", "build", ".egg-info"
}

def should_skip(path_str):
    """Check if path should be skipped."""
    return any(skip in path_str for skip in SKIP_DIRS)

for search_dir in search_dirs:
    if not search_dir.exists():
        print(f"  [{search_dir.name}] - not found")
        continue
        
    print(f"  Searching in {search_dir.name}/...", flush=True)
    count = 0
    
    for py_file in search_dir.rglob("*.py"):
        # Skip large directories to speed up search
        if should_skip(str(py_file)):
            continue
        
        count += 1
        if count % 500 == 0:
            print(f"    Scanned {count} files...", flush=True)
            
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                for line_num, line in enumerate(lines, 1):
                    for pattern in OLD_PATTERNS:
                        if pattern in line:
                            rel_path = str(py_file.relative_to(root_path))
                            results[rel_path].append((line_num, line.rstrip()))
                            break  # Only count once per line
        except Exception as e:
            pass

# Print results
if results:
    print("\n" + "=" * 100)
    print("BROKEN IMPORTS FOUND")
    print("=" * 100)
    
    for filepath in sorted(results.keys()):
        print(f"\n{filepath}")
        for line_num, line_content in results[filepath]:
            print(f"  Line {line_num}: {line_content}")
    
    print("\n" + "=" * 100)
    print(f"SUMMARY: Found {len(results)} files with broken imports")
    print("=" * 100)
    
    # Create summary for easy migration
    print("\nFILES NEEDING MIGRATION:")
    for filepath in sorted(results.keys()):
        print(f"  - {filepath}")
else:
    print("No broken imports found!")
