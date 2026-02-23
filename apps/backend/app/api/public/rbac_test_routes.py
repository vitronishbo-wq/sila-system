"""
Routes para testar RBAC Territorial

Endpoints:
- GET /api/rbac/test/access - Verifica acesso do usuário
- GET /api/rbac/test/territory - Acesso territorial a um recurso
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from modules.identity.models.user import User
from sqlalchemy import text

router = APIRouter(prefix="/rbac/test", tags=["RBAC Testing"])


@router.get("/access")
async def check_access(current_user: User = Depends(get_current_user)):
    """
    Verifica acesso do usuário autenticado.
    
    Retorna detalhes de território e permissões.
    """
    return {
        "email": current_user.email,
        "role": current_user.role,
        "level": current_user.level,
        "territory_id": str(current_user.territory_id) if current_user.territory_id else None,
        "is_national": current_user.territory_id is None,
        "can_access_all_territories": current_user.territory_id is None,
        "message": "✅ Você está autenticado" if current_user else "❌ Não autenticado"
    }


@router.get("/territory/{territory_id}")
async def check_territory_access(
    territory_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Testa acesso territorial a um recurso específico.
    
    - Se territory_id do usuário é NULL (CENTRAL) → acesso a TUDO ✅
    - Se user_territory está na closure table como ANCESTOR de resource_territory → acesso ✅
    - Senão → NEGADO ❌
    """
    
    # CENTRAL admin pode acessar tudo
    if current_user.territory_id is None:
        return {
            "user_email": current_user.email,
            "user_territory": "NACIONAL (Central Admin)",
            "resource_territory": territory_id,
            "access_granted": True,
            "reason": "✅ Você é ADMIN_CENTRAL - acesso a todo o sistema",
            "message": "✅ Você tem acesso a este território"
        }
    
    # Usuário com territorio_id precisa validar contra closure table
    # Verifica se user.territory_id é ancestral (ou igual) ao resource territory_id
    query = """
    SELECT 1 FROM territory_closure 
    WHERE ancestor_id = CAST(:ancestor_id AS UUID) 
      AND descendant_id = CAST(:descendant_id AS UUID)
    LIMIT 1
    """
    
    result = await db.execute(
        text(query),
        {"ancestor_id": str(current_user.territory_id), "descendant_id": str(territory_id)}
    )
    
    has_access = result.scalar() is not None
    
    if has_access:
        return {
            "user_email": current_user.email,
            "user_territory": str(current_user.territory_id),
            "resource_territory": territory_id,
            "access_granted": True,
            "reason": "✅ Você tem jurisdição sobre este território",
            "message": "✅ Você tem acesso a este território"
        }
    else:
        raise HTTPException(
            status_code=403,
            detail=f"❌ Acesso negado: você não tem permissão para acessar este território"
        )


@router.get("/hierarchy-test")
async def hierarchy_test(current_user: User = Depends(get_current_user)):
    """
    Testa hierarquia territorial do usuário.
    
    Retorna informações sobre a posição do usuário na hierarquia.
    """
    
    level_description = {
        "national": "Administrador Nacional - Vê toda Angola",
        "provincial": "Administrador Provincial - Vê própria província + municipalidades + comunas",
        "municipal": "Administrador Municipal - Vê próprio município + comunas",
        "communal": "Administrador Comunal - Vê própria comuna apenas",
        "local": "Cidadão - Vê apenas contexto pessoal",
    }
    
    return {
        "email": current_user.email,
        "role": current_user.role,
        "level": current_user.level,
        "level_description": level_description.get(current_user.level, "Desconhecido"),
        "territory_id": str(current_user.territory_id) if current_user.territory_id else None,
        "access_scope": "🌍 NACIONAL (vê tudo)" if current_user.territory_id is None else f"📍 TERRITORIAL ({current_user.territory_id})",
    }
