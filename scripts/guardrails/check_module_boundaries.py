#!/usr/bin/env python3
"""Detect cross-module imports under apps/backend/app/modules.

Rules:
- Allow imports from `app.shared.*`.
- Flag imports from other `app.modules.<module>` by default.
- Support JSON allowlist for approved cross-module dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FROM_MODULE_RE = re.compile(r"^\s*from\s+app\.modules\.([a-zA-Z0-9_]+)\b")
IMPORT_MODULE_RE = re.compile(r"^\s*import\s+app\.modules\.([a-zA-Z0-9_]+)\b")
FROM_SHARED_RE = re.compile(r"^\s*from\s+app\.shared\b")
IMPORT_SHARED_RE = re.compile(r"^\s*import\s+app\.shared\b")


def collect_modules(modules_root: Path) -> set[str]:
    return {p.name for p in modules_root.iterdir() if p.is_dir() and p.name != "__pycache__"}


def load_allowlist(path: Path | None) -> set[str]:
    if path is None or not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    items = data.get("allowed_cross_imports", [])
    return {str(item) for item in items if isinstance(item, str)}


def scan_module_file(
    py_file: Path,
    current_module: str,
    module_set: set[str],
    allowed_cross_imports: set[str],
    dependencies: dict[str, set[str]],
    import_counts: dict[str, int],
) -> list[str]:
    violations: list[str] = []
    try:
        text = py_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return violations

    for i, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("#"):
            continue

        if FROM_SHARED_RE.search(line) or IMPORT_SHARED_RE.search(line):
            continue

        match = FROM_MODULE_RE.search(line) or IMPORT_MODULE_RE.search(line)
        if not match:
            continue

        imported_module = match.group(1)
        if imported_module in module_set and imported_module != current_module:
            dependencies.setdefault(current_module, set()).add(imported_module)
            import_counts[current_module] = import_counts.get(current_module, 0) + 1
            allow_key = f"{current_module}->{imported_module}"
            if allow_key in allowed_cross_imports:
                continue
            violations.append(f"{py_file}:{i} imports app.modules.{imported_module}")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check cross-module imports in backend modules.",
    )
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Path to modules root",
    )
    parser.add_argument(
        "--fail-on-violation",
        action="store_true",
        help="Exit with code 1 if violations are found.",
    )
    parser.add_argument(
        "--allowlist",
        default="scripts/guardrails/allowlists/module_boundaries.json",
        help="JSON allowlist for approved cross-module dependencies.",
    )
    parser.add_argument(
        "--max-dependencies-warning",
        type=int,
        default=10,
        help="Warn when a module imports more than this number of other modules.",
    )
    args = parser.parse_args()

    modules_root = Path(args.modules_root)
    if not modules_root.exists():
        print(f"Modules root not found: {modules_root}")
        return 2

    module_set = collect_modules(modules_root)
    violations: list[str] = []
    dependencies: dict[str, set[str]] = {}
    import_counts: dict[str, int] = {}
    allowed_cross_imports = load_allowlist(Path(args.allowlist))

    for module in sorted(module_set):
        module_path = modules_root / module
        for py_file in module_path.rglob("*.py"):
            violations.extend(
                scan_module_file(
                    py_file=py_file,
                    current_module=module,
                    module_set=module_set,
                    allowed_cross_imports=allowed_cross_imports,
                    dependencies=dependencies,
                    import_counts=import_counts,
                )
            )

    print(f"Scanned modules: {len(module_set)}")
    print(f"Cross-module imports detected: {len(violations)}")
    for item in violations:
        print(f" - {item}")

    print("\nModule dependency summary (distinct module deps):")
    for module in sorted(module_set):
        dep_count = len(dependencies.get(module, set()))
        total_imports = import_counts.get(module, 0)
        print(f" - {module}: {dep_count} deps ({total_imports} import lines)")

    high_coupling = sorted(
        [
            (module, len(targets))
            for module, targets in dependencies.items()
            if len(targets) > args.max_dependencies_warning
        ],
        key=lambda item: item[1],
        reverse=True,
    )
    print(
        f"\nModules above coupling threshold ({args.max_dependencies_warning}): "
        f"{len(high_coupling)}"
    )
    for module, dep_count in high_coupling:
        print(f" - {module}: {dep_count} deps")

    if args.fail_on_violation and violations:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
