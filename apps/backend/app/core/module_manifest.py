"""Module manifest helpers for runtime/router automation and tooling."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
MODULES_ROOT = Path(__file__).resolve().parents[1] / 'modules'

def load_manifests(modules_root: Path=MODULES_ROOT) -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    if not modules_root.exists():
        return manifests
    for manifest_path in sorted(modules_root.glob('*/module.yaml')):
        try:
            payload = yaml.safe_load(manifest_path.read_text(encoding='utf-8')) or {}
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        name = payload.get('name')
        if isinstance(name, str) and name:
            manifests[name] = payload
    return manifests

def iter_manifest_api_routers(modules_root: Path=MODULES_ROOT) -> tuple[str, ...]:
    routers: set[str] = set()
    for manifest in load_manifests(modules_root).values():
        exposes = manifest.get('exposes', {})
        if not isinstance(exposes, dict):
            continue
        values = exposes.get('api_routers', [])
        if not isinstance(values, list):
            continue
        for value in values:
            if isinstance(value, str) and value:
                routers.add(value)
    return tuple(sorted(routers))