#!/usr/bin/env python3
"""
🛡️ AUTONOMOUS FILESYSTEM MANAGER
Full destructive capability with audit logging

Usage:
    python super_cleanup.py                # Interactive menu
    python super_cleanup.py --nuke <zone>  # Direct execution
    python super_cleanup.py --report        # Audit trail
    python super_cleanup.py --refactor-imports --target <path>
    python super_cleanup.py --consolidate-services --source <path> --dest <path>
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION - CHANGE WITH EXTREME CAUTION
# ============================================================================

WORKSPACE_ROOT = Path("/home/dev03wsl/sila-system")

# Folders that can be AGGRESSIVELY deleted
AGGRESSIVE_ZONES = {
    "tmp": {
        "path": WORKSPACE_ROOT / "tmp",
        "description": "Temporary files, build artifacts",
        "safe": True,
        "recursive": True,
    },
    "logs": {
        "path": WORKSPACE_ROOT / "logs",
        "description": "Application logs",
        "safe": True,
        "recursive": True,
    },
    "cache": {
        "path": WORKSPACE_ROOT / "apps/frontend/node_modules/.cache",
        "description": "Build cache",
        "safe": True,
        "recursive": True,
    },
    "pytest_cache": {
        "path": WORKSPACE_ROOT,
        "pattern": "__pycache__",
        "description": "Python cache directories",
        "safe": True,
        "recursive": True,
    },
    "reports_archive": {
        "path": WORKSPACE_ROOT / "reports/archive",
        "description": "Archived reports",
        "safe": True,
        "recursive": True,
    },
    "migrations_backups": {
        "path": WORKSPACE_ROOT / "migrations/backups",
        "description": "Old migration backups",
        "safe": True,
        "recursive": True,
    },
}

# PROTECTED ZONES - NEVER DELETE (even with --force)
PROTECTED_ZONES = [
    WORKSPACE_ROOT / "apps/frontend/src",
    WORKSPACE_ROOT / "apps/backend/src",
    WORKSPACE_ROOT / "apps/worker/src",
    WORKSPACE_ROOT / "apps/api_gateway/src",
    WORKSPACE_ROOT / "infra",
    WORKSPACE_ROOT / "docs",
    WORKSPACE_ROOT / "scripts",
    WORKSPACE_ROOT / ".git",
]

# Audit log
AUDIT_LOG = WORKSPACE_ROOT / ".cleanup_audit.jsonl"


# ============================================================================
# CORE FUNCTIONS
# ============================================================================


def log_action(action: str, target: str, status: str, details: str = ""):
    """Log all actions to audit trail."""
    record = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "target": str(target),
        "status": status,
        "details": details,
        "user": os.environ.get("USER", "unknown"),
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")


def is_protected(path: Path) -> bool:
    """Check if path is in protected zones."""
    try:
        path.relative_to(PROTECTED_ZONES[0])
    except ValueError:
        pass

    for protected in PROTECTED_ZONES:
        try:
            path.relative_to(protected)
            return True
        except ValueError:
            continue
    return False


def calculate_size(path: Path) -> tuple[int, int]:
    """Calculate total size of path (files, folders)."""
    total_size = 0
    file_count = 0
    if path.is_file():
        return path.stat().st_size, 1
    for entry in path.rglob("*"):
        if entry.is_file():
            total_size += entry.stat().st_size
            file_count += 1
    return total_size, file_count


def calculate_pattern_size(path: Path, pattern: str) -> tuple[int, int]:
    """Calculate total size for entries matching a pattern under path."""
    total_size = 0
    file_count = 0
    for entry in path.rglob(pattern):
        if entry.is_file():
            total_size += entry.stat().st_size
            file_count += 1
        elif entry.is_dir():
            size, count = calculate_size(entry)
            total_size += size
            file_count += count
    return total_size, file_count


def format_size(bytes_size: int) -> str:
    """Convert bytes to human readable."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def dry_run(zone: str) -> dict:
    """Preview what will be deleted."""
    if zone not in AGGRESSIVE_ZONES:
        return {"error": f"Unknown zone: {zone}"}

    zone_config = AGGRESSIVE_ZONES[zone]
    path = zone_config["path"]
    pattern = zone_config.get("pattern")

    if not path.exists():
        return {"zone": zone, "exists": False, "message": "Path does not exist"}

    if pattern:
        size, file_count = calculate_pattern_size(path, pattern)
    else:
        size, file_count = calculate_size(path)

    return {
        "zone": zone,
        "path": str(path),
        "exists": True,
        "file_count": file_count,
        "size": format_size(size),
        "size_bytes": size,
        "protected": is_protected(path),
        "message": f"Would delete {file_count} files, {format_size(size)} total",
    }


