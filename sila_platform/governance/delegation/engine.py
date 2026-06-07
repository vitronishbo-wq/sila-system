from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sila_platform.governance.rbac.roles import RoleGovernance, role_is_below
from sila_platform.governance.territory.models import TerritorialScope


class DelegationStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass
class Delegation:
    delegator_role: RoleGovernance
    delegator_id: str
    delegate_role: RoleGovernance
    delegate_id: str
    permissions: set[str]
    scope: TerritorialScope
    status: DelegationStatus = DelegationStatus.ACTIVE
    reason: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    revoked_at: Optional[datetime] = None


class DelegationEngine:
    """Engine de delegação hierárquica governamental.
    Permite que um nível superior delegue autoridade a um nível inferior.
    """

    def __init__(self) -> None:
        self._delegations: list[Delegation] = []

    def delegate(
        self,
        delegator_role: RoleGovernance,
        delegator_id: str,
        delegate_role: RoleGovernance,
        delegate_id: str,
        permissions: set[str],
        scope: TerritorialScope,
        reason: Optional[str] = None,
        expires_at: Optional[datetime] = None,
    ) -> Delegation:
        if not role_is_below(delegator_role, delegate_role):
            raise ValueError(
                f"{delegator_role.value} não pode delegar para {delegate_role.value}. "
                "Só é permitido delegar de cima para baixo na hierarquia."
            )
        delegation = Delegation(
            delegator_role=delegator_role,
            delegator_id=delegator_id,
            delegate_role=delegate_role,
            delegate_id=delegate_id,
            permissions=permissions,
            scope=scope,
            reason=reason,
            expires_at=expires_at,
        )
        self._delegations.append(delegation)
        return delegation

    def revoke(self, delegate_id: str) -> bool:
        for d in self._delegations:
            if d.delegate_id == delegate_id and d.status == DelegationStatus.ACTIVE:
                d.status = DelegationStatus.REVOKED
                d.revoked_at = datetime.now(timezone.utc)
                return True
        return False

    def has_delegated_permission(self, delegate_id: str, permission: str) -> bool:
        now = datetime.now(timezone.utc)
        for d in self._delegations:
            if d.delegate_id != delegate_id:
                continue
            if d.status != DelegationStatus.ACTIVE:
                continue
            if d.expires_at and now > d.expires_at:
                d.status = DelegationStatus.EXPIRED
                continue
            if permission in d.permissions:
                return True
        return False

    def get_active_delegations(self, delegate_id: Optional[str] = None) -> list[Delegation]:
        now = datetime.now(timezone.utc)
        result = []
        for d in self._delegations:
            if d.status != DelegationStatus.ACTIVE:
                continue
            if d.expires_at and now > d.expires_at:
                d.status = DelegationStatus.EXPIRED
                continue
            if delegate_id and d.delegate_id != delegate_id:
                continue
            result.append(d)
        return result

    def list_for_delegator(self, delegator_id: str) -> list[Delegation]:
        return [d for d in self._delegations if d.delegator_id == delegator_id]
