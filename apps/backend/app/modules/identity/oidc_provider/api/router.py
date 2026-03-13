from typing import Any, Dict, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from apps.backend.app.modules.identity.oidc_provider.application.oidc_service import OIDCService

router = APIRouter()
service = OIDCService()


class TokenRequest(BaseModel):
    subject: str
    credential_id: str
    registry_index: int
    credential_subject: Optional[Dict[str, Any]] = None
    scope: Optional[str] = None


@router.post('/token')
def issue_token(payload: TokenRequest):
    """Emite um token OIDC simples se a VC nao estiver revogada."""
    try:
        return service.issue_token(
            subject=payload.subject,
            credential_id=payload.credential_id,
            registry_index=payload.registry_index,
            credential_subject=payload.credential_subject,
            scope=payload.scope,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.get('/.well-known/openid-configuration')
def oidc_configuration():
    return {
        "issuer": "sila-oidc",
        "token_endpoint": "/identity/oidc_provider/token",
    }
