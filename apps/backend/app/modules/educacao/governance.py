"""On-ramp da Educação para a camada de governança.

Uso:
    from apps.backend.app.modules.educacao.governance import RoleEducacao, scope, wf
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

from apps.backend.app.modules.educacao.rbac.roles import RoleMinisterial as RoleEducacao
from apps.backend.app.modules.educacao.rbac.policies import get_permissions, check_permission as check_educacao_permission
from apps.backend.app.modules.educacao.territory.models import TerritorialScope as TerritorialScopeEducacao
from apps.backend.app.modules.educacao.territory.service import scope_from_role_and_ids, validate_scope as validate_educacao_scope
from apps.backend.app.modules.educacao.delegation.delegation_engine import DelegationEngine as DelegationEngineEducacao
from apps.backend.app.modules.educacao.organization.service import MINEDOrganizationService
from apps.backend.app.modules.educacao.organization.models import MINEDOrganization, ProvincialDirectorate, MunicipalDirectorate, School
from apps.backend.app.modules.educacao.organization.seed import seed_mined_organization, get_mined_tree
from apps.backend.app.modules.educacao.application.pagamento_matricula_service import PagamentoMatriculaService, PagamentoReferencia
from apps.backend.app.modules.educacao.infrastructure.adapters.payment_adapter import EducacaoPaymentAdapter
from apps.backend.app.modules.educacao.workflows.matricula_workflow import MatriculaWorkflowEngine
from apps.backend.app.modules.educacao.workflows.transferencia_workflow import TransferenciaWorkflowEngine

__all__ = [
    "RoleEducacao",
    "RoleGovernance",
    "role_is_above", "role_is_below",
    "get_permissions", "check_educacao_permission",
    "TerritorialScopeEducacao", "validate_educacao_scope",
    "DelegationEngineEducacao",
    "MatriculaWorkflowEngine", "TransferenciaWorkflowEngine",
    "MINEDOrganizationService",
    "MINEDOrganization", "ProvincialDirectorate", "MunicipalDirectorate", "School",
    "seed_mined_organization", "get_mined_tree",
    "PagamentoMatriculaService", "PagamentoReferencia",
    "EducacaoPaymentAdapter",
    "Organization", "OrganizationTree", "OrganizationType",
    "Tenant", "TenantManager",
    "AuditLogger", "AuditAction",
    "scope_from_role_and_ids",
]
