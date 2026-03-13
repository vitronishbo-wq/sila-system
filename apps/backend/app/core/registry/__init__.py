"""Macro-domain: module registry/catalog identity."""
from app.core.module_manifest import iter_manifest_api_routers, load_manifests
from app.core.module_registry import ModuleSpec, discover_modules_dynamic
__all__ = ['ModuleSpec', 'discover_modules_dynamic', 'iter_manifest_api_routers', 'load_manifests']