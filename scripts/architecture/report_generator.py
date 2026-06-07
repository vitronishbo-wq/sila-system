"""Report writers for architecture analysis outputs."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

try:
    from .scanner import ImportEdge, ModuleScan
except ImportError:
    from scanner import ImportEdge, ModuleScan  # type: ignore


def write_module_map_report(scans: dict[str, ModuleScan], output: Path, modules_root: Path) -> None:
    modules = [scan.to_dict() for _, scan in sorted(scans.items())]
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "scope": str(modules_root),
        "summary": {
            "modules": len(scans),
            "files_scanned": sum(scan.files_scanned for scan in scans.values()),
        },
        "modules": modules,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_dependency_graph_report(graph_payload: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph_payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_domain_overlap_markdown(
    scans: dict[str, ModuleScan],
    candidates: list[dict],
    edges: list[ImportEdge],
    output: Path,
    top_n: int = 30,
) -> None:
    lines: list[str] = []
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")

    lines.append("# Domain Overlap Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append(f"- Modules scanned: **{len(scans)}**")
    lines.append(f"- Dependency edges: **{len(edges)}**")
    lines.append("")
    lines.append("## Potential Domain Conflicts")
    lines.append("")

    if not candidates:
        lines.append("No high-confidence overlap candidates detected by current heuristics.")
    else:
        lines.append("| Pair | Similarity | Suggestion | Cross-imports |")
        lines.append("| --- | ---: | --- | ---: |")
        for item in candidates[:top_n]:
            lines.append(
                f"| `{item['left']}` <-> `{item['right']}` | {item['similarity_score']} | "
                f"{item['suggestion']} | {item['cross_imports']} |"
            )

    lines.append("")
    lines.append("## Dependency Hotspots")
    lines.append("")

    outbound = sorted(
        (
            (name, sum(scan.imports_out.values()), len(scan.imports_out))
            for name, scan in scans.items()
            if sum(scan.imports_out.values()) > 0
        ),
        key=lambda item: (-item[1], -item[2], item[0]),
    )[:20]

    if not outbound:
        lines.append("No cross-module import hotspots detected.")
    else:
        lines.append("| Module | Total outbound imports | Distinct targets |")
        lines.append("| --- | ---: | ---: |")
        for module, total, distinct in outbound:
            lines.append(f"| `{module}` | {total} | {distinct} |")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Analysis-only scanner: no source files were modified.")
    lines.append("- Similarity is heuristic and should be validated with business ownership.")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
