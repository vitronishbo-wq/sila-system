import time
import uuid
from typing import Any, Dict, Optional

from apps.backend.app.modules.identity.infrastructure.security.jwt_engine import SovereignJWT
from apps.backend.app.modules.identity.verifiable_credentials.infrastructure.repositories.revocation_repository import (
    DEFAULT_REVOCATION_REPOSITORY,
    RevocationRepository,
)


class OIDCService:
    """Servico minimo de OIDC para emitir tokens baseados em VC."""

    def __init__(
        self,
        revocation_repo: RevocationRepository = DEFAULT_REVOCATION_REPOSITORY,
        jwt_engine: Optional[SovereignJWT] = None,
    ):
        self.revocation_repo = revocation_repo
        self.jwt_engine = jwt_engine

    def build_claims(self, subject: str, credential_subject: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        claims: Dict[str, Any] = {"sub": subject}
        if not credential_subject:
            return claims
        if "name" in credential_subject:
            claims["name"] = credential_subject["name"]
        if "first_name" in credential_subject:
            claims["given_name"] = credential_subject["first_name"]
        if "last_name" in credential_subject:
            claims["family_name"] = credential_subject["last_name"]
        if "email" in credential_subject:
            claims["email"] = credential_subject["email"]
        if "bi" in credential_subject:
            claims["document_number"] = credential_subject["bi"]
        if "document_number" in credential_subject:
            claims["document_number"] = credential_subject["document_number"]
        if "birth_date" in credential_subject:
            claims["birthdate"] = credential_subject["birth_date"]
        return claims

    def issue_token(
        self,
        subject: str,
        credential_id: str,
        registry_index: int,
        credential_subject: Optional[Dict[str, Any]] = None,
        scope: Optional[str] = None,
    ) -> Dict[str, Any]:
        if self.revocation_repo.is_revoked(registry_index):
            raise ValueError("Credential is revoked")
        return {
            "access_token": str(uuid.uuid4()),
            "token_type": "Bearer",
            "subject": subject,
            "credential_id": credential_id,
            "issued_at": int(time.time()),
            "scope": scope,
            "claims": self.build_claims(subject, credential_subject),
        }

    async def authenticate(
        self,
        identity_id: str,
        roles: list,
    ) -> Dict[str, Any]:
        if not self.jwt_engine:
            raise ValueError("jwt_engine not configured")

        token = self.jwt_engine.issue_token(
            identity_id,
            roles,
        )

        return {
            "access_token": token,
            "token_type": "Bearer",
        }
