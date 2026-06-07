from __future__ import annotations

from datetime import datetime
from typing import Optional

from sila_platform.governance.delegation.engine import (
    Delegation as GovDelegation,
    DelegationEngine as GovDelegationEngine,
    DelegationStatus,
)
from apps.backend.app.modules.educacao.rbac.roles import RoleMinisterial, _to_gov
from apps.backend.app.modules.educacao.territory.models import TerritorialScope


class Delegation(GovDelegation):
    """Delegação da Educação. Reutiliza a governance com tipos Educação."""
    delegator_role: RoleMinisterial
    delegate_role: RoleMinisterial
    scope: TerritorialScope


class DelegationEngine:
    """Engine de delegação da Educação. Wrapper sobre a governance."""

    def __init__(self) -> None:
        self._gov = GovDelegationEngine()

    def delegate(
        self,
        delegator_role: RoleMinisterial,
        delegator_id: str,
        delegate_role: RoleMinisterial,
        delegate_id: str,
        permissions: set[str],
        scope: TerritorialScope,
        reason: Optional[str] = None,
        expires_at: Optional[datetime] = None,
    ) -> Delegation:
        gov_del = self._gov.delegate(
            delegator_role=_to_gov(delegator_role),
            delegator_id=delegator_id,
            delegate_role=_to_gov(delegate_role),
            delegate_id=delegate_id,
            permissions=permissions,
            scope=scope._to_gov(),
            reason=reason,
            expires_at=expires_at,
        )
        return Delegation(
            delegator_role=delegator_role,
            delegator_id=gov_del.delegator_id,
            delegate_role=delegate_role,
            delegate_id=gov_del.delegate_id,
            permissions=gov_del.permissions,
            scope=scope,
            status=gov_del.status,
            reason=gov_del.reason,
            expires_at=gov_del.expires_at,
            created_at=gov_del.created_at,
            revoked_at=gov_del.revoked_at,
        )

    def revoke(self, delegate_id: str) -> bool:
        return self._gov.revoke(delegate_id)

    def has_delegated_permission(self, delegate_id: str, permission: str) -> bool:
        return self._gov.has_delegated_permission(delegate_id, permission)

    def get_active_delegations(self, delegate_id: Optional[str] = None) -> list[Delegation]:
        return [self._to_edu(d) for d in self._gov.get_active_delegations(delegate_id)]

    def list_for_delegator(self, delegator_id: str) -> list[Delegation]:
        return [self._to_edu(d) for d in self._gov.list_for_delegator(delegator_id)]

    @staticmethod
    def _to_edu(gov: GovDelegation) -> Delegation:
        return Delegation(
            delegator_role=RoleMinisterial(gov.delegator_role.value),
            delegator_id=gov.delegator_id,
            delegate_role=RoleMinisterial(gov.delegate_role.value),
            delegate_id=gov.delegate_id,
            permissions=gov.permissions,
            scope=TerritorialScope._from_gov(gov.scope),
            status=gov.status,
            reason=gov.reason,
            expires_at=gov.expires_at,
            created_at=gov.created_at,
            revoked_at=gov.revoked_at,
        )
