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


class RoleEmprego(str, Enum):
    ROLE_MINISTERIO = "nacional"
    ROLE_DIRECAO_NACIONAL = "provincial"
    ROLE_UNIDADE = "unidade"
    ROLE_OPERADOR = "operador"

_ROLE_MAP = {RoleEmprego.ROLE_MINISTERIO: RoleGovernance.ROLE_NACIONAL,
             RoleEmprego.ROLE_DIRECAO_NACIONAL: RoleGovernance.ROLE_PROVINCIAL,
             RoleEmprego.ROLE_UNIDADE: RoleGovernance.ROLE_UNIDADE,
             RoleEmprego.ROLE_OPERADOR: RoleGovernance.ROLE_OPERADOR}
def _to_gov(role: RoleEmprego) -> RoleGovernance: return _ROLE_MAP[role]

__all__ = ["RoleEmprego", "RoleGovernance", "role_is_above", "role_is_below",
    "get_role_permissions", "check_permission", "TerritorialScope", "validate_scope",
    "filter_by_scope", "TerritorialScopeError", "DelegationEngine", "Delegation",
    "WorkflowEngine", "WorkflowStep", "WorkflowInstance", "Organization",
    "OrganizationTree", "OrganizationType", "Tenant", "TenantManager",
    "AuditLogger", "AuditAction"]
