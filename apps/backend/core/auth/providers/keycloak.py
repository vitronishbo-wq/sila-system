from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set

import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError

from core.auth.roles.role_manager import RoleManager


class KeycloakAuthProvider:
    """
    Keycloak adapter for validating JWTs and mapping claims to roles/perms.
    """

    def __init__(
        self,
        issuer: str,
        jwks_url: str,
        client_id: str,
        algorithms: Optional[List[str]] = None,
        role_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        self.issuer = issuer
        self.jwks_url = jwks_url
        self.client_id = client_id
        self.algorithms = algorithms or ["RS256"]
        self.role_mapping = role_mapping or {}
        self._jwks_client = PyJWKClient(self.jwks_url)
        self._role_manager = RoleManager()

    def _decode(self, token: str, verify_exp: bool = True) -> Dict[str, Any]:
        signing_key = self._jwks_client.get_signing_key_from_jwt(token)
        try:
            return jwt.decode(
                token,
                signing_key.key,
                algorithms=self.algorithms,
                audience=self.client_id,
                issuer=self.issuer,
                options={"verify_exp": verify_exp},
            )
        except Exception as exc:  # pragma: no cover - passthrough
            raise InvalidTokenError(f"Token validation failed: {exc}") from exc

    def _extract_roles(self, claims: Dict[str, Any]) -> List[str]:
        roles: Set[str] = set()

        realm_roles = (
            claims.get("realm_access", {}).get("roles", []) or []
        )
        roles.update(realm_roles)

        resource_access = claims.get("resource_access", {}) or {}
        client_roles = (
            resource_access.get(self.client_id, {}).get("roles", []) or []
        )
        roles.update(client_roles)

        direct_roles = claims.get("roles", []) or []
        if isinstance(direct_roles, str):
            direct_roles = [direct_roles]
        roles.update(direct_roles)

        mapped = {self.role_mapping.get(r, r) for r in roles}
        return sorted(mapped)

    def _roles_to_permissions(self, roles: Iterable[str]) -> List[str]:
        permissions: Set[str] = set()
        for role in roles:
            if self._role_manager.role_exists(role):
                permissions.update(self._role_manager.get_permissions(role))
        return sorted(permissions)

    def authenticate(self, token: str) -> Dict[str, Any]:
        claims = self._decode(token)
        roles = self._extract_roles(claims)
        permissions = self._roles_to_permissions(roles)
        return {
            "subject": claims.get("sub"),
            "roles": roles,
            "permissions": permissions,
            "claims": claims,
        }


__all__ = ["KeycloakAuthProvider"]
