"""Identity domain models (ORM) for SILA System."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base

if TYPE_CHECKING:
    from modules.identity.models.user import User


class Identity(Base):
    """ORM model representando documentos de identidade (BI, NIF, Passaporte)."""

    __tablename__ = "identities"
    __table_args__ = {"extend_existing": True}

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    identity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # BI, NIF, etc.
    identity_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    issued_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relacionamento
    # Relacionamento (Usando backref para evitar dependência circular na definição do User)
    user: Mapped["modules.identity.models.user.User"] = relationship("modules.identity.models.user.User", backref="identities")
