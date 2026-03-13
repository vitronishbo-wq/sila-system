#!/usr/bin/env python3
"""Compile module.yaml manifests into a contract graph artifact."""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
from typing import Any

import yaml


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def _validate_manifest(path: Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    name = data.get("name")
    if not isinstance(name, str) or not name:
        errors.append("missing/invalid 'name'")
    if data.get("type") not in {"macro_domain", "sub_domain"}:
        errors.append("missing/invalid 'type' (expected macro_domain or sub_domain)")
    exposes = data.get("exposes")
    if not isinstance(exposes, dict):
        errors.append("missing/invalid 'exposes'")
    requires = data.get("requires")
    if not isinstance(requires, dict):
        errors.append("missing/invalid 'requires'")

    if isinstance(exposes, dict):
        for key in ("api_routers", "public_models", "events_published"):
            if not isinstance(exposes.get(key, []), list):
                errors.append(f"exposes.{key} must be a list")
    if isinstance(requires, dict):
        for key in ("domains", "core_services"):
            if not isinstance(requires.get(key, []), list):
                errors.append(f"requires.{key} must be a list")

    if not isinstance(data.get("subdomains", []), list):
        errors.append("subdomains must be a list")

    if errors:
        prefix = path.as_posix()
        return [f"{prefix}: {msg}" for msg in errors]
    return []


def load_manifests(manifest_glob: str = "apps/backend/app/modules/**/module.yaml") -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    validation_errors: list[str] = []
    for file_path in sorted(glob.glob(manifest_glob, recursive=True)):
        path = Path(file_path)
        with path.open(encoding="utf-8") as fh:
            payload = yaml.safe_load(fh) or {}
        if not isinstance(payload, dict):
            validation_errors.append(f"{path.as_posix()}: manifest root must be a mapping")
            continue
        validation_errors.extend(_validate_manifest(path, payload))
        name = payload.get("name")
        if isinstance(name, str) and name:
            key = name
            if key in manifests:
                modules_root = Path("apps/backend/app/modules")
                try:
                    relative = path.parent.relative_to(modules_root).as_posix()
                except ValueError:
                    relative = path.parent.as_posix()
                key = relative.replace("/", ".")
            manifests[key] = payload

    if validation_errors:
        message = "\n".join(validation_errors)
        raise ValueError(f"Manifest validation failed:\n{message}")
    return manifests


def compile_graph(manifests: dict[str, dict[str, Any]]) -> dict[str, Any]:
    nodes = sorted(manifests.keys())
    edges: list[dict[str, str]] = []
    for source in nodes:
        manifest = manifests[source]
        requires = manifest.get("requires", {})
        domains = _as_list(requires.get("domains") if isinstance(requires, dict) else [])
        for target in sorted(str(dep) for dep in domains if isinstance(dep, str) and dep and dep != source):
            edges.append({"from": source, "to": target})
    return {"nodes": nodes, "edges": edges}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile module manifests into a dependency graph.")
    parser.add_argument(
        "--manifest-glob",
        default="apps/backend/app/modules/**/module.yaml",
        help="Glob pattern for module manifests.",
    )
    parser.add_argument(
        "--output",
        default="reports/module_manifest_graph.json",
        help="Output JSON file for compiled manifest graph.",
    )
    args = parser.parse_args()

    manifests = load_manifests(args.manifest_glob)
    graph = compile_graph(manifests)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Generated: {output_path}")
    print(f"Manifests: {len(manifests)}")
    print(f"Edges: {len(graph['edges'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
