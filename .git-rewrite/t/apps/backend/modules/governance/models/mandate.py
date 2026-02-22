"""
Mandate Model for SILA Governance Module.

This model is aligned with the OpenAPI specification and Pydantic schemas,
ensuring full type safety and consistency across the stack.
"""

from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class Mandate(Base):
    """
    ORM model for governance mandates.

    Represents government mandates and authorizations in the system.
    """

    __tablename__ = "governance_mandates"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Mandate fields
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(2000), nullable=True)
    mandate_type = Column(
        String(100), nullable=True, index=True
    )  # executive, legislative, judicial, etc.
    issuing_authority = Column(String(200), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        String(50), nullable=False, default="active", index=True
    )  # active, expired, revoked
    scope = Column(JSON, nullable=True)  # JSON structure defining scope and limitations
    related_documents = Column(JSON, nullable=True)  # JSON array of document references

    # Foreign key to institution
    institution_id = Column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("governance_institutions.id"),
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
    institution = relationship(
        "Institution", foreign_keys=[institution_id], back_populates="mandates"
    )

    def __repr__(self) -> str:
        return f"<Mandate(id={self.id}, title={self.title}, status={self.status})>"
