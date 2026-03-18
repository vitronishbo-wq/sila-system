import os
from typing import Optional
from fastapi import APIRouter, Query, Header, HTTPException, status
from apps.backend.app.modules.identity.subdomains.verifiable_credentials.application.services.revocation_service import RevocationService
from apps.backend.app.modules.identity.subdomains.verifiable_credentials.infrastructure.repositories.revocation_repository import DEFAULT_REVOCATION_REPOSITORY
router = APIRouter(prefix='/verifiable_credentials', tags=['endpoints'])
_revocation_service = RevocationService(DEFAULT_REVOCATION_REPOSITORY)
_admin_token = os.getenv('SILA_ADMIN_TOKEN', 'dev-admin-token')

@router.get('/status/{registry_index}')
def get_credential_status(registry_index: int, credential_id: Optional[str]=None, include_status_list: bool=Query(default=False)):
    """Consulta o status de revogacao de uma credencial (StatusList2021)."""
    revoked = DEFAULT_REVOCATION_REPOSITORY.is_revoked(registry_index)
    response = {'credential_id': credential_id, 'registry_index': registry_index, 'revoked': revoked}
    if include_status_list:
        response['status_list'] = DEFAULT_REVOCATION_REPOSITORY.get_compressed_status_list()
    return response

@router.post('/revoke')
def revoke_credential(credential_id: str, registry_index: int, x_admin_token: Optional[str]=Header(default=None, alias='X-Admin-Token')):
    """Revoga uma credencial via API (admin)."""
    if not x_admin_token or x_admin_token != _admin_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin token invalid')
    return _revocation_service.invalidate_credential(credential_id, registry_index)