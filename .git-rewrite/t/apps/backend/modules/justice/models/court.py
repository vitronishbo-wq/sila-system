"""Court model for the justice module."""

from enum import Enum

from sqlalchemy import (
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


class CourtType(str, Enum):
    """Types of courts in Angola."""

    SUPREME = "supreme"  # Tribunal Supremo
    CONSTITUTIONAL = "constitutional"  # Tribunal Constitucional
    ACCOUNTS = "accounts"  # Tribunal de Contas
    PROVINCIAL = "provincial"  # Tribunal Provincial
    MUNICIPAL = "municipal"  # Tribunal Municipal
    COMMUNAL = "communal"  # Tribunal Comunal
    SPECIALIZED = "specialized"  # Tribunais Especializados
    MILITARY = "military"  # Tribunal Militar


class CourtJurisdiction(str, Enum):
    """Jurisdiction levels of courts."""

    NATIONAL = "national"
    PROVINCIAL = "provincial"
    MUNICIPAL = "municipal"
    COMMUNAL = "communal"
    SPECIALIZED = "specialized"


class CourtStatus(str, Enum):
    """Operational status of courts."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    MAINTENANCE = "maintenance"


class Court(Base):
    """Court model representing judicial institutions."""

    __tablename__ = "justice_courts"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    # Basic information
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    court_type = Column(SQLEnum(CourtType), nullable=False, index=True)
    jurisdiction = Column(SQLEnum(CourtJurisdiction), nullable=False, index=True)
    status = Column(SQLEnum(CourtStatus), default=CourtStatus.ACTIVE, index=True)

    # Location information
    province_id = Column(
        Integer, ForeignKey("justice_province.id"), nullable=False, index=True
    )
    municipality_id = Column(Integer, ForeignKey("justice_municipality.id"), index=True)
    commune_id = Column(Integer, ForeignKey("justice_commune.id"), index=True)
    address = Column(Text)
    postal_code = Column(String(20))

    # Contact information
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(200))

    # Administrative details
    chief_judge = Column(String(200))
    secretary = Column(String(200))
    total_judges = Column(Integer, default=1)
    courtrooms = Column(Integer, default=1)

    # Operating information
    operating_hours = Column(String(100))  # e.g., "08:00-17:00"
    languages = Column(String(200))  # Supported languages
    specializations = Column(Text)  # JSON string of specializations

    # Capacity and workload
    max_cases_per_month = Column(Integer)
    current_case_load = Column(Integer, default=0)

    # Administrative
    created_by = Column(Integer, ForeignKey("justice_users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("justice_users.id"))

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    cases = relationship("Case", back_populates="court")

    def __repr__(self):
        return (
            f"<Court(code='{self.code}', name='{self.name}', type='{self.court_type}')>"
        )

    @property
    def is_operational(self) -> bool:
        """Check if court is operational."""
        return self.status == CourtStatus.ACTIVE

    @property
    def capacity_utilization(self) -> float:
        """Calculate current capacity utilization percentage."""
        if not self.max_cases_per_month or self.max_cases_per_month == 0:
            return 0.0
        return (self.current_case_load / self.max_cases_per_month) * 100

    @property
    def is_overloaded(self) -> bool:
        """Check if court is overloaded (>90% capacity)."""
        return self.capacity_utilization > 90.0

    @property
    def full_location(self) -> str:
        """Get full location string from related location models."""
        parts = []
        if self.province_id:
            parts.append(f"Província {self.province_id}")
        if self.municipality_id:
            parts.append(f"Município {self.municipality_id}")
        if self.commune_id:
            parts.append(f"Comuna {self.commune_id}")
        return ", ".join(parts)
