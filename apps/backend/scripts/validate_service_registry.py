#!/usr/bin/env python3
"""Validate module.yaml registry schema across modules."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("PyYAML required. Install with `pip install pyyaml`.") from exc


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
MODULES_ROOT = BACKEND_ROOT / "app" / "modules"


def _validate_service(service: dict[str, Any]) -> list[str]:
    errors = []
    service_id = service.get("id") or service.get("code")
    if not service_id:
        errors.append("missing id")
    if not service.get("name"):
        errors.append("missing name")
    sla = service.get("sla") or {}
    if sla:
        if not isinstance(sla.get("days"), int) or sla.get("days", 0) <= 0:
            errors.append("sla.days must be > 0")
    pricing = service.get("pricing") or {}
    if pricing:
        if pricing.get("amount") is None or float(pricing.get("amount", 0)) < 0:
            errors.append("pricing.amount must be >= 0")
    workflow = service.get("workflow") or {}
    steps = workflow.get("steps") or []
    if not steps:
        errors.append("workflow.steps required")
    form = service.get("form") or {}
    if not form.get("schema"):
        errors.append("form.schema required")
    return errors


def _validate_module(module_path: Path) -> dict[str, Any]:
    data = {}
    with module_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    module_code = data.get("code") or data.get("module")
    errors = []
    if not module_code:
        errors.append("module code missing")
    if not data.get("name"):
        errors.append("module name missing")
    if not data.get("version"):
        errors.append("module version missing")
    if not data.get("last_updated"):
        errors.append("module last_updated missing")

    services = data.get("services") or []
    service_errors = {}
    for idx, service in enumerate(services):
        svc_errors = _validate_service(service)
        if svc_errors:
            service_errors[service.get("id") or service.get("code") or f"index_{idx}"] = svc_errors

    return {
        "module": module_code or module_path.parent.name,
        "errors": errors,
        "service_errors": service_errors,
        "service_count": len(services),
    }


def validate(modules_root: Path) -> dict[str, Any]:
    module_reports = []
    seen_codes: set[str] = set()
    duplicate_codes: set[str] = set()
    total_services = 0

    for module_path in sorted(modules_root.glob("*/module.yaml")):
        report = _validate_module(module_path)
        module_reports.append(report)
        total_services += report["service_count"]
        with module_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        for service in data.get("services") or []:
            code = (service.get("id") or service.get("code") or "").upper()
            if not code:
                continue
            if code in seen_codes:
                duplicate_codes.add(code)
            else:
                seen_codes.add(code)

    errors = [r for r in module_reports if r["errors"] or r["service_errors"]]
    return {
        "modules_checked": len(module_reports),
        "total_services": total_services,
        "duplicate_codes": sorted(duplicate_codes),
        "module_errors": errors,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate module.yaml service registry")
    parser.add_argument("--modules-root", default=str(MODULES_ROOT), help="Modules root")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    report = validate(Path(args.modules_root))
    timestamp = datetime.utcnow().isoformat()
    print(f"[{timestamp}] modules={report['modules_checked']} services={report['total_services']}")
    if report["duplicate_codes"]:
        print(f"Duplicate service codes: {', '.join(report['duplicate_codes'])}")
    if report["module_errors"]:
        print("Validation errors:")
        for module in report["module_errors"]:
            if module["errors"]:
                print(f"- {module['module']}: {', '.join(module['errors'])}")
            for svc, errs in module["service_errors"].items():
                print(f"  - {svc}: {', '.join(errs)}")
        raise SystemExit(1)
    print("Registry validation OK.")


if __name__ == "__main__":
    main()