def nuke_zone(zone: str, force: bool = False) -> dict:
    """Aggressively delete zone."""
    if zone not in AGGRESSIVE_ZONES:
        log_action("nuke", zone, "failed", "Unknown zone")
        return {"error": f"Unknown zone: {zone}"}

    zone_config = AGGRESSIVE_ZONES[zone]
    path = zone_config["path"]
    pattern = zone_config.get("pattern")

    if is_protected(path) and not force:
        log_action("nuke", str(path), "blocked", "Protected zone")
        return {
            "error": f"PROTECTED ZONE: {zone}",
            "message": "This folder is protected. Use --force to override (not recommended)",
        }

    if not path.exists():
        log_action("nuke", str(path), "skipped", "Path does not exist")
        return {"zone": zone, "message": "Path does not exist", "deleted": 0}

    if pattern:
        size, file_count = calculate_pattern_size(path, pattern)
    else:
        size, file_count = calculate_size(path)

    try:
        deleted_paths = 0
        if pattern:
            for entry in path.rglob(pattern):
                if is_protected(entry):
                    continue
                if entry.is_dir():
                    shutil.rmtree(entry)
                    deleted_paths += 1
                elif entry.is_file():
                    entry.unlink()
                    deleted_paths += 1
        else:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

        log_action("nuke", str(path), "success", f"Deleted {file_count} files, {format_size(size)}")

        return {
            "zone": zone,
            "success": True,
            "deleted_files": file_count,
            "deleted_size": format_size(size),
            "message": f"✅ Deleted {zone}: {file_count} files, {format_size(size)}",
            "deleted_paths": deleted_paths if pattern else None,
        }

    except Exception as e:
        log_action("nuke", str(path), "failed", str(e))
        return {"zone": zone, "error": str(e), "message": f"❌ Failed to delete {zone}"}


def cleanup_all() -> dict:
    """Nuke all aggressive zones at once."""
    results = []
    total_deleted = 0
    total_size = 0

    for zone in AGGRESSIVE_ZONES.keys():
        result = nuke_zone(zone, force=False)
        results.append(result)
        if "deleted_files" in result:
            total_deleted += result["deleted_files"]
            total_size += result.get("deleted_size_bytes", 0)

    return {
        "operation": "cleanup_all",
        "zones_processed": len(AGGRESSIVE_ZONES),
        "zones_cleaned": len([r for r in results if r.get("success")]),
        "total_files_deleted": total_deleted,
        "total_size_deleted": format_size(total_size),
        "details": results,
    }


def audit_report() -> dict:
    """Show audit trail."""
    if not AUDIT_LOG.exists():
        return {"message": "No audit log found"}

    logs = []
    with open(AUDIT_LOG) as f:
        for line in f:
            logs.append(json.loads(line))

    return {
        "audit_log": str(AUDIT_LOG),
        "total_operations": len(logs),
        "operations": logs[-20:],  # Last 20
    }


def list_zones() -> dict:
    """List all available zones."""
    zones = []
    for zone_name, config in AGGRESSIVE_ZONES.items():
        path = config["path"]
        pattern = config.get("pattern")
        exists = path.exists()
        if exists:
            if pattern:
                size, file_count = calculate_pattern_size(path, pattern)
            else:
                size, file_count = calculate_size(path)
        else:
            size, file_count = 0, 0

        zones.append(
            {
                "zone": zone_name,
                "path": str(path),
                "description": config["description"],
                "exists": exists,
                "files": file_count,
                "size": format_size(size) if exists else "N/A",
            }
        )

    return {"zones": zones}


