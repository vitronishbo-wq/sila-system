from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base

class AuditLog(Base):
    """
    Institutional Audit Log for tracking critical actions and traceability.
    """
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=True, default={})
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow,
        index=True
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")

