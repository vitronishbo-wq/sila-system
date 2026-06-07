from __future__ import annotations

from enum import Enum

from sila_platform.governance.rbac.roles import (
    RoleGovernance,
    ROLE_HIERARCHY as GOV_HIERARCHY,
    role_is_above as gov_role_is_above,
    role_is_below as gov_role_is_below,
    role_superiores as gov_role_superiores,
    role_inferiores as gov_role_inferiores,
)


class RoleMinisterial(str, Enum):
    """Roles do Sistema Nacional de Gestão Educacional.
    Mapeia para RoleGovernance da plataforma.
    """
    ROLE_MINISTERIO = "nacional"
    ROLE_PROVINCIA = "provincial"
    ROLE_MUNICIPIO = "municipal"
    ROLE_ESCOLA = "unidade"
    ROLE_OPERADOR = "operador"


_ROLE_MAP: dict[RoleMinisterial, RoleGovernance] = {
    RoleMinisterial.ROLE_MINISTERIO: RoleGovernance.ROLE_NACIONAL,
    RoleMinisterial.ROLE_PROVINCIA: RoleGovernance.ROLE_PROVINCIAL,
    RoleMinisterial.ROLE_MUNICIPIO: RoleGovernance.ROLE_MUNICIPAL,
    RoleMinisterial.ROLE_ESCOLA: RoleGovernance.ROLE_UNIDADE,
    RoleMinisterial.ROLE_OPERADOR: RoleGovernance.ROLE_OPERADOR,
}


def _to_gov(role: RoleMinisterial) -> RoleGovernance:
    return _ROLE_MAP[role]


ROLE_HIERARCHY: list[RoleMinisterial] = [
    RoleMinisterial.ROLE_MINISTERIO,
    RoleMinisterial.ROLE_PROVINCIA,
    RoleMinisterial.ROLE_MUNICIPIO,
    RoleMinisterial.ROLE_ESCOLA,
    RoleMinisterial.ROLE_OPERADOR,
]


def role_is_above(a: RoleMinisterial, b: RoleMinisterial) -> bool:
    return gov_role_is_above(_to_gov(a), _to_gov(b))


def role_is_below(a: RoleMinisterial, b: RoleMinisterial) -> bool:
    return gov_role_is_below(_to_gov(a), _to_gov(b))


def role_superiores(role: RoleMinisterial) -> list[RoleMinisterial]:
    return [r for r in ROLE_HIERARCHY[:ROLE_HIERARCHY.index(role)]]


def role_inferiores(role: RoleMinisterial) -> list[RoleMinisterial]:
    return [r for r in ROLE_HIERARCHY[ROLE_HIERARCHY.index(role) + 1:]]
