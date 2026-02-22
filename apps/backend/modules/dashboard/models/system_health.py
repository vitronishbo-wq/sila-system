"""
Modelo para saúde do sistema - SILA System
Fase 1: Módulos Críticos
"""

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from config.database import Base


class SystemHealth(Base):
    """Modelo para monitoramento de saúde do sistema"""

    __tablename__ = "dashboard_system_health"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    # Informações do serviço
    service_name = Column(String(100), nullable=False, index=True)
    service_type = Column(String(50), nullable=False)  # api, database, cache, etc.

    # Status de saúde
    status = Column(String(20), nullable=False)  # healthy, warning, critical, down
    is_active = Column(Boolean, default=True, nullable=False)

    # Métricas de performance
    response_time = Column(Float, nullable=True)  # em milissegundos
    cpu_usage = Column(Float, nullable=True)  # porcentagem
    memory_usage = Column(Float, nullable=True)  # porcentagem
    disk_usage = Column(Float, nullable=True)  # porcentagem

    # Informações de conexão
    endpoint = Column(String(255), nullable=True)
    port = Column(Integer, nullable=True)

    # Detalhes adicionais
    last_check = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_error = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String(500), nullable=True)

    # Configurações específicas do serviço
    config = Column(JSON, nullable=True)

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
        return f"<SystemHealth(service={self.service_name}, status={self.status})>"

