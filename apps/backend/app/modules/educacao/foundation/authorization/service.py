from __future__ import annotations

from collections.abc import Callable


class AuthorizationService:
    """Minimal RBAC-like authorization service.

    This stores permissions per user (and optionally per tenant).
    In production, back this with a policy engine (OPA) or a DB.
    """

    def __init__(self) -> None:
        self._permissions: dict[str, set[str]] = {}

    def grant(self, user_id: str, permission: str) -> None:
        self._permissions.setdefault(user_id, set()).add(permission)

    def revoke(self, user_id: str, permission: str) -> None:
        self._permissions.get(user_id, set()).discard(permission)

    def has_permission(self, user_id: str, permission: str, tenant_id: str | None = None) -> bool:
        return permission in self._permissions.get(user_id, set())


def require_permission(permission: str):
    """Decorator factory to require a permission on function calls.

    The decorated function is expected to receive `user_id` as a kwarg
    or positional arg (first arg after self for methods).
    """

    def deco(fn: Callable):
        def wrapper(*args, **kwargs):
            svc = AuthorizationService()
            user_id = kwargs.get("user_id")
            if user_id is None and len(args) > 0:
                # assume first arg is user_id for simple functions
                user_id = args[0]
            if not svc.has_permission(user_id, permission):
                raise PermissionError(f"user {user_id} lacks {permission}")
            return fn(*args, **kwargs)

        return wrapper

    return deco
