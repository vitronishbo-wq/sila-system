from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class TenantStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


@dataclass
class Tenant:
    """Propriedade administrativa de um módulo governamental.
    
    Cada módulo (educacao, saude, justica) é um tenant.
    Define ownership — RBAC, menus, dashboards, workflows internos, auditoria.
    
    NÃO bloqueia interoperabilidade transversal.
    Workflows cross-sector e eventos atravessam tenants livremente
    através de platform/interoperability/.
    """
    id: str
    module: str
    name: str
    description: Optional[str] = None
    status: TenantStatus = TenantStatus.ACTIVE
    config: dict[str, Any] = field(default_factory=dict)
    parent_tenant_id: Optional[str] = None
    organization_id: Optional[str] = None
    territory_scope_id: Optional[str] = None


class TenantManager:
    """Gestor de inquilinos (tenants) para isolamento entre módulos."""

    def __init__(self) -> None:
        self._tenants: dict[str, Tenant] = {}

    def register(self, tenant: Tenant) -> Tenant:
        self._tenants[tenant.id] = tenant
        return tenant

    def get(self, tenant_id: str) -> Optional[Tenant]:
        return self._tenants.get(tenant_id)

    def get_by_module(self, module: str) -> Optional[Tenant]:
        for t in self._tenants.values():
            if t.module == module and t.status == TenantStatus.ACTIVE:
                return t
        return None

    def list_active(self) -> list[Tenant]:
        return [t for t in self._tenants.values() if t.status == TenantStatus.ACTIVE]

    def list_all(self) -> list[Tenant]:
        return list(self._tenants.values())

    def activate(self, tenant_id: str) -> bool:
        t = self._tenants.get(tenant_id)
        if t:
            t.status = TenantStatus.ACTIVE
            return True
        return False

    def deactivate(self, tenant_id: str) -> bool:
        t = self._tenants.get(tenant_id)
        if t:
            t.status = TenantStatus.INACTIVE
            return True
        return False

    def get_module_config(self, module: str, key: str, default: Any = None) -> Any:
        tenant = self.get_by_module(module)
        if tenant:
            return tenant.config.get(key, default)
        return default
