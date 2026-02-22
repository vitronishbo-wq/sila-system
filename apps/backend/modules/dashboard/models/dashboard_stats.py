"""
Modelo para estatísticas do dashboard - SILA System
Fase 1: Módulos Críticos
"""

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from config.database import Base


class DashboardStats(Base):
    """Modelo para estatísticas gerais do sistema"""

    __tablename__ = "dashboard_stats"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    # Estatísticas de usuários
    total_users = Column(Integer, default=0, nullable=False)
    active_users = Column(Integer, default=0, nullable=False)
    new_users_today = Column(Integer, default=0, nullable=False)

    # Estatísticas de serviços
    total_services = Column(Integer, default=0, nullable=False)
    active_services = Column(Integer, default=0, nullable=False)
    services_usage_count = Column(Integer, default=0, nullable=False)

    # Estatísticas de requisições
    total_requests = Column(Integer, default=0, nullable=False)
    pending_requests = Column(Integer, default=0, nullable=False)
    completed_requests = Column(Integer, default=0, nullable=False)
    rejected_requests = Column(Integer, default=0, nullable=False)

    # Métricas de performance
    avg_response_time = Column(Float, default=0.0, nullable=False)
    system_uptime = Column(Float, default=0.0, nullable=False)

    # Status do sistema
    system_health_status = Column(String(20), default="healthy", nullable=False)
    last_error_time = Column(DateTime, nullable=True)

    # Metadados
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<DashboardStats(id={self.id}, users={self.total_users}, services={self.total_services})>"

