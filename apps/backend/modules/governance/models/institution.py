"""
Institution Model for SILA Governance Module.

This model is aligned with the OpenAPI specification and Pydantic schemas,
ensuring full type safety and consistency across the stack.
"""

from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import relationship

from config.database import Base


class Institution(Base):
    """
    ORM model for governance institutions.

    Represents government institutions and organizations in the system.
    """

    __tablename__ = "governance_institutions"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Institution fields
    name = Column(String(200), nullable=False, index=True)
    acronym = Column(String(50), nullable=True)
    institution_type = Column(
        String(100), nullable=True, index=True
    )  # ministry, agency, department, etc.
    jurisdiction = Column(String(200), nullable=True)
    description = Column(String(2000), nullable=True)
    founding_date = Column(DateTime(timezone=True), nullable=True)
    website = Column(String(200), nullable=True)
    contact_info = Column(JSON, nullable=True)  # JSON structure with contact details
    leadership = Column(JSON, nullable=True)  # JSON array of leaders and their roles

    # Foreign key to parent institution
    parent_institution_id = Column(
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
    parent_institution = relationship(
        "Institution", remote_side=[id], backref="departments"
    )
    mandates = relationship("Mandate", back_populates="institution")

    def __repr__(self) -> str:
        return f"<Institution(id={self.id}, name={self.name}, type={self.institution_type})>"

