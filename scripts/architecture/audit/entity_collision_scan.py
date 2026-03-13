#!/usr/bin/env python3
"""Detect entity name collisions across modules."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect duplicated entity names across modules.")
    parser.add_argument("--modules-root", default="apps/backend/app/modules")
    parser.add_argument("--output", default="reports/entity_collision_scan.md")
    args = parser.parse_args()

    modules_root = Path(args.modules_root)
    output = Path(args.output)

    entities: dict[str, list[str]] = defaultdict(list)
    for file in modules_root.rglob("domain/entities/*.py"):
        if file.name == "__init__.py":
            continue
        entities[file.stem].append(file.as_posix())

    collisions = {name: paths for name, paths in entities.items() if len(paths) > 1}

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        f.write("# Entity Collision Scan\n\n")
        f.write(f"- entities_scanned: {len(entities)}\n")
        f.write(f"- collisions: {len(collisions)}\n\n")
        f.write("## Collisions\n")
        if not collisions:
            f.write("- none\n")
        else:
            for entity, paths in sorted(collisions.items()):
                f.write(f"- {entity}\n")
                for path in sorted(paths):
                    f.write(f"  - {path}\n")

    print(f"Entity collision scan generated -> {output.as_posix()}")


if __name__ == "__main__":
    main()