def _resolve_import_target(base_dir: Path, import_path: str, src_root: Path) -> str | None:
    if not import_path.startswith("."):
        return None

    resolved = (base_dir / import_path).resolve()
    candidates = []

    if resolved.exists():
        candidates.append(resolved)
    else:
        for ext in [".ts", ".tsx", ".js", ".jsx"]:
            if (resolved.with_suffix(ext)).exists():
                candidates.append(resolved.with_suffix(ext))
                break
        if resolved.is_dir():
            for ext in [".ts", ".tsx", ".js", ".jsx"]:
                index_file = resolved / f"index{ext}"
                if index_file.exists():
                    candidates.append(index_file)
                    break

    if not candidates:
        return None

    target = candidates[0]
    try:
        rel = target.relative_to(src_root)
    except ValueError:
        return None

    if target.name.startswith("index."):
        rel = rel.parent
    else:
        rel = rel.with_suffix("")

    return f"@/{rel.as_posix()}"


def refactor_imports(target: Path) -> dict:
    """Refactor relative imports to @/ absolute paths within target."""
    if not target.exists():
        log_action("refactor_imports", str(target), "failed", "Target does not exist")
        return {"error": "Target does not exist", "target": str(target)}

    src_root = target
    changed_files = 0
    total_rewrites = 0

    pattern_from = re.compile(r'(\bfrom\s+)(["\'])([^"\']+)(["\'])')
    pattern_import = re.compile(r'(\bimport\s+)(["\'])([^"\']+)(["\'])')

    for file_path in src_root.rglob("*"):
        if file_path.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        if file_path.is_dir():
            continue

        original = file_path.read_text(encoding="utf-8")
        updated = original

        def _replace(match: re.Match) -> str:
            nonlocal total_rewrites
            prefix, quote_open, import_path, quote_close = match.groups()
            replacement = _resolve_import_target(file_path.parent, import_path, src_root)
            if not replacement:
                return match.group(0)
            total_rewrites += 1
            return f"{prefix}{quote_open}{replacement}{quote_close}"

        updated = pattern_from.sub(_replace, updated)
        updated = pattern_import.sub(_replace, updated)

        if updated != original:
            file_path.write_text(updated, encoding="utf-8")
            changed_files += 1

    log_action(
        "refactor_imports",
        str(target),
        "success",
        f"Updated {changed_files} files, {total_rewrites} imports",
    )

    return {
        "target": str(target),
        "files_updated": changed_files,
        "imports_rewritten": total_rewrites,
        "message": f"✅ Refactored {total_rewrites} imports across {changed_files} files",
    }


