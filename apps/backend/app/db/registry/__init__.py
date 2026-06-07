"""Auto-discovery registry for SQLAlchemy models."""

from __future__ import annotations

import importlib
import json
import os
import re
import warnings
from collections.abc import Iterable
from pathlib import Path

from apps.backend.app.core.db import Base
from sqlalchemy.orm import configure_mappers

APP_ROOT = Path(__file__).resolve().parents[2]
SEARCH_ROOTS = [
    APP_ROOT / "modules",
    APP_ROOT / "core",
]
EXCLUDE_DIRS = {
    "__pycache__",
    "_deprecated",
    "tests",
    "alembic",
    "migrations",
}
MODEL_CLASS_PATTERN = re.compile(r"class\s+\w+\s*\([^)]*\bBase\b[^)]*\):")
CACHE_PATH = Path(
    os.getenv(
        "SILA_REGISTRY_CACHE_PATH",
        APP_ROOT / "db" / "registry" / ".cache" / "registry_modules.json",
    )
)
CACHE_VERSION = 1


def _should_skip(path: Path) -> bool:
    if path.name == "__init__.py":
        return True
    return any(part in EXCLUDE_DIRS for part in path.parts)


def _is_candidate(path: Path) -> bool:
    if path.name.endswith("_model.py") or path.name == "models.py":
        return True
    if "models" in path.parts or "orm" in path.parts:
        return True
    if "bridges" in path.parts:
        return True
    return False


def _looks_like_model_module(path: Path) -> bool:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return bool(MODEL_CLASS_PATTERN.search(content))


def _module_name_from_path(path: Path, root: Path) -> str:
    relative = path.relative_to(root).with_suffix("")
    return "apps.backend.app." + ".".join(relative.parts)


def _latest_source_mtime() -> float:
    latest = 0.0
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if _should_skip(path):
                continue
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if mtime > latest:
                latest = mtime
    return latest


def _load_cache(latest_mtime: float) -> list[str] | None:
    if not CACHE_PATH.exists():
        return None
    try:
        payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if payload.get("version") != CACHE_VERSION:
        return None
    cached_mtime = payload.get("latest_mtime")
    module_names = payload.get("module_names")
    if not isinstance(cached_mtime, (int, float)):
        return None
    if cached_mtime < latest_mtime:
        return None
    if not isinstance(module_names, list) or not all(
        isinstance(name, str) for name in module_names
    ):
        return None
    return module_names


def _write_cache(module_names: list[str], latest_mtime: float) -> None:
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": CACHE_VERSION,
            "latest_mtime": latest_mtime,
            "module_names": module_names,
        }
        CACHE_PATH.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    except OSError:
        return


def discover_model_modules() -> list[str]:
    latest_mtime = _latest_source_mtime()
    cached = _load_cache(latest_mtime)
    if cached is not None:
        return cached
    module_names: set[str] = set()
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if _should_skip(path):
                continue
            if not _is_candidate(path):
                continue
            if not _looks_like_model_module(path):
                continue
            module_names.add(_module_name_from_path(path, APP_ROOT))
    discovered = sorted(module_names)
    _write_cache(discovered, latest_mtime)
    return discovered


def import_model_modules(module_names: Iterable[str]) -> list[str]:
    imported_modules: list[str] = []
    errors: dict[str, Exception] = {}
    for module_name in module_names:
        try:
            # If an equivalent module exists under the alternate namespace,
            # ensure sys.modules maps the desired name to the already-loaded
            # module object to avoid duplicate imports/classes.
            try:
                import sys

                if module_name.startswith("apps.backend.app."):
                    alt = "apps.backend.app." + module_name[len("apps.backend.app."):]
                    if alt in sys.modules and module_name not in sys.modules:
                        sys.modules[module_name] = sys.modules[alt]
                elif module_name == "apps.backend.app":
                    if "app" in sys.modules and module_name not in sys.modules:
                        sys.modules[module_name] = sys.modules["app"]
                elif module_name.startswith("apps.backend.app."):
                    alt = "apps.backend.app." + module_name[len("apps.backend.app."):]
                    if alt in sys.modules and module_name not in sys.modules:
                        sys.modules[module_name] = sys.modules[alt]
            except Exception:
                pass

            module = importlib.import_module(module_name)
            # Register alias so imports using the alternate namespace "apps.backend.app.*"
            # resolve to the same module object and avoid duplicate classes.
            try:
                if module_name.startswith("apps.backend.app."):
                    alias = "apps.backend.app." + module_name[len("apps.backend.app."):]
                    import sys
                    sys.modules.setdefault(alias, module)
                elif module_name == "apps.backend.app":
                    import sys
                    sys.modules.setdefault("app", module)
            except Exception:
                # Do not fail module import due to aliasing issues
                pass
            imported_modules.append(module_name)
        except Exception as exc:
            errors[module_name] = exc
    if errors:
        warnings.warn(
            (
                "The model registry skipped some modules because they failed to import:\n"
                + "\n".join(f"{name}: {type(exc).__name__}: {exc}" for name, exc in errors.items())
            ),
            stacklevel=2,
        )
    return imported_modules


def collect_models(module_names: Iterable[str]) -> list[type]:
    models: list[type] = []
    seen: set[type] = set()
    for module_name in module_names:
        module = importlib.import_module(module_name)
        for obj in getattr(module, "__dict__", {}).values():
            if not isinstance(obj, type):
                continue
            if not hasattr(obj, "__tablename__"):
                continue
            if not issubclass(obj, Base):
                continue
            if obj.__module__ != module_name:
                continue
            if obj in seen:
                continue
            seen.add(obj)
            models.append(obj)
    return models


def build_all_models() -> list[type]:
    module_names = discover_model_modules()
    imported_module_names = import_model_modules(module_names)
    try:
        configure_mappers()
    except Exception as exc:  # noqa: BLE001 - surface mapper configuration failures clearly
        raise RuntimeError(
            f"failed to configure SQLAlchemy mappers after importing model modules: {exc}"
        ) from exc
    return collect_models(imported_module_names)


ALL_MODELS = build_all_models()


def _format_model(model: object) -> str:
    if hasattr(model, "__module__") and hasattr(model, "__name__"):
        return f"{model.__module__}.{model.__name__}"
    return repr(model)


def smoke_check_all_models() -> None:
    errors: list[str] = []
    module_names = discover_model_modules()
    try:
        import_model_modules(module_names)
    except Exception as exc:  # noqa: BLE001 - surface any import failure
        errors.append(f"failed to import model modules: {exc}")
        raise RuntimeError("Registry smoke check failed:\n" + "\n".join(errors)) from exc

    collected = collect_models(module_names)
    if collected and collected != ALL_MODELS:
        errors.append("ALL_MODELS order mismatch with discovery order")

    duplicates = [model for model in collected if collected.count(model) > 1]
    if duplicates:
        errors.append("duplicate models: " + ", ".join(_format_model(m) for m in duplicates))

    if errors:
        message = "Registry smoke check failed:\n" + "\n".join(errors)
        raise RuntimeError(message)


def maybe_smoke_check_all_models() -> None:
    if os.getenv("SILA_REGISTRY_SMOKE_CHECK") == "1":
        smoke_check_all_models()


maybe_smoke_check_all_models()

__all__ = [
    "ALL_MODELS",
    "discover_model_modules",
    "smoke_check_all_models",
]
