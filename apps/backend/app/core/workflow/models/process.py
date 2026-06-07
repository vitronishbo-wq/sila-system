import uuid

from apps.backend.app.core.db import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class Process(Base):
    __tablename__ = "processes"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"))
    citizen_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("citizen_fuc.citizen_id")
    )
    status: Mapped[str] = mapped_column(String(50), default="submitted")
    current_step: Mapped[str | None] = mapped_column(String(100), nullable=True)
