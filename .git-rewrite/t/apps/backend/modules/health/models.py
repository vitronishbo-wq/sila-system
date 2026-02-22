"""
Health module ORM models.

These models are aligned with the OpenAPI specification and Pydantic schemas
from Phase 2, ensuring full type safety and consistency across the stack.
"""

from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class HealthRecord(Base):
    """
    ORM model for health records.

    Represents a medical record in the system, linked to a user.
    """

    __tablename__ = "health_records"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Foreign key to users table
    user_id = Column(
        PostgreSQLUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # Health record fields (aligned with OpenAPI)
    patient_name = Column(String(255), nullable=True)
    diagnosis = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

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
    user = relationship("User", backref="health_records")

    def __repr__(self) -> str:
        return f"<HealthRecord(id={self.id}, patient_name={self.patient_name})>"


class HealthService(Base):
    """
    ORM model for health services.

    Represents available medical services (consultations, exams, vaccines, etc.).
    """

    __tablename__ = "health_services"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Service information
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(
        String(100), nullable=True, index=True
    )  # consulta, exame, vacina, etc.
    status = Column(
        String(50), nullable=False, default="available", index=True
    )  # available, unavailable

    # Additional metadata
    estimated_duration = Column(String(50), nullable=True)  # Duration in minutes
    requirements = Column(Text, nullable=True)  # JSON or comma-separated requirements

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
    appointments = relationship("Appointment", back_populates="service")

    def __repr__(self) -> str:
        return (
            f"<HealthService(id={self.id}, name={self.name}, category={self.category})>"
        )


class Appointment(Base):
    """
    ORM model for medical appointments.

    Represents a scheduled appointment for a medical service.
    """

    __tablename__ = "health_appointments"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Foreign keys
    user_id = Column(
        PostgreSQLUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    service_id = Column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("health_services.id"),
        nullable=False,
        index=True,
    )

    # Appointment details
    scheduled_date = Column(DateTime(timezone=True), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    status = Column(
        String(50), nullable=False, default="scheduled", index=True
    )  # scheduled, confirmed, completed, cancelled

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
    user = relationship("User", backref="appointments")
    service = relationship("HealthService", back_populates="appointments")
    medical_record = relationship(
        "MedicalRecord", back_populates="appointment", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Appointment(id={self.id}, user_id={self.user_id}, scheduled_date={self.scheduled_date})>"


class MedicalRecord(Base):
    """
    ORM model for medical records.

    Represents a medical record (prontuário) related to an appointment.
    """

    __tablename__ = "health_medical_records"
    __table_args__ = {"extend_existing": True}

    # Primary key with UUID
    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    # Foreign key to appointment
    appointment_id = Column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("appointments.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Medical record information
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

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
    appointment = relationship("Appointment", back_populates="medical_record")

    def __repr__(self) -> str:
        return f"<MedicalRecord(id={self.id}, appointment_id={self.appointment_id})>"


__all__ = [
    "HealthRecord",
    "HealthService",
    "Appointment",
    "MedicalRecord",
]