def consolidate_services(source: Path, dest: Path) -> dict:
    """Move service files from a legacy source into module service folders."""
    if not source.exists():
        log_action("consolidate_services", str(source), "skipped", "Source does not exist")
        return {"source": str(source), "message": "Source does not exist; nothing to consolidate"}

    dest.mkdir(parents=True, exist_ok=True)

    module_map = {
        "admin": "admin",
        "dashboard": "admin",
        "export": "admin",
        "citizen": "citizen",
        "identity": "identity",
        "biometric": "identity",
        "payment": "pagamentos",
        "finance": "pagamentos",
        "tax": "pagamentos",
        "order": "operations",
        "operation": "operations",
        "meteorologia": "meteorologia",
        "weather": "meteorologia",
    }

    moved = []
    skipped = []

    for file_path in source.rglob("*.ts"):
        name = file_path.stem.lower()
        module = None
        for key, mod in module_map.items():
            if key in name:
                module = mod
                break
        if not module:
            skipped.append(str(file_path))
            continue

        target_dir = dest / module / "services"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file_path.name
        if target_path.exists():
            skipped.append(str(file_path))
            continue

        shutil.move(str(file_path), str(target_path))
        moved.append({"from": str(file_path), "to": str(target_path)})

    log_action(
        "consolidate_services",
        f"{source} -> {dest}",
        "success",
        f"Moved {len(moved)} files, skipped {len(skipped)}",
    )

    return {
        "source": str(source),
        "dest": str(dest),
        "moved": moved,
        "skipped": skipped,
        "message": f"✅ Consolidated {len(moved)} services, skipped {len(skipped)}",
    }


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        # Interactive menu
        print("\n🛡️  AUTONOMOUS FILESYSTEM MANAGER")
        print("=" * 60)
        print("\nAvailable Operations:")
        print("  1. List zones")
        print("  2. Dry-run (preview deletion)")
        print("  3. Nuke zone")
        print("  4. Cleanup all")
        print("  5. Audit trail")
        print("  6. Exit")

        choice = input("\nSelect operation (1-6): ").strip()

        if choice == "1":
            import json

            result = list_zones()
            print(json.dumps(result, indent=2))

        elif choice == "2":
            zone = input("Zone to preview: ").strip()
            import json

            result = dry_run(zone)
            print(json.dumps(result, indent=2))

        elif choice == "3":
            zone = input("Zone to delete: ").strip()
            confirm = input(f"CONFIRM DELETE {zone}? (yes/no): ").strip().lower()
            if confirm == "yes":
                import json

                result = nuke_zone(zone)
                print(json.dumps(result, indent=2))
            else:
                print("Cancelled.")

        elif choice == "4":
            confirm = input("CONFIRM DELETE ALL ZONES? (yes/no): ").strip().lower()
            if confirm == "yes":
                import json

                result = cleanup_all()
                print(json.dumps(result, indent=2))
            else:
                print("Cancelled.")

        elif choice == "5":
            import json

            result = audit_report()
            print(json.dumps(result, indent=2))

        elif choice == "6":
            print("Bye.")
            sys.exit(0)

    elif sys.argv[1] == "--nuke":
        # Direct aggressive deletion
        if len(sys.argv) < 3:
            print("Usage: python super_cleanup.py --nuke <zone>")
            sys.exit(1)

        zone = sys.argv[2]
        force = "--force" in sys.argv

        import json

        result = nuke_zone(zone, force=force)
        print(json.dumps(result, indent=2))

    elif sys.argv[1] == "--cleanup-all":
        # Nuke everything
        import json

        result = cleanup_all()
        print(json.dumps(result, indent=2))

    elif sys.argv[1] == "--list":
        # List zones
        import json

        result = list_zones()
        print(json.dumps(result, indent=2))

    elif sys.argv[1] == "--audit":
        # Show audit
        import json

        result = audit_report()
        print(json.dumps(result, indent=2))

    elif sys.argv[1] == "--refactor-imports":
        if "--target" not in sys.argv:
            print("Usage: python super_cleanup.py --refactor-imports --target <path>")
            sys.exit(1)
        target = Path(sys.argv[sys.argv.index("--target") + 1]).resolve()
        import json

        result = refactor_imports(target)
        print(json.dumps(result, indent=2))

    elif sys.argv[1] == "--consolidate-services":
        if "--source" not in sys.argv or "--dest" not in sys.argv:
            print(
                "Usage: python super_cleanup.py --consolidate-services --source <path> --dest <path>"
            )
            sys.exit(1)
        source = Path(sys.argv[sys.argv.index("--source") + 1]).resolve()
        dest = Path(sys.argv[sys.argv.index("--dest") + 1]).resolve()
        import json

        result = consolidate_services(source, dest)
        print(json.dumps(result, indent=2))

    elif sys.argv[1] == "--dry-run":
        # Preview
        if len(sys.argv) < 3:
            print("Usage: python super_cleanup.py --dry-run <zone>")
            sys.exit(1)

        zone = sys.argv[2]
        import json

        result = dry_run(zone)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {sys.argv[1]}")
        print("\nUsage:")
        print("  python super_cleanup.py                    # Interactive")
        print("  python super_cleanup.py --list              # List zones")
        print("  python super_cleanup.py --dry-run <zone>    # Preview")
        print("  python super_cleanup.py --nuke <zone>       # Delete")
        print("  python super_cleanup.py --cleanup-all        # Delete all")
        print("  python super_cleanup.py --audit              # Audit trail")
        sys.exit(1)
