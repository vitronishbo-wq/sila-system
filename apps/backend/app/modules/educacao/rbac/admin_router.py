from fastapi import APIRouter

from apps.backend.app.modules.educacao.delegation.delegation_engine import DelegationEngine
from apps.backend.app.modules.educacao.rbac.policies import check_permission, get_permissions
from apps.backend.app.modules.educacao.rbac.roles import (
    ROLE_HIERARCHY,
    RoleMinisterial,
    role_superiores,
    role_inferiores,
)
from apps.backend.app.modules.educacao.territory.models import NivelTerritorial, TerritorialScope
from apps.backend.app.modules.educacao.territory.service import (
    scope_from_role_and_ids,
    validate_scope,
    filter_by_scope,
)
from apps.backend.app.modules.educacao.workflows.matricula_workflow import MatriculaWorkflowEngine
from apps.backend.app.modules.educacao.workflows.transferencia_workflow import TransferenciaWorkflowEngine

router = APIRouter(prefix="/educacao/admin", tags=["Educacao Admin"])

_matricula_wf = MatriculaWorkflowEngine()
_transferencia_wf = TransferenciaWorkflowEngine()
_delegation = DelegationEngine()


@router.get("/roles")
def list_roles():
    return {
        "roles": [r.value for r in ROLE_HIERARCHY],
        "hierarchy": [r.value for r in ROLE_HIERARCHY],
    }


@router.get("/roles/{role}/permissions")
def role_permissions(role: str):
    try:
        r = RoleMinisterial(role)
        perms = get_permissions(r)
        superiores = [s.value for s in role_superiores(r)]
        inferiores = [i.value for i in role_inferiores(r)]
        return {
            "role": r.value,
            "permissions": sorted(perms),
            "superiores": superiores,
            "inferiores": inferiores,
        }
    except ValueError:
        return {"error": f"role invalida: {role}"}


@router.get("/scope/check")
def check_scope(
    user_role: str,
    user_province: str = "",
    user_municipality: str = "",
    user_school: str = "",
    resource_nivel: str = "escola",
    resource_province: str = "",
    resource_municipality: str = "",
    resource_school: str = "",
):
    try:
        role = RoleMinisterial(user_role)
        user_scope = scope_from_role_and_ids(
            role, user_province or None, user_municipality or None, user_school or None,
        )
        resource_scope = TerritorialScope(
            nivel=NivelTerritorial(resource_nivel),
            province_id=resource_province or None,
            municipality_id=resource_municipality or None,
            school_id=resource_school or None,
        )
        try:
            validate_scope(user_scope, resource_scope)
            return {"allowed": True, "user_scope": user_scope.to_dict(), "resource_scope": resource_scope.to_dict()}
        except PermissionError as e:
            return {"allowed": False, "reason": str(e), "user_scope": user_scope.to_dict(), "resource_scope": resource_scope.to_dict()}
    except ValueError as e:
        return {"error": str(e)}


@router.post("/workflows/matricula/criar")
def criar_matricula_workflow(
    provider: str,
    student_id: str,
    school_id: str,
    municipality_id: str = "",
    province_id: str = "",
):
    wf = _matricula_wf.criar(
        provider=provider,
        student_id=student_id,
        school_id=school_id,
        municipality_id=municipality_id or None,
        province_id=province_id or None,
    )
    return {"ok": True, "workflow": wf}


@router.post("/workflows/matricula/avancar")
def avancar_matricula_workflow(provider: str, actor: str):
    try:
        wf = _matricula_wf.avancar(provider, actor)
        return {"ok": True, "step": wf.step.value, "history": wf.history}
    except (ValueError, PermissionError) as e:
        return {"ok": False, "error": str(e)}


@router.post("/workflows/transferencia/criar")
def criar_transferencia_workflow(
    provider: str,
    student_id: str,
    school_origin_id: str,
    school_destination_id: str,
    municipality_id: str = "",
    province_id: str = "",
):
    wf = _transferencia_wf.criar(
        provider=provider,
        student_id=student_id,
        school_origin_id=school_origin_id,
        school_destination_id=school_destination_id,
        municipality_id=municipality_id or None,
        province_id=province_id or None,
    )
    return {"ok": True, "workflow": wf}


@router.post("/workflows/transferencia/avancar")
def avancar_transferencia_workflow(provider: str, actor: str):
    try:
        wf = _transferencia_wf.avancar(provider, actor)
        return {"ok": True, "step": wf.step.value, "history": wf.history}
    except (ValueError, PermissionError) as e:
        return {"ok": False, "error": str(e)}


@router.post("/delegation/delegate")
def delegate_permission(
    delegator_role: str,
    delegator_id: str,
    delegate_role: str,
    delegate_id: str,
    permission: str,
    province_id: str = "",
    municipality_id: str = "",
    school_id: str = "",
):
    try:
        d = _delegation.delegate(
            delegator_role=RoleMinisterial(delegator_role),
            delegator_id=delegator_id,
            delegate_role=RoleMinisterial(delegate_role),
            delegate_id=delegate_id,
            permissions={permission},
            scope=TerritorialScope(
                nivel=NivelTerritorial.NACIONAL,
                province_id=province_id or None,
                municipality_id=municipality_id or None,
                school_id=school_id or None,
            ),
        )
        return {"ok": True, "delegation": {"from": d.delegator_role.value, "to": d.delegate_role.value, "permission": permission}}
    except ValueError as e:
        return {"ok": False, "error": str(e)}


@router.get("/delegation/list/{delegate_id}")
def list_delegations(delegate_id: str):
    active = _delegation.get_active_delegations(delegate_id)
    return {
        "delegate_id": delegate_id,
        "active_delegations": [
            {
                "from": d.delegator_role.value,
                "by": d.delegator_id,
                "permissions": sorted(d.permissions),
                "reason": d.reason,
            }
            for d in active
        ],
    }
