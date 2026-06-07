from sila_platform.governance.rbac.roles import RoleGovernance, ROLE_HIERARCHY, role_is_above, role_is_below
from sila_platform.governance.rbac.policies import get_role_permissions, check_permission
from sila_platform.governance.territory.models import TerritorialScope
from sila_platform.governance.territory.service import validate_scope, filter_by_scope, TerritorialScopeError
from sila_platform.governance.delegation.engine import DelegationEngine, Delegation
from sila_platform.governance.workflows.engine import WorkflowEngine, WorkflowStep, WorkflowInstance
from sila_platform.governance.organization.models import Organization, OrganizationTree, OrganizationType
from sila_platform.governance.tenancy.models import Tenant, TenantManager
from sila_platform.governance.audit.logger import AuditLogger, AuditAction

from enum import Enum


class RoleRegistoCivil(str, Enum):
    ROLE_MINISTERIO = "nacional"
    ROLE_DIRECAO_NACIONAL = "provincial"
    ROLE_MUNICIPIO = "municipal"
    ROLE_CONSERVATORIA = "unidade"
    ROLE_OPERADOR = "operador"


_ROLE_MAP = {
    RoleRegistoCivil.ROLE_MINISTERIO: RoleGovernance.ROLE_NACIONAL,
    RoleRegistoCivil.ROLE_DIRECAO_NACIONAL: RoleGovernance.ROLE_PROVINCIAL,
    RoleRegistoCivil.ROLE_MUNICIPIO: RoleGovernance.ROLE_MUNICIPAL,
    RoleRegistoCivil.ROLE_CONSERVATORIA: RoleGovernance.ROLE_UNIDADE,
    RoleRegistoCivil.ROLE_OPERADOR: RoleGovernance.ROLE_OPERADOR,
}


def _to_gov(role: RoleRegistoCivil) -> RoleGovernance:
    return _ROLE_MAP[role]


__all__ = [
    "RoleRegistoCivil",
    "RoleGovernance",
    "role_is_above", "role_is_below",
    "get_role_permissions", "check_permission",
    "TerritorialScope", "validate_scope", "filter_by_scope", "TerritorialScopeError",
    "DelegationEngine", "Delegation",
    "WorkflowEngine", "WorkflowStep", "WorkflowInstance",
    "Organization", "OrganizationTree", "OrganizationType",
    "Tenant", "TenantManager",
    "AuditLogger", "AuditAction",
]
