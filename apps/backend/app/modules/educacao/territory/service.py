from __future__ import annotations

from typing import Optional

from sila_platform.governance.territory.service import (
    TerritorialScopeError,
    scope_from_role_and_ids as gov_scope_from_role_and_ids,
    validate_scope as gov_validate_scope,
    filter_by_scope as gov_filter_by_scope,
)
from apps.backend.app.modules.educacao.rbac.roles import RoleMinisterial, _to_gov
from apps.backend.app.modules.educacao.territory.models import TerritorialScope


def scope_from_role_and_ids(
    role: RoleMinisterial,
    province_id: Optional[str] = None,
    municipality_id: Optional[str] = None,
    school_id: Optional[str] = None,
) -> TerritorialScope:
    gov_scope = gov_scope_from_role_and_ids(
        _to_gov(role), province_id, municipality_id, school_id,
    )
    return TerritorialScope._from_gov(gov_scope)


def validate_scope(
    user_scope: TerritorialScope,
    resource_scope: TerritorialScope,
) -> None:
    gov_validate_scope(user_scope._to_gov(), resource_scope._to_gov())


def filter_by_scope(
    user_scope: TerritorialScope,
    resources: list[tuple],
    resource_province_field: str = "province_id",
    resource_municipality_field: str = "municipality_id",
    resource_school_field: str = "school_id",
) -> list:
    gov_resources = gov_filter_by_scope(
        user_scope._to_gov(), resources,
        province_field=resource_province_field,
        municipality_field=resource_municipality_field,
        unit_field=resource_school_field,
    )
    return gov_resources
