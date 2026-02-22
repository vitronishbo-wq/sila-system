"""Case model for the justice module."""

"""Case model for the justice module."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.database import Base


class CaseType(str, Enum):
    """Types of legal cases."""

    CIVIL = "civil"
    CRIMINAL = "criminal"
    ADMINISTRATIVE = "administrative"
    FAMILY = "family"
    LABOR = "labor"
    COMMERCIAL = "commercial"
    CONSTITUTIONAL = "constitutional"
    FISCAL = "fiscal"


class CaseStatus(str, Enum):
    """Status of legal cases."""

    REGISTERED = "registered"
    IN_PROGRESS = "in_progress"
    SUSPENDED = "suspended"
    CONCLUDED = "concluded"
    ARCHIVED = "archived"
    APPEALED = "appealed"


class CasePriority(str, Enum):
    """Priority levels for cases."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Case(Base):
    """Legal case model representing judicial processes."""

    __tablename__ = "justice_cases"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    case_type = Column(SQLEnum(CaseType), nullable=False, index=True)
    status = Column(SQLEnum(CaseStatus), default=CaseStatus.REGISTERED, index=True)
    priority = Column(SQLEnum(CasePriority), default=CasePriority.MEDIUM)

    # Parties involved
    plaintiff_citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=True)
    defendant_citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=True)
    plaintiff_name = Column(String(200))  # For non-citizen plaintiffs
    defendant_name = Column(String(200))  # For non-citizen defendants

    # Court assignment
    court_id = Column(Integer, ForeignKey("justice_courts.id"), nullable=False)
    judge_name = Column(String(200))
    prosecutor_name = Column(String(200))

    # Dates
    filing_date = Column(DateTime, default=func.now(), nullable=False)
    hearing_date = Column(DateTime)
    conclusion_date = Column(DateTime)

    # Administrative
    created_by = Column(Integer, ForeignKey("justice_users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("justice_users.id"))
    is_public = Column(Boolean, default=False)  # Public access to case info
    is_confidential = Column(Boolean, default=False)  # Restricted access

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    court = relationship("Court", foreign_keys=[court_id], back_populates="cases")
    events = relationship(
        "CaseEvent", back_populates="case", cascade="all, delete-orphan"
    )
    documents = relationship(
        "LegalDocument", back_populates="case", cascade="all, delete-orphan"
    )

    # Foreign key relationships (to be defined when other modules are available)
    # plaintiff_citizen = relationship("Citizen", foreign_keys=[plaintiff_citizen_id])
    # defendant_citizen = relationship("Citizen", foreign_keys=[defendant_citizen_id])

    def __repr__(self):
        return f"<Case(case_number='{self.case_number}', title='{self.title}', status='{self.status}')>"

    @property
    def is_active(self) -> bool:
        """Check if case is currently active."""
        return self.status in [CaseStatus.REGISTERED, CaseStatus.IN_PROGRESS]

    @property
    def duration_days(self) -> Optional[int]:
        """Calculate case duration in days."""
        if self.conclusion_date:
            return (self.conclusion_date - self.filing_date).days
        return (datetime.utcnow() - self.filing_date).days

