from __future__ import annotations

from enum import Enum


class RoleGovernance(str, Enum):
    """Roles genéricas para qualquer módulo governamental.
    Hierarquia: NACIONAL > PROVINCIAL > MUNICIPAL > UNIDADE > OPERADOR.
    """
    ROLE_NACIONAL = "nacional"
    ROLE_PROVINCIAL = "provincial"
    ROLE_MUNICIPAL = "municipal"
    ROLE_UNIDADE = "unidade"
    ROLE_OPERADOR = "operador"


ROLE_HIERARCHY: list[RoleGovernance] = list(RoleGovernance)


def role_is_above(a: RoleGovernance, b: RoleGovernance) -> bool:
    return ROLE_HIERARCHY.index(a) < ROLE_HIERARCHY.index(b)


def role_is_below(a: RoleGovernance, b: RoleGovernance) -> bool:
    return ROLE_HIERARCHY.index(a) > ROLE_HIERARCHY.index(b)


def role_superiores(role: RoleGovernance) -> list[RoleGovernance]:
    idx = ROLE_HIERARCHY.index(role)
    return ROLE_HIERARCHY[:idx]


def role_inferiores(role: RoleGovernance) -> list[RoleGovernance]:
    idx = ROLE_HIERARCHY.index(role)
    return ROLE_HIERARCHY[idx + 1:]
