"""
API de Dashboard por Perfil de Utilizador
Cada perfil vê EXATAMENTE o que deve ver.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import UUID

from app.api.deps import get_db, get_current_user
from modules.identity.models.user import User
from app.citizen.core.profile_queries import ProfileQueries

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


async def get_current_user_info(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Extrair informações do utilizador autenticado"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Não autenticado")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "territory_id": current_user.territory_id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "citizen_id": current_user.citizen_id
    }


@router.get("/meu-dashboard")
async def get_my_dashboard(
    current_user: Dict[str, Any] = Depends(get_current_user_info),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    🎯 ÚNICO endpoint para todos os perfis administrativos
    O sistema decide qual dashboard entregar baseado no perfil do utilizador
    
    Query: /admin/dashboard/meu-dashboard
    """
    
    try:
        role = current_user.role
        user_id = current_user.id
        
        # ===== PERFIL 1: Comuna =====
        if role in ["ADMIN_COMMUNAL"]:
            commune_id = current_user.territory_id
            if not commune_id:
                raise HTTPException(status_code=400, detail="Utilizador sem comuna associada")
            
            return ProfileQueries.get_commune_dashboard(
                db, 
                UUID(str(commune_id)) if isinstance(commune_id, str) else commune_id,
                user_id=UUID(str(user_id)) if user_id and isinstance(user_id, str) else user_id
            )
        
        # ===== PERFIL 2: Município =====
        elif role == "ADMIN_MUNICIPAL":
            municipality_id = current_user.territory_id
            if not municipality_id:
                raise HTTPException(status_code=400, detail="Utilizador sem município associado")
            
            return ProfileQueries.get_municipality_dashboard(
                db, 
                UUID(str(municipality_id)) if isinstance(municipality_id, str) else municipality_id
            )
        
        # ===== PERFIL 3: Província =====
        elif role == "ADMIN_PROVINCIAL":
            province_id = current_user.territory_id
            if not province_id:
                raise HTTPException(status_code=400, detail="Utilizador sem província associada")
            
            return ProfileQueries.get_province_dashboard(
                db, 
                UUID(str(province_id)) if isinstance(province_id, str) else province_id
            )
        
        # ===== PERFIL 4: Central =====
        elif role in ["ADMIN_CENTRAL", "ADMIN_SUPER"]:
            return ProfileQueries.get_central_dashboard(db)
        
        else:
            raise HTTPException(
                status_code=403, 
                detail=f"Perfil '{role}' não tem dashboard definido"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar dashboard: {str(e)}")


@router.get("/central")
async def get_central_dashboard(
    current_user: Dict[str, Any] = Depends(get_current_user_info),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Dashboard de governança nacional (Central)"""
    
    # Validar permissão
    if current_user.get("role") not in ["central_admin", "system_admin"]:
        raise HTTPException(status_code=403, detail="Apenas Central tem acesso")
    
    try:
        return ProfileQueries.get_central_dashboard(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/commune/{commune_id}")
async def get_commune_dashboard(
    commune_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_info),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Dashboard da Comuna - execução pura"""
    
    # Validar permissão: deve ser da mesma comuna ou admin
    user_territory = str(current_user.get("territory_id") or current_user.get("commune_id") or "")
    if current_user.get("role") not in ["commune_admin", "system_admin"] or (user_territory and user_territory != commune_id):
        if current_user.get("role") not in ["system_admin"]:
            raise HTTPException(status_code=403, detail="Sem permissão para esta comuna")
    
    try:
        return ProfileQueries.get_commune_dashboard(db, UUID(commune_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="commune_id inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/municipality/{municipality_id}")
async def get_municipality_dashboard(
    municipality_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_info),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Dashboard do Município - supervisão e escalados"""
    
    # Validar permissão
    if current_user.get("role") not in ["municipality_admin", "system_admin"]:
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    try:
        return ProfileQueries.get_municipality_dashboard(db, UUID(municipality_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="municipality_id inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/province/{province_id}")
async def get_province_dashboard(
    province_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_info),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Dashboard da Província - exceções e casos críticos"""
    
    # Validar permissão
    if current_user.get("role") not in ["province_admin", "system_admin"]:
        raise HTTPException(status_code=403, detail="Sem permissão")
    
    try:
        return ProfileQueries.get_province_dashboard(db, UUID(province_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="province_id inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audit-trail")
async def get_audit_trail(
    days: int = 30,
    current_user: Dict[str, Any] = Depends(get_current_user_info),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Auditoria completa - APENAS Central"""
    
    # Validar permissão
    if current_user.get("role") not in ["central_admin", "system_admin"]:
        raise HTTPException(status_code=403, detail="Apenas Central tem acesso a auditoria")
    
    try:
        return ProfileQueries.get_audit_trail(db, days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

