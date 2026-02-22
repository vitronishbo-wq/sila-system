import uuid
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.constants import UserRole


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Role: Foreign Key implícito via CHECK constraint + validação
    # Valores válidos: admin_super, admin_central, admin_provincial, admin_municipal, admin_communal
    role: Mapped[str] = mapped_column(String, nullable=False)
    
    # Service Code: apenas string, sem FK
    service_code: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True
    )
    
    # Permissões granulares
    can_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_write: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_approve: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Metadados (opcional)
    code: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # ...