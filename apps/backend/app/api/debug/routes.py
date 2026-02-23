"""
Endpoint de diagnóstico para identificar problemas de autenticação
REMOVER EM PRODUÇÃO!
"""

from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from modules.identity.models.user import User
from app.core.constants import UserRole
import logging

router = APIRouter(prefix="/debug", tags=["debug"])

logger = logging.getLogger(__name__)

@router.get("/auth-check")
async def debug_auth(current_user: User = Depends(get_current_user)):
    """
    Endpoint de diagnóstico que mostra EXATAMENTE o que o backend sabe sobre o user
    """
    try:
        # Log completo para debugging
        logger.info(f"🔍 DEBUG AUTH: {current_user}")
        
        # Retornar tudo que sabemos
        return {
            "authenticated": True,
            "user": {
                "id": str(current_user.id) if current_user.id else None,
                "email": current_user.email,
                "role": current_user.role,
                "citizen_id": str(current_user.citizen_id) if current_user.citizen_id else None,
                "sub": current_user.email,
                "username": current_user.username,
                "full_name": current_user.full_name,
                "is_active": current_user.is_active,
                "territory_id": str(current_user.territory_id) if current_user.territory_id else None
            },
            "permissions": {
                "can_access_citizen": current_user.role == "CITIZEN",
                "can_access_admin": current_user.role in ["ADMIN_SUPER", "ADMIN_CENTRAL", "ADMIN_PROVINCIAL", "ADMIN_MUNICIPAL", "ADMIN_COMMUNAL"],
                "has_citizen_id": current_user.citizen_id is not None
            },
            "recommended_dashboard": get_dashboard_for_role(current_user.role)
        }
    except Exception as e:
        logger.error(f"Erro no debug auth: {e}")
        return {"authenticated": False, "error": str(e)}


def get_dashboard_for_role(role: str) -> str:
    """Retorna o dashboard correto para cada papel"""
    dashboards = {
        "CITIZEN": "/citizen/portal",
        "ADMIN_SUPER": "/admin",
        "ADMIN_CENTRAL": "/admin",
        "ADMIN_PROVINCIAL": "/admin",
        "ADMIN_MUNICIPAL": "/admin",
        "ADMIN_COMMUNAL": "/admin"
    }
    return dashboards.get(role, "/login")
