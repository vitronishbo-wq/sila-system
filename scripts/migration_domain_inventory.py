#!/usr/bin/env python3
"""Generate migration inventory grouped by inferred domain."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

DOMAIN_TOKENS = (
    "governance",
    "economy",
    "social",
    "infrastructure",
    "environment",
    "security",
    "identity",
    "core_system",
    "agricultura",
    "saude",
    "educacao",
    "financas",
    "taxpayer",
    "justica",
    "juventude",
    "telecomunicacoes",
    "obras_publicas",
    "estatistica",
    "statistics",
)


def infer_domain(filename: str) -> str:
    lower = filename.lower()
    for token in DOMAIN_TOKENS:
        if token in lower:
            return token
    return "unclassified"


def collect(paths: tuple[Path, ...]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for base in paths:
        if not base.exists():
            continue
        for file in sorted(base.glob("*.py")):
            if file.name.startswith("__"):
                continue
            group = infer_domain(file.name)
            grouped[group].append(file.as_posix())
    return grouped


def render(grouped: dict[str, list[str]]) -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
    total = sum(len(items) for items in grouped.values())

    lines: list[str] = []
    lines.append("# Migration Domain Inventory")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append(f"- Total migration files: **{total}**")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Group | Count |")
    lines.append("| --- | ---: |")
    for group in sorted(grouped):
        lines.append(f"| `{group}` | {len(grouped[group])} |")
    lines.append("")

    for group in sorted(grouped):
        lines.append(f"## {group}")
        lines.append("")
        for item in grouped[group]:
            lines.append(f"- `{item}`")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate migration domain inventory.")
    parser.add_argument(
        "--versions",
        action="append",
        default=[
            "apps/backend/alembic/versions",
            "alembic/versions",
            "migrations/versions",
        ],
        help="Versions folder path (repeatable).",
    )
    parser.add_argument(
        "--output",
        default="reports/migration_domain_inventory.md",
        help="Output markdown path.",
    )
    args = parser.parse_args()

    versions = tuple(Path(item).resolve() for item in args.versions)
    grouped = collect(versions)

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(grouped), encoding="utf-8")
    print(f"Generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
