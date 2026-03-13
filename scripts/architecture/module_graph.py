"""Dependency graph utilities for module-level architecture analysis."""

from __future__ import annotations

from collections import Counter

try:
    from .scanner import ImportEdge, ModuleScan
except ImportError:
    from scanner import ImportEdge, ModuleScan  # type: ignore


def build_dependency_graph(scans: dict[str, ModuleScan], edges: list[ImportEdge]) -> dict:
    inbound_counter: Counter[str] = Counter()
    outbound_counter: Counter[str] = Counter()

    for edge in edges:
        outbound_counter[edge.source] += edge.count
        inbound_counter[edge.target] += edge.count

    nodes: list[dict] = []
    for module_name in sorted(scans.keys()):
        nodes.append(
            {
                "id": module_name,
                "path": scans[module_name].path,
                "files_scanned": scans[module_name].files_scanned,
                "outbound_imports": outbound_counter[module_name],
                "inbound_imports": inbound_counter[module_name],
                "distinct_outbound_targets": len(scans[module_name].imports_out),
            }
        )

    serialized_edges = [
        {
            "source": edge.source,
            "target": edge.target,
            "count": edge.count,
            "evidence": edge.evidence,
        }
        for edge in sorted(edges, key=lambda item: (-item.count, item.source, item.target))
    ]

    hotspots_outbound = sorted(
        (
            {
                "module": name,
                "total_outbound_imports": outbound_counter[name],
                "distinct_targets": len(scans[name].imports_out),
                "top_targets": sorted(
                    scans[name].imports_out.items(),
                    key=lambda item: (-item[1], item[0]),
                )[:5],
            }
            for name in scans
            if outbound_counter[name] > 0
        ),
        key=lambda item: (-item["total_outbound_imports"], item["module"]),
    )[:20]

    hotspots_inbound = sorted(
        (
            {"module": name, "total_inbound_imports": count}
            for name, count in inbound_counter.items()
            if count > 0
        ),
        key=lambda item: (-item["total_inbound_imports"], item["module"]),
    )[:20]

    return {
        "summary": {
            "modules": len(scans),
            "edges_distinct": len(serialized_edges),
            "edges_total": sum(edge.count for edge in edges),
        },
        "nodes": nodes,
        "edges": serialized_edges,
        "hotspots": {
            "outbound": hotspots_outbound,
            "inbound": hotspots_inbound,
        },
    }
