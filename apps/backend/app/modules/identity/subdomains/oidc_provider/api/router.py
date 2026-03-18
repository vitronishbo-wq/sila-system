from typing import Any, Dict, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Request, status
from apps.backend.app.modules.identity.subdomains.oidc_provider.application.oidc_service import OIDCService
from apps.backend.app.modules.identity.subdomains.oidc_provider.infrastructure.jwks import get_jwks, load_provider_config
router = APIRouter(tags=['endpoints'])
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
        return service.issue_token(subject=payload.subject, credential_id=payload.credential_id, registry_index=payload.registry_index, credential_subject=payload.credential_subject, scope=payload.scope)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))

@router.get('/.well-known/openid-configuration')
def oidc_configuration(request: Request):
    config = load_provider_config()
    base_url = str(request.base_url).rstrip('/')
    default_issuer = f'{base_url}/identity/oidc_provider'
    issuer = config.issuer if config.issuer.startswith('http') else default_issuer
    jwks_uri = f'{issuer}/jwks' if issuer.startswith('http') else f'{default_issuer}/jwks'
    token_endpoint = f'{issuer}/token' if issuer.startswith('http') else f'{default_issuer}/token'
    return {'issuer': issuer, 'token_endpoint': token_endpoint, 'jwks_uri': jwks_uri, 'token_endpoint_auth_methods_supported': ['client_secret_basic', 'client_secret_post'], 'grant_types_supported': ['client_credentials']}

@router.get('/jwks')
def jwks():
    return get_jwks()