from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

import jwt
from core.auth import JWTHandler
from fastapi import Depends, Header, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import get_db as core_get_db
from apps.backend.app.core.identity.context import IdentityContext
from apps.backend.app.core.notifications.services.notification_service import NotificationService
from apps.backend.app.core.settings import settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in core_get_db():
        yield session


async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async for session in core_get_db():
        yield session


def _extract_roles(claims: dict[str, Any]) -> list[str]:
    roles: list[str] = []
    realm_access = claims.get("realm_access") or {}
    realm_roles = realm_access.get("roles") or []
    if isinstance(realm_roles, list):
        roles.extend(realm_roles)
    resource_access = claims.get("resource_access") or {}
    if isinstance(resource_access, dict):
        for resource in resource_access.values():
            resource_roles = resource.get("roles") or []
            if isinstance(resource_roles, list):
                roles.extend(resource_roles)
    return roles


def _map_primary_role(roles: list[str], email: str | None) -> str | None:
    role_set = {role.upper() for role in roles if role}
    if "CITIZEN" in role_set:
        return "CITIZEN"
    if "SUPERADMIN" in role_set:
        return "ADMIN_SUPER"
    if "ADMIN" in role_set:
        return "ADMIN_CENTRAL"
    if "MANAGER" in role_set:
        prefix = (email or "").split("@")[0].lower()
        if prefix.startswith("prov"):
            return "ADMIN_PROVINCIAL"
        if prefix.startswith("mun"):
            return "ADMIN_MUNICIPAL"
        if prefix.startswith("comun"):
            return "ADMIN_COMMUNAL"
        return "ADMIN_CENTRAL"
    return None


def _map_levels(primary_role: str | None) -> tuple[str | None, str | None]:
    if primary_role == "ADMIN_SUPER":
        return ("super", "CENTRAL")
    if primary_role == "ADMIN_CENTRAL":
        return ("central", "CENTRAL")
    if primary_role == "ADMIN_PROVINCIAL":
        return ("provincial", "PROVINCIAL")
    if primary_role == "ADMIN_MUNICIPAL":
        return ("municipal", "LOCAL")
    if primary_role == "ADMIN_COMMUNAL":
        return ("communal", "LOCAL")
    return (None, None)


def _decode_local_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except InvalidTokenError:
        return None


async def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    """Extract current user from JWT token using centralized JWTHandler.

    Uses core/auth JWTHandler for token validation and role extraction.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Empty bearer token")
    jwt_handler = JWTHandler(secret_key=settings.SECRET_KEY)
    try:
        claims = jwt_handler.decode_token(token)
        if not claims:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token validation error"
        ) from err
    user = dict(claims)
    user["authorization"] = authorization
    user.setdefault("roles", _extract_roles(claims))
    scope = claims.get("scope", "")
    user.setdefault("scopes", scope.split() if isinstance(scope, str) and scope else [])
    if not user.get("role") and user.get("roles"):
        primary_role = _map_primary_role(user.get("roles", []), user.get("email"))
        if primary_role:
            level_lower, level_upper = _map_levels(primary_role)
            user["role"] = primary_role
            if level_lower:
                user.setdefault("level", level_lower)
            if level_upper:
                user.setdefault("administrative_level", level_upper)
    return user


current_user_dep = Depends(get_current_user)


async def get_current_citizen_user(
    current_user: dict[str, Any] = current_user_dep,
) -> dict[str, Any]:
    return current_user


async def get_identity_context(
    current_user: dict[str, Any] = current_user_dep,
) -> IdentityContext:
    return IdentityContext(current_user)

db_dep = Depends(get_db)


async def get_notification_service(db: AsyncSession = db_dep) -> NotificationService:
    return NotificationService(db)
