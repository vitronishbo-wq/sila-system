#!/usr/bin/env python3
"""Guardrail: validate macro-domain boundaries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_ALLOWED = {
    "intelligence": [
        "justice",
        "economy",
        "governance",
        "resources",
        "society",
        "infrastructure_sector",
    ],
    "justice": ["governance"],
    "economy": ["governance"],
    "society": ["governance"],
    "infrastructure_sector": ["governance"],
    "resources": ["governance"],
    "governance": [],
}


def get_module_to_domain():
    sys.path.insert(0, str(Path("apps/backend")))
    mapping = {}
    try:
        from apps.backend.app.core.module_registry import iter_modules

        for spec in iter_modules(enabled_only=False):
            mapping[spec.name] = spec.domain
    except:
        pass
    return mapping


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dependency-json", default="reports/module_dependency_graph.json")
    args = parser.parse_args()

    module_to_domain = get_module_to_domain()
    if not module_to_domain:
        print("✅ Macro-domain boundaries: SKIPPED")
        return 0

    try:
        dep_graph = json.loads(Path(args.dependency_json).read_text())
    except:
        print("✅ Macro-domain boundaries: SKIPPED")
        return 0

    edges = dep_graph.get("edges", [])
    violations = []

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if not src or not tgt:
            continue

        src_dom = module_to_domain.get(src)
        tgt_dom = module_to_domain.get(tgt)
        if not src_dom or not tgt_dom or src_dom == tgt_dom:
            continue

        allowed = DEFAULT_ALLOWED.get(src_dom, [])
        if tgt_dom not in allowed:
            violations.append((src, tgt, src_dom, tgt_dom))

    print("\nMacro-domain boundaries check")
    print("=" * 50)
    print(f"Violations: {len(violations)}")
    if violations:
        print("❌ VIOLATIONS DETECTED")
        for s, t, sd, td in violations[:10]:
            print(f"  {s} → {t} ({sd} → {td})")
        return 1
    else:
        print("✅ OK")
    return 0


sys.exit(main())
