from datetime import datetime, date
from typing import List, Optional
from enum import Enum
from sqlalchemy import String, Boolean, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from config.database import Base


class AdministrativeLevel(str, Enum):
    CENTRAL = "CENTRAL"
    PROVINCIAL = "PROVINCIAL"
    MUNICIPAL = "MUNICIPAL"
    COMMUNAL = "COMMUNAL"
    LOCAL = "LOCAL"


class User(Base):
    """User model - Alinhado com schema real do BD PostgreSQL (2026-02-22)
    
    Tabela real: users
    Colunas reais:
    - id: INTEGER (PK, auto-increment)
    - uuid: VARCHAR (gen_random_uuid)
    - email: VARCHAR (unique)
    - hashed_password: VARCHAR
    - phone: VARCHAR (nullable)
    - bi_number: VARCHAR (unique, nullable)
    - is_active: BOOLEAN
    - is_verified: BOOLEAN
    - status: VARCHAR
    - level: VARCHAR (nullable, legacy)
    - region_id: INTEGER FK → locations.id (nullable)
    - roles: JSON (array de roles como string)
    - created_at: TIMESTAMP
    - updated_at: TIMESTAMP
    - last_login: TIMESTAMP (nullable)
    - full_name: VARCHAR (nullable)
    - administrative_level: VARCHAR (default='LOCAL')
    """
    
    __tablename__ = "users"

    # Primary Key (auto-increment INTEGER)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # UUID for external reference
    uuid: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False)
    
    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Personal Info - APENAS CAMPOS QUE EXISTEM NO BD
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # NÃO phone_number
    bi_number: Mapped[Optional[str]] = mapped_column(String(20), unique=True, index=True, nullable=True)
    
    # ⚠️ REMOVIDOS: address, birth_date, gender (não existem no BD)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False)
    
    # Authorization - Geographic level
    administrative_level: Mapped[str] = mapped_column(String(20), default="LOCAL", nullable=False)
    
    # ⚠️ REMOVIDO: level (coluna não existe no BD real)
    
    # Geographic assignment - FK to locations (NOT territories!)
    region_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Roles - stored as JSON array
    # Example: ["ADMIN", "USER"] or ["CITIZEN"]
    roles: Mapped[List[str]] = mapped_column(JSON, default=lambda: ["user"], nullable=False)

    # ⚠️ REMOVIDOS: Relacionamentos deixando para lazy loading via session
    # Para evitar circular imports e initialization errors
    # Use: session.refresh(user) ou desabilitar lazy loading se necessário

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.email} (Roles: {self.roles})>"

    def has_role(self, role: str) -> bool:
        return role in self.roles
