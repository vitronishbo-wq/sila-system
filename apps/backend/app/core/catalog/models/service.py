import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer, Numeric, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

class Service(Base):
    __tablename__ = 'services'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scope: Mapped[str] = mapped_column(String, default='public')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    module_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('modules.id', ondelete='SET NULL'), nullable=True, index=True)
    module = relationship('Module', back_populates='services')
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))
    estimated_days: Mapped[int] = mapped_column(Integer, default=5)
    workflow_definition_key: Mapped[str | None] = mapped_column(String(120), nullable=True)
    required_documents: Mapped[list[str]] = mapped_column(JSON, default=list)
    visibility: Mapped[str] = mapped_column(String(20), default='PUBLIC')
    version: Mapped[int] = mapped_column(Integer, default=1)
    business_priority: Mapped[int] = mapped_column(Integer, default=100)
    territory_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey('locations.id', ondelete='SET NULL'), nullable=True, index=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_essential: Mapped[bool] = mapped_column(Boolean, default=False)
    icon_slug: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)