# auto-generated placeholder
from sqlalchemy import Column, Integer

from core.db.base_class import Base  # Use centralized Base


class TrainingEnrollment(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "training_trainingenrollments"
    id = Column(Integer, primary_key=True)


class TrainingProgram(Base):
    __tablename__ = "training_trainingprograms"
    id = Column(Integer, primary_key=True)
