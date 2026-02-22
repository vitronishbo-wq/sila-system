from datetime import datetime, date
from typing import List, Optional
from enum import Enum
from sqlalchemy import String, Boolean, DateTime, JSON, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from config.database import Base


class AdministrativeLevel(str, Enum):
    CENTRAL = "CENTRAL"
    PROVINCIAL = "PROVINCIAL"
    MUNICIPAL = "MUNICIPAL"
    COMMUNAL = "COMMUNAL"
    LOCAL = "LOCAL"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, index=True, server_default=func.gen_random_uuid())
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    bi_number: Mapped[Optional[str]] = mapped_column(String(20), unique=True, index=True, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="active")

    administrative_level: Mapped[AdministrativeLevel] = mapped_column(String(20), default=AdministrativeLevel.LOCAL)
    region_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("locations.id"), nullable=True)

    roles: Mapped[List[str]] = mapped_column(JSON, default=lambda: ["user"], nullable=False)

    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    folders: Mapped[List["DocumentFolder"]] = relationship("DocumentFolder", back_populates="owner", cascade="all, delete-orphan")
    updates_bi: Mapped[List["AtualizacaoBI"]] = relationship("AtualizacaoBI", back_populates="user", cascade="all, delete-orphan")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="owner", cascade="all, delete-orphan")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.email} (Roles: {self.roles})>"

    def has_role(self, role: str) -> bool:
        return role in self.roles
