#!/usr/bin/env python3
"""Guardrail: validates module dependency cycles against policy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def load_structured(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text) or {}
    return json.loads(text) or {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check dependency cycles.")
    parser.add_argument("--observed-json", default="reports/module_dependency_graph.json")
    parser.add_argument(
        "--policy-yaml",
        default="docs/architecture/domain_dependency_policy.yaml",
    )
    args = parser.parse_args()

    observed = load_structured(Path(args.observed_json))
    policy = load_structured(Path(args.policy_yaml))
    if not observed:
        raise SystemExit(f"Missing observed graph: {args.observed_json}")
    if not policy:
        raise SystemExit(f"Missing policy file: {args.policy_yaml}")

    allow_circular = bool(policy.get("rules", {}).get("allow_circular_dependencies", False))
    cycles = [c for c in observed.get("cycles", []) if isinstance(c, list)]

    if allow_circular:
        print("✅ Cycle check skipped by policy (allow_circular_dependencies=true).")
        return 0

    if cycles:
        print(f"❌ Detected {len(cycles)} cycle group(s).")
        for cycle in cycles[:20]:
            print(" - " + " -> ".join(str(node) for node in cycle))
        return 1

    print("✅ No circular dependencies detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
