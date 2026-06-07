"""Core bridge layer with lazy exports to avoid import-time cycles."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "BIEventRecord",
    "BIRecord",
    "CitizenRepository",
    "CitizenRepositoryPort",
    "CitizenFUC",
    "ServiceRequestLifecycleBridge",
]
_EXPORTS: dict[str, tuple[str, str]] = {
    "CitizenRepository": ("apps.backend.app.core.bridges.citizen_repository_bridge", "CitizenRepository"),
    "CitizenRepositoryPort": (
        "apps.backend.app.core.bridges.citizen_repository_port_bridge",
        "CitizenRepositoryPort",
    ),
    "BIEventRecord": ("apps.backend.app.core.bridges.identity_bridge", "BIEventRecord"),
    "BIRecord": ("apps.backend.app.core.bridges.identity_bridge", "BIRecord"),
    "CitizenFUC": ("apps.backend.app.core.bridges.identity_bridge", "CitizenFUC"),
    "ServiceRequestLifecycleBridge": (
        "apps.backend.app.core.bridges.service_requests_bridge",
        "ServiceRequestLifecycleBridge",
    ),
}


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_path, attr = _EXPORTS[name]
    module = import_module(module_path)
    return getattr(module, attr)
