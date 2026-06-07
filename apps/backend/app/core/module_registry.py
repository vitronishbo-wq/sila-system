"""Explicit module registry for SILA bounded contexts.

Single source of truth for:
- enabled modules
- module -> domain federation mapping
- bootstrap mounting scope (api/main/none)
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Literal, get_args

DomainName = Literal[
    "economy",
    "educacao",
    "governance",
    "infrastructure_sector",
    "intelligence",
    "justice",
    "resources",
    "society",
]
BootstrapScope = Literal["api", "main", "none"]


@dataclass(frozen=True, slots=True)
class ModuleSpec:
    name: str
    domain: DomainName
    router_import: str | None
    mount_prefix: str = "/v1"
    mount_tags: tuple[str, ...] = ()
    bootstrap_scope: BootstrapScope = "none"
    enabled: bool = True
    notes: str = ""


MODULES_ROOT_DEFAULT = Path(__file__).resolve().parents[1] / "modules"
_MODULES_CACHE = None


def discover_modules_dynamic(modules_root: Path = MODULES_ROOT_DEFAULT) -> tuple[ModuleSpec, ...]:
    """Dynamically discover modules from macro-domain structure."""
    global _MODULES_CACHE
    if _MODULES_CACHE is not None:
        return _MODULES_CACHE
    if not modules_root.exists():
        _MODULES_CACHE = tuple()
        return _MODULES_CACHE
    specs = []
    domain_names = get_args(DomainName)
    for macro_domain_path in sorted(modules_root.iterdir()):
        if not macro_domain_path.is_dir() or macro_domain_path.name.startswith("__"):
            continue
        macro_domain = macro_domain_path.name
        if macro_domain not in domain_names:
            continue
        is_standalone_module = all(
            (macro_domain_path / component).is_dir()
            for component in ["api", "application", "domain", "infrastructure"]
        )
        if is_standalone_module:
            router_path = macro_domain_path / "api" / "router.py"
            specs.append(
                ModuleSpec(
                    name=macro_domain,
                    domain=macro_domain,
                    router_import=f"apps.backend.app.modules.{macro_domain}.api.router:router"
                    if router_path.exists()
                    else None,
                    bootstrap_scope="api",
                    enabled=True,
                )
            )
            continue
        for module_path in sorted(macro_domain_path.iterdir()):
            if not module_path.is_dir() or module_path.name.startswith("__"):
                continue
            module_name = module_path.name
            has_module_structure = any(
                (module_path / component).is_dir()
                for component in ["api", "application", "domain", "infrastructure"]
            )
            if not has_module_structure:
                continue
            router_path = module_path / "api" / "router.py"
            if router_path.exists():
                router_import = f"apps.backend.app.modules.{macro_domain}.{module_name}.api.router:router"
            else:
                router_import = None
            spec = ModuleSpec(
                name=module_name,
                domain=macro_domain,
                router_import=router_import,
                bootstrap_scope="api",
                enabled=True,
            )
            specs.append(spec)
    _MODULES_CACHE = tuple(specs)
    return _MODULES_CACHE


MODULES = discover_modules_dynamic()
MODULE_INDEX = {spec.name: spec for spec in MODULES}
if len(MODULE_INDEX) != len(MODULES):
    raise RuntimeError("Duplicate module names detected in MODULES registry.")
DOMAIN_INDEX = {}
_domain_map = defaultdict(list)
for _spec in MODULES:
    _domain_map[_spec.domain].append(_spec.name)
for _domain, _names in _domain_map.items():
    DOMAIN_INDEX[_domain] = tuple(sorted(_names))


def iter_modules(enabled_only: bool = True) -> tuple[ModuleSpec, ...]:
    if not enabled_only:
        return MODULES
    return tuple(spec for spec in MODULES if spec.enabled)


def iter_bootstrap_modules(scope: BootstrapScope) -> tuple[ModuleSpec, ...]:
    return tuple(spec for spec in iter_modules(enabled_only=True) if spec.bootstrap_scope == scope)


def list_module_names(enabled_only: bool = True) -> tuple[str, ...]:
    return tuple(spec.name for spec in iter_modules(enabled_only=enabled_only))


def get_modules_by_domain(domain: DomainName, enabled_only: bool = True) -> tuple[ModuleSpec, ...]:
    return tuple(spec for spec in iter_modules(enabled_only=enabled_only) if spec.domain == domain)


def default_module_tag(module_name: str) -> str:
    return module_name.replace("_", " ").title()


def load_module_router(spec: ModuleSpec):
    """Load router object defined by ModuleSpec.router_import."""
    if not spec.router_import:
        return None
    module_path, attribute = spec.router_import.split(":", maxsplit=1)
    module = import_module(module_path)
    return getattr(module, attribute)


def discover_module_names(modules_root: Path = MODULES_ROOT_DEFAULT) -> tuple[str, ...]:
    """Discover module names from disk."""
    return tuple(spec.name for spec in discover_modules_dynamic(modules_root))


def find_unregistered_modules(modules_root: Path = MODULES_ROOT_DEFAULT) -> tuple[str, ...]:
    """Find module folders that exist on disk but are not in the registry."""
    discovered_names = set(discover_module_names(modules_root))
    registered_names = set(spec.name for spec in iter_modules(enabled_only=False))
    unregistered = sorted(discovered_names - registered_names)
    return tuple(unregistered)


def find_missing_enabled_modules(modules_root: Path = MODULES_ROOT_DEFAULT) -> tuple[str, ...]:
    """Find enabled modules in registry that don't exist on disk."""
    discovered_names = set(discover_module_names(modules_root))
    enabled_names = set(spec.name for spec in iter_modules(enabled_only=True))
    missing = sorted(enabled_names - discovered_names)
    return tuple(missing)


def find_bootstrap_misalignment(modules_root: Path = MODULES_ROOT_DEFAULT) -> tuple[str, ...]:
    """Find bootstrap-scoped modules that don't exist on disk."""
    discovered_names = set(discover_module_names(modules_root))
    bootstrap_names = set(
        spec.name for spec in iter_modules(enabled_only=False) if spec.bootstrap_scope != "none"
    )
    misaligned = sorted(bootstrap_names - discovered_names)
    return tuple(misaligned)
