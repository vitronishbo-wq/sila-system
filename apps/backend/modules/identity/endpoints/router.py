from fastapi import APIRouter, Depends
from modules.identity.models.user import User
from modules.identity.schemas.citizen_identity import CitizenIdentityRead
from core.security import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=CitizenIdentityRead)
async def get_my_identity(
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna o perfil completo do utilizador autenticado (Fonte da Verdade).
    """
    return current_user