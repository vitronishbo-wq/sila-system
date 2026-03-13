#!/usr/bin/env python3
"""Generate architecture map report from module registry and dependency graph."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.module_registry import (
    DOMAIN_INDEX,
    find_bootstrap_misalignment,
    find_unregistered_modules,
    iter_bootstrap_modules,
)


def load_dependency_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def render_report(
    dependency_payload: dict | None,
    modules_root: Path,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    unregistered = find_unregistered_modules(modules_root)
    misaligned = find_bootstrap_misalignment(modules_root)
    api_bootstrap = [spec.name for spec in iter_bootstrap_modules("api")]
    main_bootstrap = [spec.name for spec in iter_bootstrap_modules("main")]

    lines: list[str] = []
    lines.append("# Architecture Map")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append("- Source of truth: `app/core/module_registry.py`")
    lines.append("")
    lines.append("## Federation Domains")
    lines.append("")
    for domain in (
        "governance",
        "economy",
        "social",
        "infrastructure",
        "environment",
        "security",
        "identity",
        "core_system",
    ):
        members = DOMAIN_INDEX.get(domain, tuple())
        lines.append(f"### {domain}")
        lines.append("")
        if members:
            lines.append(", ".join(f"`{name}`" for name in members))
        else:
            lines.append("- No modules.")
        lines.append("")

    lines.append("## Bootstrap Scopes")
    lines.append("")
    lines.append("### API Scope")
    lines.append("")
    lines.append(", ".join(f"`{name}`" for name in sorted(api_bootstrap)) or "-")
    lines.append("")
    lines.append("### Main Scope")
    lines.append("")
    lines.append(", ".join(f"`{name}`" for name in sorted(main_bootstrap)) or "-")
    lines.append("")

    lines.append("## Registry Integrity")
    lines.append("")
    lines.append(f"- Unregistered module folders: **{len(unregistered)}**")
    if unregistered:
        lines.append(f"  - {', '.join(f'`{name}`' for name in unregistered)}")
    lines.append(f"- Bootstrap misalignment (registered but missing on disk): **{len(misaligned)}**")
    if misaligned:
        lines.append(f"  - {', '.join(f'`{name}`' for name in misaligned)}")
    lines.append("")

    lines.append("## Dependency Snapshot")
    lines.append("")
    if dependency_payload:
        lines.append(f"- Distinct edges: **{len(dependency_payload.get('edges', []))}**")
        lines.append(f"- Circular groups: **{len(dependency_payload.get('cycles', []))}**")
    else:
        lines.append("- Dependency graph JSON not found. Run `scripts/module_dependency_analysis.py`.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate architecture map report.")
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Path to modules root.",
    )
    parser.add_argument(
        "--dependency-json",
        default="reports/module_dependency_graph.json",
        help="Path to dependency graph json.",
    )
    parser.add_argument(
        "--output",
        default="reports/architecture_map.md",
        help="Output markdown path.",
    )
    args = parser.parse_args()

    modules_root = Path(args.modules_root).resolve()
    dep_json = Path(args.dependency_json).resolve()
    output = Path(args.output).resolve()

    payload = load_dependency_json(dep_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(payload, modules_root), encoding="utf-8")
    print(f"Generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
