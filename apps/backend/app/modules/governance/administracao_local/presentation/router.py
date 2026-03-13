from fastapi import APIRouter, HTTPException, Depends
from apps.backend.app.modules.governance.administracao_local.presentation.schemas import AdministradorRead
from apps.backend.app.modules.governance.administracao_local.presentation.dependencies import get_administracao_service
from apps.backend.app.modules.governance.administracao_local.application.service import AdministracaoLocalService
router = APIRouter(prefix='/administracao-local', tags=['Administracao Local'])

@router.get('/administradores/{admin_id}', response_model=AdministradorRead)
async def get_administrador(admin_id: str, service: AdministracaoLocalService=Depends(get_administracao_service)):
    admin = await service.get_administrador(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail='Administrador não encontrado')
    return admin