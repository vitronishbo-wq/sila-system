from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.api.deps import get_db, get_current_user
from app.modules.statistics.kpis_service import KPIService
from app.core.events_unified import get_recent_events

router = APIRouter(prefix="/dashboard", tags=["admin-dashboard"])

@router.get("/")
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Dashboard com dados REAIS"""
    
    kpis = KPIService(db)
    
    # KPIs reais
    metrics = await kpis.get_dashboard_kpis()
    
    # Eventos recentes
    events = get_recent_events(20)
    
    # Atividade dos últimos 7 dias (real)
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    return {
        "metrics": metrics,
        "recent_events": events,
        "period": {
            "start": week_ago.isoformat(),
            "end": datetime.utcnow().isoformat()
        },
        "message": "Dashboard com dados reais da base"
    }
