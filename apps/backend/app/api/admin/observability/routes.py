from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import get_current_user, get_current_admin_user, get_db
from app.core.constants import UserRole
from modules.identity.models.user import User
from app.core.territory.models.territory import Territory

router = APIRouter(prefix="/observability", tags=["Observability"])

def resolve_kpi_scope(user: User, scope: str | None = None, municipality_id: UUID | None = None):
    """
    Resolve and validate scope based on User Role.
    """
    role = user.role
    
    # 1. SUPER ADMIN: Can access everything
    if role == UserRole.ADMIN_SUPER:
        return scope or "global", municipality_id

    # 2. CENTRAL ADMIN: Only Global scope allowed
    if role == UserRole.ADMIN_CENTRAL:
        if scope and scope != "global":
             raise HTTPException(status_code=403, detail="Central Admin is restricted to Global scope.")
        return "global", None

    # 3. MUNICIPAL ADMIN: Only Municipal scope for THEIR municipality
    if role == UserRole.ADMIN_MUNICIPAL:
        if scope != "municipal":
             raise HTTPException(status_code=403, detail="Municipal Admin is restricted to Municipal scope.")
        
        # Must provide municipality_id OR fallback to user's territory if linked
        target_mun_id = municipality_id or user.territory_id
        
        if not target_mun_id:
             raise HTTPException(status_code=400, detail="Municipality context missing for Municipal Admin.")
             
        # Verification: Is the user actually from this territory? (Simplified check)
        # In a real scenario we'd check strict hierarchy. For now, we assume user.territory_id is the boundary.
        if user.territory_id and str(target_mun_id) != str(user.territory_id):
             raise HTTPException(status_code=403, detail="Access denied to this territory.")

        return "municipal", target_mun_id

    # 4. OTHERS (Provincial/Communal/Agente): Deny for now as per instructions
    raise HTTPException(status_code=403, detail="Role not authorized to access KPIs.")


@router.get("/kpis")
async def kpis(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
    scope: str | None = Query(None, description="Scope of KPIs: global, municipal"),
    municipality_id: UUID | None = Query(None, description="Target Municipality ID for municipal scope")
):
    """
    Get Key Performance Indicators (Users, Territories, etc).
    Enforces strict RBAC via resolve_kpi_scope.
    """
    resolved_scope, target_id = resolve_kpi_scope(current_user, scope, municipality_id)
    
    # Base queries
    users_query = select(func.count()).select_from(User)
    territories_query = select(func.count()).select_from(Territory)

    # Filter based on resolved scope
    if resolved_scope == "municipal" and target_id:
        # For a full implementation, we'd join Territory to check hierarchy. 
        # Here we mock filtering by assuming users have a direct territory_id or we filter territories by parent.
        # This is a simplified "Green" implementation.
        users_query = users_query.where(User.territory_id == target_id)
        # For territories, we might count communes within this municipality
        territories_query = territories_query.where(Territory.parent_id == target_id)

    total_users = await db.scalar(users_query)
    total_territories = await db.scalar(territories_query)

    return {
        "kpis": {
            "users": total_users,
            "territories": total_territories,
             # Mocked business kpis
            "services": 14, 
            "requests": 0
        },
        "meta": {
            "scope": resolved_scope,
            "target_id": str(target_id) if target_id else None,
            "health": "green"
        }
    }

