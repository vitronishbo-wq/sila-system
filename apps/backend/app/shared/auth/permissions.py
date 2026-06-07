from __future__ import annotations

from apps.backend.core.auth import PermissionGuard, RoleManager

from .current_user import CurrentUser

SUPERUSER_ROLES = RoleManager().get_superuser_roles()


def has_permission(user: CurrentUser, required_role: str) -> bool:
    """Centralized permission check using core/auth PermissionGuard.

    Delegates to the consolidated permission system for consistency.
    """
    PermissionGuard(RoleManager())
    return required_role in user.roles or bool(user.roles.intersection(SUPERUSER_ROLES))
