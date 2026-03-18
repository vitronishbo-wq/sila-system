"""Compatibility bridge for shared platform imports.

This module proxies legacy shared-bridges imports to app.core.bridges.* to keep
older paths working without referencing the deprecated namespace directly.
"""
from __future__ import annotations
from importlib import import_module
import sys
from app.core import bridges as _core_bridges
__all__ = list(getattr(_core_bridges, '__all__', []))
for _name in __all__:
    globals()[_name] = getattr(_core_bridges, _name)
_SUBMODULES = ['citizen_repository_bridge', 'citizen_repository_port_bridge', 'civil_identity_bridge', 'cross_domain_ports_bridge', 'emprego_bridge', 'finance_bridge', 'governance_service_requests_bridge', 'identity_bridge', 'infrastructure_sector_bridge', 'intelligence_bi_sources_bridge', 'justice_public_safety_bridge', 'resources_agricultura_bridge', 'resources_external_services_bridge', 'service_requests_bridge', 'society_domain_enums_bridge', 'society_repository_bridges', 'society_statistics_models_bridge']
for _mod in _SUBMODULES:
    sys.modules[f'{__name__}.{_mod}'] = import_module(f'app.core.bridges.{_mod}')