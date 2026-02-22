"""
Serviço para dashboard - SILA System
Fase 1: Módulos Críticos
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.dashboard_stats import DashboardStats
from ..schemas.dashboard_stats import (
    DashboardStatsCreate,
    DashboardStatsSummary,
    DashboardStatsUpdate,
)


class DashboardService:
    """Serviço para gerenciar estatísticas do dashboard"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats_summary(self) -> DashboardStatsSummary:
        """Obtém resumo das estatísticas do sistema"""

        # Buscar estatísticas mais recentes
        result = await self.db.execute(
            select(DashboardStats).order_by(DashboardStats.updated_at.desc()).limit(1)
        )
        stats = result.scalar_one_or_none()

        if stats:
            return DashboardStatsSummary(
                total_users=stats.total_users,
                total_services=stats.total_services,
                active_requests=stats.pending_requests,
                completed_requests=stats.completed_requests,
                system_health=stats.system_health_status,
                last_updated=stats.updated_at,
            )

        # Se não há estatísticas, retornar dados básicos
        return DashboardStatsSummary(
            total_users=0,
            total_services=0,
            active_requests=0,
            completed_requests=0,
            system_health="unknown",
            last_updated=datetime.utcnow(),
        )

    async def get_detailed_stats(self) -> Optional[DashboardStats]:
        """Obtém estatísticas detalhadas"""

        result = await self.db.execute(
            select(DashboardStats).order_by(DashboardStats.updated_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def create_stats(self, stats_data: DashboardStatsCreate) -> DashboardStats:
        """Cria novas estatísticas"""

        db_stats = DashboardStats(**stats_data.dict())
        self.db.add(db_stats)
        await self.db.commit()
        await self.db.refresh(db_stats)
        return db_stats

    async def update_stats(
        self, stats_id: int, stats_data: DashboardStatsUpdate
    ) -> Optional[DashboardStats]:
        """Atualiza estatísticas existentes"""

        result = await self.db.execute(
            select(DashboardStats).where(DashboardStats.id == stats_id)
        )
        db_stats = result.scalar_one_or_none()

        if not db_stats:
            return None

        update_data = stats_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_stats, field, value)

        db_stats.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(db_stats)
        return db_stats

    async def get_service_stats(self, module: Optional[str] = None) -> Dict[str, Any]:
        """Obtém estatísticas por serviço/módulo"""

        # Query base para estatísticas de serviços
        query = select(
            func.count().label("total_requests"),
            func.sum(text("CASE WHEN status = 'completed' THEN 1 ELSE 0 END")).label(
                "completed"
            ),
            func.sum(text("CASE WHEN status = 'pending' THEN 1 ELSE 0 END")).label(
                "pending"
            ),
            func.sum(text("CASE WHEN status = 'rejected' THEN 1 ELSE 0 END")).label(
                "rejected"
            ),
        )

        if module:
            # Filtrar por módulo específico se fornecido
            # TODO: Implementar filtro por módulo quando a estrutura estiver definida
            pass

        result = await self.db.execute(query)
        stats = result.first()

        return {
            "total_requests": stats.total_requests or 0,
            "completed": stats.completed or 0,
            "pending": stats.pending or 0,
            "rejected": stats.rejected or 0,
            "completion_rate": (stats.completed or 0)
            / max(stats.total_requests or 1, 1)
            * 100,
        }

    async def calculate_real_time_stats(self) -> DashboardStatsSummary:
        """Calcula estatísticas em tempo real a partir dos dados atuais"""

        # TODO: Implementar consultas reais quando os modelos estiverem definidos
        # Por enquanto, retornar dados mockados

        return DashboardStatsSummary(
            total_users=1250,
            total_services=45,
            active_requests=234,
            completed_requests=1890,
            system_health="healthy",
            last_updated=datetime.utcnow(),
        )
