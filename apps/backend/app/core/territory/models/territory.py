import uuid

from apps.backend.app.core.db import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Territory(Base):
    __tablename__ = "locations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, index=True)
    type: Mapped[str] = mapped_column(String)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"), nullable=True
    )
    parent = relationship("Territory", remote_side=[id], back_populates="children")
    children = relationship("Territory", back_populates="parent", cascade="all, delete")
