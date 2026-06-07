from __future__ import annotations

from typing import Optional, TypeVar

from sila_platform.governance.rbac.roles import RoleGovernance
from sila_platform.governance.territory.constants import NivelTerritorial
from sila_platform.governance.territory.models import TerritorialScope

T = TypeVar("T")


class TerritorialScopeError(PermissionError):
    """Quando o utilizador tenta aceder fora do seu âmbito territorial."""


NIVEL_MAP: dict[RoleGovernance, NivelTerritorial] = {
    RoleGovernance.ROLE_NACIONAL: NivelTerritorial.NACIONAL,
    RoleGovernance.ROLE_PROVINCIAL: NivelTerritorial.PROVINCIAL,
    RoleGovernance.ROLE_MUNICIPAL: NivelTerritorial.MUNICIPAL,
    RoleGovernance.ROLE_UNIDADE: NivelTerritorial.UNIDADE,
    RoleGovernance.ROLE_OPERADOR: NivelTerritorial.OPERADOR,
}


def scope_from_role_and_ids(
    role: RoleGovernance,
    province_id: Optional[str] = None,
    municipality_id: Optional[str] = None,
    unit_id: Optional[str] = None,
) -> TerritorialScope:
    return TerritorialScope(
        nivel=NIVEL_MAP.get(role, NivelTerritorial.NACIONAL),
        province_id=province_id,
        municipality_id=municipality_id,
        unit_id=unit_id,
    )


def validate_scope(
    user_scope: TerritorialScope,
    resource_scope: TerritorialScope,
) -> None:
    if not user_scope.covers(resource_scope):
        raise TerritorialScopeError(
            f"Utilizador com âmbito {user_scope.nivel.value} "
            f"(province={user_scope.province_id}, "
            f"municipality={user_scope.municipality_id}, "
            f"unit={user_scope.unit_id}) "
            f"não cobre recurso {resource_scope.nivel.value} "
            f"(province={resource_scope.province_id}, "
            f"municipality={resource_scope.municipality_id}, "
            f"unit={resource_scope.unit_id})"
        )


def filter_by_scope(
    user_scope: TerritorialScope,
    resources: list[T],
    province_field: str = "province_id",
    municipality_field: str = "municipality_id",
    unit_field: str = "unit_id",
) -> list[T]:
    nivel = user_scope.nivel
    if nivel == NivelTerritorial.NACIONAL:
        return resources
    if nivel == NivelTerritorial.PROVINCIAL:
        return [r for r in resources if getattr(r, province_field, None) == user_scope.province_id]
    if nivel == NivelTerritorial.MUNICIPAL:
        return [r for r in resources if getattr(r, municipality_field, None) == user_scope.municipality_id]
    if nivel in (NivelTerritorial.UNIDADE, NivelTerritorial.OPERADOR):
        return [r for r in resources if getattr(r, unit_field, None) == user_scope.unit_id]
    return resources
