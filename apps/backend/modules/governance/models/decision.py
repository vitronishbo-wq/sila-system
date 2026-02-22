"""
Decision Model for SILA Governance Module.

This model is aligned with the OpenAPI specification and Pydantic schemas,
ensuring full type safety and consistency across the stack.
"""

from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import relationship

from config.database import Base


class Decision(Base):
    """
    ORM model for governance decisions.

    Represents governance decisions and resolutions in the system.
    """

    __tablename__ = "governance_decisions"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Decision fields
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    decision_type = Column(
        String(100), nullable=True, index=True
    )  # policy, resolution, directive, etc.
    status = Column(
        String(50), nullable=False, default="proposed", index=True
    )  # proposed, approved, rejected, implemented
    voting_record = Column(
        JSON, nullable=True
    )  # JSON array of votes (member_id, vote, timestamp)
    effective_date = Column(DateTime(timezone=True), nullable=True)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    related_documents = Column(JSON, nullable=True)  # JSON array of document references

    # Foreign key to council meeting
    meeting_id = Column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("governance_council_meetings.id"),
        nullable=True,
        index=True,
    )

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
    meeting = relationship(
        "CouncilMeeting", foreign_keys=[meeting_id], back_populates="decisions_rel"
    )

    def __repr__(self) -> str:
        return f"<Decision(id={self.id}, title={self.title}, status={self.status})>"

