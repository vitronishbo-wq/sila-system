"""
Exemplo de Migração para Usar BaseModel Centralizado

Este arquivo demonstra como migrar um modelo existente para usar
o BaseModel centralizado em core.db
"""

# ═════════════════════════════════════════════════════════════════════════════
# ANTES (Descentralizado - DEPRECIADO)
# ═════════════════════════════════════════════════════════════════════════════

# ❌ NÃO USE MAIS - Seu próprio Base em cada módulo:
# from sqlalchemy.orm import DeclarativeBase
# class Base(DeclarativeBase):
#     pass
#
# class OldUser(Base):
#     __tablename__ = "users"


# ═════════════════════════════════════════════════════════════════════════════
# DEPOIS (Centralizado - RECOMENDADO)
# ═════════════════════════════════════════════════════════════════════════════

from datetime import datetime
from sqlalchemy import DateTime, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base  # ✅ USE ISTO!


class User(Base):
    """
    Modelo de Usuário - usando BaseModel centralizado.
    
    Herda de core.db.Base que fornece:
    - Método __repr__ automático
    - to_dict() para serialização
    - to_json() para JSON
    - update(**kwargs) para atualização múltipla
    - Métodos de classe: get_table_name(), get_columns(), get_pk_column()
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Campos obrigatórios
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Campos opcionais
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Timestamps automáticos (adicionados por padrão)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


# ═════════════════════════════════════════════════════════════════════════════
# EXEMPLOS DE USO
# ═════════════════════════════════════════════════════════════════════════════

async def example_usage():
    """Exemplos de como usar o modelo com BaseModel centralizado."""
    
    
    # Criar novo usuário
    user = User(
        email="john@example.com",
        name="John Doe",
        phone="555-1234"
    )
    # created_at e updated_at são preenchidos automaticamente pelo banco
    
    # 1. Serializar para dicionário
    user_dict = user.to_dict()
    assert user_dict["email"] == "john@example.com"
    assert "created_at" in user_dict
    
    # 2. Serializar para JSON
    json_str = user.to_json()
    # {"id": 1, "email": "john@example.com", "name": "John Doe", ...}
    
    # 3. Atualizar múltiplos campos
    user.update(
        name="John Smith",
        phone="555-5678"
    )
    
    # 4. Representação legível
    print(user)
    # <User id=1 email='john@example.com' name='John Smith' phone='555-5678' ...>
    
    # 5. Info do modelo
    print(User.get_table_name())      # "users"
    print(User.get_columns())         # ["id", "email", "name", "phone", ...]
    print(User.get_pk_column())       # "id"


# ═════════════════════════════════════════════════════════════════════════════
# CASOS DE USO AVANÇADO
# ═════════════════════════════════════════════════════════════════════════════

# 1. Com UUID como Primary Key
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

class UserWithUUID(Base):
    __tablename__ = "users_uuid"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)


# 2. Com Soft Delete
class SoftDeletableUser(Base):
    __tablename__ = "users_soft_delete"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    
    # Soft Delete
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    def soft_delete(self):
        """Marca como deletado sem remover do banco."""
        from datetime import datetime, timezone
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)


# 3. Com Auditoria (created_by, updated_by)
class AuditedUser(Base):
    __tablename__ = "users_audited"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Auditoria
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(255), nullable=True)


__all__ = [
    "User",
    "UserWithUUID",
    "SoftDeletableUser",
    "AuditedUser",
]
