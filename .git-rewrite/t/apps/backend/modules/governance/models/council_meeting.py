"""
Council Meeting Model for SILA Governance Module.

This model is aligned with the OpenAPI specification and Pydantic schemas,
ensuring full type safety and consistency across the stack.
"""

from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class CouncilMeeting(Base):
    """
    ORM model for council meetings.

    Represents municipal council meetings and decisions in the system.
    """

    __tablename__ = "governance_council_meetings"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Meeting fields
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    location = Column(String(200), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        String(50), nullable=False, default="scheduled", index=True
    )  # scheduled, in_progress, completed, canceled
    agenda = Column(JSON, nullable=True)  # JSON array of agenda items
    minutes = Column(JSON, nullable=True)  # JSON structure of meeting minutes
    decisions = Column(JSON, nullable=True)  # JSON array of decisions made
    participants = Column(
        JSON, nullable=True
    )  # JSON array of participant IDs and roles

    # Foreign key to council (optional, can be None if council model doesn't exist)
    council_id = Column(PostgreSQLUUID(as_uuid=True), nullable=True, index=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Soft delete
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Relationships
    decisions_rel = relationship("Decision", back_populates="meeting")

    def __repr__(self) -> str:
        return (
            f"<CouncilMeeting(id={self.id}, title={self.title}, status={self.status})>"
        )
