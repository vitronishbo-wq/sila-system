import uuid
import datetime
from sqlalchemy import String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.constants import EntityStatus

class Request(Base):
    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    citizen_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("citizen_fuc.citizen_id"), index=True, nullable=False)
    service_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=True)
    service_code: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default=EntityStatus.PENDING.value)
    data_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    
    # Territorial link (Local onde o pedido foi iniciado)
    territory_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("territories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Link para Processo (se existir)
    process_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
