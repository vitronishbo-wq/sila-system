"""Add health table indexes migration"""

from alembic import op


def upgrade():
    """Create indexes for performance"""
    op.create_index("ix_appointments_citizen_id", "appointments", ["citizen_id"])
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"])
    op.create_index("ix_appointments_health_unit_id", "appointments", ["health_unit_id"])
    op.create_index("ix_appointments_status", "appointments", ["status"])
    op.create_index("ix_appointments_appointment_date", "appointments", ["appointment_date"])
    op.create_index(
        "ix_appointments_citizen_date", "appointments", ["citizen_id", "appointment_date"]
    )
    op.create_index("ix_prescriptions_citizen_id", "prescriptions", ["citizen_id"])
    op.create_index("ix_prescriptions_doctor_id", "prescriptions", ["doctor_id"])
    op.create_index("ix_prescriptions_status", "prescriptions", ["status"])
    op.create_index("ix_medical_records_citizen_id", "medical_records", ["citizen_id"])
    op.create_index("ix_medical_records_doctor_id", "medical_records", ["doctor_id"])
    op.create_index("ix_medical_records_health_unit_id", "medical_records", ["health_unit_id"])
    op.create_index("ix_vaccine_doses_citizen_id", "vaccine_doses", ["citizen_id"])
    op.create_index("ix_vaccine_doses_vaccine_id", "vaccine_doses", ["vaccine_id"])
    op.create_index("ix_health_units_municipality", "health_units", ["municipality"])
    op.create_index("ix_health_units_unit_type", "health_units", ["unit_type"])
    op.create_index("ix_exam_requests_citizen_id", "exam_requests", ["citizen_id"])
    op.create_index("ix_exam_requests_doctor_id", "exam_requests", ["doctor_id"])
    op.create_index("ix_exam_requests_status", "exam_requests", ["status"])


def downgrade():
    """Drop indexes"""
    op.drop_index("ix_exam_requests_status")
    op.drop_index("ix_exam_requests_doctor_id")
    op.drop_index("ix_exam_requests_citizen_id")
    op.drop_index("ix_health_units_unit_type")
    op.drop_index("ix_health_units_municipality")
    op.drop_index("ix_vaccine_doses_vaccine_id")
    op.drop_index("ix_vaccine_doses_citizen_id")
    op.drop_index("ix_medical_records_health_unit_id")
    op.drop_index("ix_medical_records_doctor_id")
    op.drop_index("ix_medical_records_citizen_id")
    op.drop_index("ix_prescriptions_status")
    op.drop_index("ix_prescriptions_doctor_id")
    op.drop_index("ix_prescriptions_citizen_id")
    op.drop_index("ix_appointments_citizen_date")
    op.drop_index("ix_appointments_appointment_date")
    op.drop_index("ix_appointments_status")
    op.drop_index("ix_appointments_health_unit_id")
    op.drop_index("ix_appointments_doctor_id")
    op.drop_index("ix_appointments_citizen_id")
