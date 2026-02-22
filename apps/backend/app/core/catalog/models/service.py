import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    scope: Mapped[str] = mapped_column(String, default="public")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relacionamento com Módulo (NOVO - Arquitectura Modular)
    module_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("modules.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    module = relationship("Module", back_populates="services")
    
    # Preço/Emolumento do serviço
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    
    # Prazo estimado em dias
    estimated_days: Mapped[int] = mapped_column(Integer, default=5)
    
    # Territorial link (Optional for global services)
    territory_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("territories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Indicador de serviço público (visível para todos)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Indicador de serviço essencial para a homepage
    is_essential: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Identificador do ícone para o frontend
    icon_slug: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # Timestamp de última atualização
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)