from __future__ import annotations
from .current_user import CurrentUser
SUPERUSER_ROLES = {'admin', 'super_admin', 'root'}

def has_permission(user: CurrentUser, required_role: str) -> bool:
    """Centralized permission check to avoid ad-hoc role logic in modules."""
    return required_role in user.roles or bool(user.roles.intersection(SUPERUSER_ROLES))