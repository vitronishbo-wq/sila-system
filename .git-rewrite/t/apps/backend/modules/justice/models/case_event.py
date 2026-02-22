"""Case event model for the justice module."""

from datetime import datetime
from enum import Enum

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

from core.db.base_class import Base


class EventType(str, Enum):
    """Types of case events."""

    HEARING = "hearing"
    DEPOSITION = "deposition"
    RULING = "ruling"
    SENTENCE = "sentence"
    APPEAL = "appeal"
    MOTION = "motion"
    EVIDENCE_SUBMISSION = "evidence_submission"
    WITNESS_TESTIMONY = "witness_testimony"
    EXPERT_REPORT = "expert_report"
    MEDIATION = "mediation"
    SETTLEMENT = "settlement"
    POSTPONEMENT = "postponement"
    DISMISSAL = "dismissal"


class EventStatus(str, Enum):
    """Status of case events."""

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class CaseEvent(Base):
    """Case event model representing judicial process movements."""

    __tablename__ = "justice_case_events"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(
        Integer, ForeignKey("justice_cases.id"), nullable=False, index=True
    )

    # Event details
    event_type = Column(SQLEnum(EventType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(EventStatus), default=EventStatus.SCHEDULED, index=True)

    # Scheduling
    scheduled_date = Column(DateTime, nullable=False)
    actual_date = Column(DateTime)
    duration_minutes = Column(Integer)
    location = Column(String(200))  # Courtroom, office, etc.

    # Participants
    judge_name = Column(String(200))
    prosecutor_name = Column(String(200))
    defense_attorney = Column(String(200))
    witnesses = Column(Text)  # JSON string of witness names

    # Outcomes
    outcome = Column(Text)
    next_steps = Column(Text)
    is_public = Column(Boolean, default=True)

    # Administrative
    created_by = Column(Integer, ForeignKey("justice_users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("justice_users.id"))

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    case = relationship("Case", foreign_keys=[case_id], back_populates="events")

    def __repr__(self):
        return f"<CaseEvent(case_id={self.case_id}, event_type='{self.event_type}', title='{self.title}')>"

    @property
    def is_completed(self) -> bool:
        """Check if event is completed."""
        return self.status == EventStatus.COMPLETED

    @property
    def is_upcoming(self) -> bool:
        """Check if event is scheduled for the future."""
        if self.status != EventStatus.SCHEDULED:
            return False
        return self.scheduled_date > datetime.utcnow()

    @property
    def is_overdue(self) -> bool:
        """Check if scheduled event is overdue."""
        if self.status != EventStatus.SCHEDULED:
            return False
        return self.scheduled_date < datetime.utcnow()
