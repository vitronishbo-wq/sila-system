from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CurrentUser:
    """Minimal shared user context for cross-module auth checks."""

    user_id: UUID
    username: str
    roles: frozenset[str]

    def has_role(self, role: str) -> bool:
        return role in self.roles
