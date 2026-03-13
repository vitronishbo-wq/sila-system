#!/usr/bin/env python3
"""Run architecture scanner and generate enterprise reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

if __package__ in (None, ""):
    import sys

    THIS_DIR = Path(__file__).resolve().parent
    if str(THIS_DIR) not in sys.path:
        sys.path.insert(0, str(THIS_DIR))

    from module_graph import build_dependency_graph  # type: ignore
    from report_generator import (  # type: ignore
        write_dependency_graph_report,
        write_domain_overlap_markdown,
        write_module_map_report,
    )
    from scanner import collect_edges, scan_modules  # type: ignore
    from similarity import compute_similarity_candidates  # type: ignore
else:
    from .module_graph import build_dependency_graph
    from .report_generator import (
        write_dependency_graph_report,
        write_domain_overlap_markdown,
        write_module_map_report,
    )
    from .scanner import collect_edges, scan_modules
    from .similarity import compute_similarity_candidates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run architecture analysis for SILA modules.")
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Modules root to analyze.",
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory where reports will be generated.",
    )
    parser.add_argument(
        "--top-overlap",
        type=int,
        default=30,
        help="Maximum number of overlap pairs in markdown report.",
    )
    parser.add_argument(
        "--min-similarity",
        type=float,
        default=0.60,
        help="Minimum similarity threshold for overlap candidates.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    modules_root = Path(args.modules_root).resolve()
    reports_dir = Path(args.reports_dir).resolve()

    if not modules_root.is_dir():
        raise SystemExit(f"Modules root not found: {modules_root}")

    scans = scan_modules(modules_root)
    edges = collect_edges(scans)
    graph_payload = build_dependency_graph(scans, edges)
    candidates = compute_similarity_candidates(scans, min_score=args.min_similarity)

    module_map_out = reports_dir / "module_map.json"
    dependency_graph_out = reports_dir / "dependency_graph.json"
    overlap_md_out = reports_dir / "domain_overlap_report.md"

    write_module_map_report(scans, module_map_out, modules_root)
    write_dependency_graph_report(graph_payload, dependency_graph_out)
    write_domain_overlap_markdown(
        scans=scans,
        candidates=candidates,
        edges=edges,
        output=overlap_md_out,
        top_n=args.top_overlap,
    )

    summary = {
        "modules": len(scans),
        "edges_distinct": len(edges),
        "edges_total": sum(edge.count for edge in edges),
        "overlap_candidates": len(candidates),
        "reports": {
            "module_map": str(module_map_out),
            "dependency_graph": str(dependency_graph_out),
            "domain_overlap": str(overlap_md_out),
        },
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
