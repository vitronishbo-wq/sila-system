#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../apps/backend'))

print("=" * 70)
print("🔍 AUDITORIA FINAL: Core Module Import Validation")
print("=" * 70)

errors = []
successes = []

# Test 1: Core module structure
try:
    from app import core
    successes.append("✅ Core module loads successfully")
except Exception as e:
    errors.append(f"❌ Core module import failed: {e}")

# Test 2: Check for legacy files
legacy_files = [
    "events_old.py",
    "events_unified.py", 
    "iam_unified.py",
    "auth.py",
    "audit_legacy.py",
    "database.py",
    "db.py",
    "module_registry_new.py"
]

core_path = Path(__file__).parent.parent / "apps/backend/app/core"
found_legacy = []
for legacy_file in legacy_files:
    if (core_path / legacy_file).exists():
        found_legacy.append(legacy_file)

if not found_legacy:
    successes.append(f"✅ No legacy files remaining (checked {len(legacy_files)} files)")
else:
    errors.append(f"❌ Found {len(found_legacy)} legacy files: {found_legacy}")

# Test 3: Core submodules 
required_structures = [
    ("app.core.events", "Events system"),
    ("app.modules.identity", "Identity system"),
    ("app.core.audit", "Audit system"),
    ("app.core.db", "Database system"),
]

for module_path, description in required_structures:
    try:
        __import__(module_path)
        successes.append(f"✅ {description}: Imports successfully")
    except ImportError as e:
        errors.append(f"❌ {description} ({module_path}): {e}")
    except Exception as e:
        errors.append(f"❌ {description} ({module_path}): {e}")

# Test 4: Check for legacy import references
import_scan_files = [
    "apps/backend/app/core/events/__init__.py",
    "apps/backend/app/core/audit/__init__.py", 
    "apps/backend/app/core/security/__init__.py",
]

legacy_imports_found = 0
for file_path in import_scan_files:
    full_path = Path(__file__).parent.parent / file_path
    if full_path.exists():
        content = full_path.read_text()
        if any(legacy in content for legacy in ["events_old", "events_unified", "iam_unified", "audit_legacy"]):
            legacy_imports_found += 1
            errors.append(f"❌ Legacy imports found in {file_path}")

if legacy_imports_found == 0:
    successes.append(f"✅ No legacy imports in core __init__.py files ({len(import_scan_files)} checked)")

# Test 5: Domain boundary guardrail
# Domain layer must not depend directly on platform/infrastructure concerns.
domain_root = Path(__file__).parent.parent / "apps/backend/app/modules"
domain_files = list(domain_root.glob("**/domain/**/*.py"))
domain_violations = []

for py_file in domain_files:
    try:
        content = py_file.read_text(encoding="utf-8")
    except Exception:
        # Keep scan resilient on odd encodings
        continue

    if "app.platform" in content:
        domain_violations.append(
            f"❌ Domain importing platform: {py_file.relative_to(Path(__file__).parent.parent)}"
        )

    if "from sqlalchemy.orm import Session" in content or "sqlalchemy.orm.Session" in content:
        domain_violations.append(
            f"❌ Domain using sqlalchemy.orm.Session: {py_file.relative_to(Path(__file__).parent.parent)}"
        )

if domain_violations:
    errors.extend(domain_violations)
else:
    successes.append(
        f"✅ Domain boundary guardrail passed ({len(domain_files)} domain Python files scanned)"
    )

# Print results
print("\n📊 RESULTS:")
print("-" * 70)

for success in successes:
    print(success)

if errors:
    print("\n⚠️  ERRORS:")
    for error in errors:
        print(error)
    sys.exit(1)
else:
    print("\n" + "=" * 70)
    print("✅ AUDITORIA FINAL: ALL CHECKS PASSED")
    print("🎉 Core sanitization verified successfully!")
    print("=" * 70)
    sys.exit(0)
