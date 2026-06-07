import importlib
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI


def _safe_prefix(segments: tuple[str, ...]) -> str:
    cleaned = [segment.strip("/") for segment in segments if segment and segment.strip("/")]
    if not cleaned:
        return ""
    return "/" + "/".join(cleaned)


def _to_import_path(base_path: Path, router_file: Path) -> str:
    rel = router_file.relative_to(base_path.parent)
    return f"apps.backend.app.{rel.with_suffix('').as_posix().replace('/', '.')}"


def discover_and_register_routers(app: FastAPI) -> dict[str, list[dict[str, Any]]]:
    base_path = (Path(__file__).resolve().parents[2] / "modules").resolve()
    report: dict[str, list[dict[str, Any]]] = {"loaded": [], "skipped": [], "failed": []}
    for path in sorted(base_path.rglob("api/router.py")):
        rel = path.relative_to(base_path)
        parts = rel.parts
        domain_parts = parts[:-2]
        if len(parts) < 3 or parts[-2] != "api" or parts[-1] != "router.py":
            report["skipped"].append({"file": rel.as_posix(), "reason": "invalid_router_location"})
            continue
        if len(domain_parts) < 2:
            report["skipped"].append({"file": rel.as_posix(), "reason": "depth_below_threshold"})
            continue
        prefix = _safe_prefix(domain_parts)
        module_path = _to_import_path(base_path, path)
        tag = domain_parts[0]
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            report["failed"].append(
                {
                    "file": rel.as_posix(),
                    "module": module_path,
                    "prefix": prefix,
                    "error": f"{e.__class__.__name__}: {e}",
                }
            )
            continue
        router = getattr(module, "router", None)
        if not isinstance(router, APIRouter):
            report["skipped"].append(
                {
                    "file": rel.as_posix(),
                    "module": module_path,
                    "reason": "router_missing_or_invalid",
                }
            )
            continue
        try:
            app.include_router(router, prefix=prefix, tags=[tag])
            report["loaded"].append(
                {"file": rel.as_posix(), "module": module_path, "prefix": prefix, "tag": tag}
            )
        except Exception as e:
            report["failed"].append(
                {
                    "file": rel.as_posix(),
                    "module": module_path,
                    "prefix": prefix,
                    "error": f"{e.__class__.__name__}: {e}",
                }
            )
    return report
