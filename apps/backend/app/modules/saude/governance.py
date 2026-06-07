"""On-ramp da Saúde para a camada de governança.

Uso:
    from apps.backend.app.modules.saude.governance import RoleSaude, scope_saude, wf_saude
"""

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


class RoleSaude(str, Enum):
    ROLE_MINISTERIO = "nacional"
    ROLE_DIRECAO_PROVINCIAL = "provincial"
    ROLE_DIRECAO_MUNICIPAL = "municipal"
    ROLE_HOSPITAL = "unidade"
    ROLE_OPERADOR = "operador"


_ROLE_MAP = {
    RoleSaude.ROLE_MINISTERIO: RoleGovernance.ROLE_NACIONAL,
    RoleSaude.ROLE_DIRECAO_PROVINCIAL: RoleGovernance.ROLE_PROVINCIAL,
    RoleSaude.ROLE_DIRECAO_MUNICIPAL: RoleGovernance.ROLE_MUNICIPAL,
    RoleSaude.ROLE_HOSPITAL: RoleGovernance.ROLE_UNIDADE,
    RoleSaude.ROLE_OPERADOR: RoleGovernance.ROLE_OPERADOR,
}


def _to_gov(role: RoleSaude) -> RoleGovernance:
    return _ROLE_MAP[role]


__all__ = [
    "RoleSaude",
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
