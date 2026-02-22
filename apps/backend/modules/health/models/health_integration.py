# auto-generated placeholder
from sqlalchemy import Column, Integer

from config.database import Base  # Use centralized Base


class AlertStatus(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "health_alertstatuss"
    id = Column(Integer, primary_key=True)


class DiseaseCategory(Base):
    __tablename__ = "health_diseasecategorys"
    id = Column(Integer, primary_key=True)


class EpidemiologicalRecord(Base):
    __tablename__ = "health_epidemiologicalrecords"
    id = Column(Integer, primary_key=True)


class HealthAlert(Base):
    __tablename__ = "health_healthalerts"
    id = Column(Integer, primary_key=True)


class HealthFacility(Base):
    __tablename__ = "health_healthfacilitys"
    id = Column(Integer, primary_key=True)


class HealthProfessional(Base):
    __tablename__ = "health_healthprofessionals"
    id = Column(Integer, primary_key=True)


class HealthStatisticsSnapshot(Base):
    __tablename__ = "health_healthstatisticssnapshots"
    id = Column(Integer, primary_key=True)


class SeverityLevel(Base):
    __tablename__ = "health_severitylevels"
    id = Column(Integer, primary_key=True)

