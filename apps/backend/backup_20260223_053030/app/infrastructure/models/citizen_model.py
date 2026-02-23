from sqlalchemy import Column, String, Date, Enum, Boolean, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime
from ...domain.enums import GenderEnum, MaritalStatusEnum, CitizenStatusEnum, VerificationLevelEnum

Base = declarative_base()

class CitizenModel(Base):
    __tablename__ = "citizen"
    __table_args__ = (
        UniqueConstraint("national_id_number", name="uq_citizen_national_id_number"),
        UniqueConstraint("nif", name="uq_citizen_nif"),
        UniqueConstraint("passport_number", name="uq_citizen_passport_number"),
        UniqueConstraint("social_security_number", name="uq_citizen_social_security_number"),
        Index("ix_citizen_full_name", "full_name"),
        Index("ix_citizen_national_id_number", "national_id_number"),
        Index("ix_citizen_nif", "nif"),
        Index("ix_citizen_phone", "phone"),
        Index("ix_citizen_province", "province"),
        Index("ix_citizen_status", "status"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    national_id_number = Column(String(32), nullable=False)
    nif = Column(String(32), nullable=False)
    passport_number = Column(String(32), nullable=True)
    social_security_number = Column(String(32), nullable=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    full_name = Column(String(128), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    birth_date = Column(Date, nullable=False)
    marital_status = Column(Enum(MaritalStatusEnum), nullable=False)
    nationality = Column(String(64), nullable=False)
    place_of_birth = Column(String(128), nullable=False)
    father_name = Column(String(128), nullable=False)
    mother_name = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=False)
    alternative_phone = Column(String(32), nullable=True)
    email = Column(String(128), nullable=False)
    province = Column(String(64), nullable=False)
    municipality = Column(String(64), nullable=False)
    commune = Column(String(64), nullable=False)
    neighborhood = Column(String(64), nullable=False)
    street = Column(String(128), nullable=False)
    house_number = Column(String(32), nullable=False)
    geo_coordinates = Column(String(64), nullable=True)
    status = Column(Enum(CitizenStatusEnum), nullable=False, default=CitizenStatusEnum.ACTIVE)
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_level = Column(Enum(VerificationLevelEnum), nullable=False, default=VerificationLevelEnum.BASIC)
    biometric_data = Column(String, nullable=True, comment="Campo reservado para dados biométricos futuros")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(64), nullable=False)
    updated_by = Column(String(64), nullable=False)
    # Foreign keys futuras
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True, index=True)
    household_id = Column(UUID(as_uuid=True), ForeignKey('household.id'), nullable=True, index=True)
    taxpayer_profile_id = Column(UUID(as_uuid=True), ForeignKey('taxpayer_profile.id'), nullable=True, index=True)
    employment_profile_id = Column(UUID(as_uuid=True), ForeignKey('employment_profile.id'), nullable=True, index=True)
    health_profile_id = Column(UUID(as_uuid=True), ForeignKey('health_profile.id'), nullable=True, index=True)
    education_profile_id = Column(UUID(as_uuid=True), ForeignKey('education_profile.id'), nullable=True, index=True)
