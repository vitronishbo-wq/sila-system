import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.constants import UserRole, AdminLevel, ROLE_TO_LEVEL

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    
    # Role: Use valores do Enum UserRole - NEVER arbitrary strings
    role: Mapped[str] = mapped_column(String, default=UserRole.ADMIN_CENTRAL.value)
    
    # Level: MUST correspond to role (derived automatically)
    # Values: 'super', 'central', 'provincial', 'municipal', 'communal'
    level: Mapped[str] = mapped_column(String, default=AdminLevel.CENTRAL.value)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # � Vínculo com Cidadão (para cidadãos = users que existem no FUC)
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("citizen_fuc.citizen_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Liga ao cidadão no Ficheiro Único do Cidadão"
    )
    
    # �🗺️ Vínculo Territorial - Define a jurisdição do usuário
    territory_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("territories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Relacionamento com Territory
    territory: Mapped["Territory"] = relationship("Territory", foreign_keys=[territory_id])
