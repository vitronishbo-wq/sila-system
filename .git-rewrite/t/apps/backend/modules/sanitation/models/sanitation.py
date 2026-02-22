# auto-generated placeholder
from sqlalchemy import Column, Integer

from core.db.base_class import Base  # Use centralized Base


class SanitationRecord(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "sanitation_sanitationrecords"
    id = Column(Integer, primary_key=True)


class SanitationType(Base):
    __tablename__ = "sanitation_sanitationtypes"
    id = Column(Integer, primary_key=True)
