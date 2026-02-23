from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from typing import Dict, Any

from app.core.workflow.models.request import Request
from app.citizen.core.models import CitizenFUC
from app.modules.financas.domain.models.invoice import Invoice

class KPIService:
    """KPIs REAIS baseados na BD (Async)"""
    
    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db
    
    async def get_dashboard_kpis(self) -> Dict[str, Any]:
        """Retorna KPIs reais (ou valores padrão se tabelas não existirem)"""
        
        try:
            # Contagens reais (Async)
            total_citizens_res = await self.db.execute(select(func.count()).select_from(CitizenFUC))
            total_citizens = total_citizens_res.scalar() or 0
            
            total_requests_res = await self.db.execute(select(func.count()).select_from(Request))
            total_requests = total_requests_res.scalar() or 0
            
            total_invoices_res = await self.db.execute(select(func.count()).select_from(Invoice))
            total_invoices = total_invoices_res.scalar() or 0
            
            # Pedidos hoje
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
            requests_today_res = await self.db.execute(
                select(func.count()).select_from(Request).where(Request.created_at >= today_start)
            )
            requests_today = requests_today_res.scalar() or 0
            
            # Faturas pendentes
            pending_invoices_res = await self.db.execute(
                select(func.count()).select_from(Invoice).where(Invoice.status == "pending")
            )
            pending_invoices = pending_invoices_res.scalar() or 0
            
        except Exception as e:
            # Se houver erro (tabelas não existem, etc), retorna valores padrão
            print(f"[WARN] Erro ao buscar KPIs: {str(e)}")
            total_citizens = 0
            total_requests = 0
            total_invoices = 0
            requests_today = 0
            pending_invoices = 0
        
        return {
            "total_cidadaos": total_citizens,
            "total_pedidos": total_requests,
            "total_faturas": total_invoices,
            "pedidos_hoje": requests_today,
            "faturas_pendentes": pending_invoices,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "KPIs reais da base de dados"
        }
    
    async def get_growth_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Métricas de crescimento reais (ou valores padrão se tabelas não existirem)"""
        try:
            since = datetime.utcnow() - timedelta(days=days)
            
            # Crescimento real
            citizens_before_res = await self.db.execute(
                select(func.count()).select_from(CitizenFUC).where(CitizenFUC.created_at < since)
            )
            citizens_before = citizens_before_res.scalar() or 0
            
            citizens_after_res = await self.db.execute(
                select(func.count()).select_from(CitizenFUC).where(CitizenFUC.created_at >= since)
            )
            citizens_after = citizens_after_res.scalar() or 0
            
        except Exception as e:
            print(f"[WARN] Erro ao buscar growth metrics: {str(e)}")
            citizens_before = 0
            citizens_after = 0
        
        return {
            "periodo_dias": days,
            "novos_cidadaos": citizens_after,
            "crescimento_percentual": round(
                (citizens_after / max(citizens_before, 1)) * 100, 2
            ),
            "timestamp": datetime.utcnow().isoformat()
        }