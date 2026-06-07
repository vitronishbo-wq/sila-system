from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "apps" / "backend" / "app"
MODULES_DIR = APP_DIR / "modules"
REPORT_DIR = ROOT / "reports"

IMPORT_RE = re.compile(
    r"^from\s+(app\.modules\.(?P<mod>[^.]+)\.(?P<path>[^ ]+))\s+import\s+(?P<symbols>.+)$"
)


@dataclass
class ImportChange:
    file: str
    original: str
    updated: str


def load_port_symbols(module_name: str) -> set[str]:
    ports_dir = MODULES_DIR / module_name / "application" / "ports"
    if not ports_dir.exists():
        return set()
    symbols: set[str] = set()
    for py in ports_dir.glob("*.py"):
        try:
            content = py.read_text(encoding="utf-8")
        except Exception:
            continue
        for line in content.splitlines():
            if line.strip().startswith("class "):
                name = line.strip().split()[1].split("(")[0]
                symbols.add(name)
    return symbols


def split_symbols(symbols: str) -> list[str]:
    return [s.strip() for s in symbols.split(",") if s.strip()]


def should_convert_to_ports(module_name: str, imported_symbols: list[str]) -> bool:
    ports = load_port_symbols(module_name)
    if not ports:
        return False
    return all(sym in ports for sym in imported_symbols)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair ACL imports by redirecting to ports when possible."
    )
    parser.add_argument("--apply", action="store_true", help="Apply safe replacements.")
    args = parser.parse_args()

    changes: list[ImportChange] = []
    for py in APP_DIR.rglob("*.py"):
        try:
            content = py.read_text(encoding="utf-8")
        except Exception:
            continue
        updated_lines: list[str] = []
        changed = False
        for line in content.splitlines():
            match = IMPORT_RE.match(line.strip())
            if not match:
                updated_lines.append(line)
                continue
            module_name = match.group("mod")
            path = match.group("path")
            symbols = split_symbols(match.group("symbols"))

            # Replace core.application.ports -> application.ports
            if path.startswith("core.application.ports"):
                new_path = path.replace("core.application.ports", "application.ports")
                new_line = line.replace(
                    match.group(0).split()[1], f"apps.backend.app.modules.{module_name}.{new_path}"
                )
                changes.append(ImportChange(str(py), line, new_line))
                updated_lines.append(new_line)
                changed = True
                continue

            # Replace core.application.* -> application.*
            if path.startswith("core.application."):
                new_path = path.replace("core.application.", "application.")
                new_line = line.replace(
                    match.group(0).split()[1], f"apps.backend.app.modules.{module_name}.{new_path}"
                )
                changes.append(ImportChange(str(py), line, new_line))
                updated_lines.append(new_line)
                changed = True
                continue

            # Replace core.domain.* -> domain.*
            if path.startswith("core.domain."):
                new_path = path.replace("core.domain.", "domain.")
                new_line = line.replace(
                    match.group(0).split()[1], f"apps.backend.app.modules.{module_name}.{new_path}"
                )
                changes.append(ImportChange(str(py), line, new_line))
                updated_lines.append(new_line)
                changed = True
                continue

            # Replace core.api.* -> api.*
            if path.startswith("core.api."):
                new_path = path.replace("core.api.", "api.")
                new_line = line.replace(
                    match.group(0).split()[1], f"apps.backend.app.modules.{module_name}.{new_path}"
                )
                changes.append(ImportChange(str(py), line, new_line))
                updated_lines.append(new_line)
                changed = True
                continue

            # Replace core.infrastructure.* -> infrastructure.*
            if path.startswith("core.infrastructure."):
                new_path = path.replace("core.infrastructure.", "infrastructure.")
                new_line = line.replace(
                    match.group(0).split()[1], f"apps.backend.app.modules.{module_name}.{new_path}"
                )
                changes.append(ImportChange(str(py), line, new_line))
                updated_lines.append(new_line)
                changed = True
                continue

            # Replace core.domain.enums -> domain.enums
            if path.startswith("core.domain.enums"):
                new_path = path.replace("core.domain.enums", "domain.enums")
                new_line = line.replace(
                    match.group(0).split()[1], f"apps.backend.app.modules.{module_name}.{new_path}"
                )
                changes.append(ImportChange(str(py), line, new_line))
                updated_lines.append(new_line)
                changed = True
                continue

            # Replace infrastructure.models -> application.ports when safe
            if path.startswith("core.infrastructure.models") or path.startswith(
                "infrastructure.models"
            ):
                if should_convert_to_ports(module_name, symbols):
                    new_path = "application.ports"
                    new_line = line.replace(
                        match.group(0).split()[1], f"apps.backend.app.modules.{module_name}.{new_path}"
                    )
                    changes.append(ImportChange(str(py), line, new_line))
                    updated_lines.append(new_line)
                    changed = True
                    continue

            updated_lines.append(line)

        if args.apply and changed:
            py.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"repair_acl_imports_{stamp}.json"
    json_path.write_text(json.dumps([asdict(c) for c in changes], indent=2), encoding="utf-8")
    md_path = REPORT_DIR / f"repair_acl_imports_{stamp}.md"
    lines = [
        "# Repair ACL Imports - Relatorio",
        "",
        f"- Timestamp (UTC): {datetime.utcnow().isoformat()}",
        f"- Import changes: {len(changes)}",
        "",
        "| Arquivo | Antes | Depois |",
        "| --- | --- | --- |",
    ]
    for c in changes:
        lines.append(f"| {c.file} | {c.original} | {c.updated} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
