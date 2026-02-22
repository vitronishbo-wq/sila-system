"""
Modelo para log de atividades - SILA System
Fase 1: Módulos Críticos
"""

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.database import Base


class ActivityLog(Base):
    """Modelo para log de atividades do sistema"""

    __tablename__ = "dashboard_activity_log"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    # Informações da atividade
    action = Column(
        String(100), nullable=False, index=True
    )  # login, create, update, delete, etc.
    resource_type = Column(
        String(50), nullable=False, index=True
    )  # user, service, document, etc.
    resource_id = Column(String(100), nullable=True, index=True)

    # Informações do usuário
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    user_email = Column(String(255), nullable=True, index=True)
    user_role = Column(String(50), nullable=True)

    # Detalhes da atividade
    description = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 ou IPv6
    user_agent = Column(String(500), nullable=True)

    # Resultado da operação
    status = Column(
        String(20), nullable=False, default="success"
    )  # success, error, warning
    status_code = Column(Integer, nullable=True)
    error_message = Column(String(500), nullable=True)

    # Dados relacionados (para auditoria)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    meta_data = Column(JSON, nullable=True)

    # Timestamps
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relacionamentos
    # Usar foreign_keys sem back_populates para evitar circular imports
    # O relacionamento User -> ActivityLog é opcional
    user = relationship("User", foreign_keys=[user_id], lazy="noload")

    def __repr__(self):
        return (
            f"<ActivityLog(id={self.id}, action={self.action}, user={self.user_email})>"
        )

