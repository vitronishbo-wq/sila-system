"""Create health tables migration"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    """Create health tables"""
    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_number", sa.String(50), nullable=True),
        sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("doctor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("health_unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_type", sa.String(50), nullable=False),
        sa.Column("specialty", sa.String(100), nullable=False),
        sa.Column("appointment_date", sa.Date(), nullable=False),
        sa.Column("appointment_time", sa.Time(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("status", sa.String(50), nullable=False, server_default="AGENDADA"),
        sa.Column("priority", sa.String(20), nullable=False, server_default="MEDIA"),
        sa.Column("reason", sa.String(500), nullable=False),
        sa.Column("symptoms", sa.String(1000), nullable=True),
        sa.Column("notes", sa.String(2000), nullable=True),
        sa.Column("workflow_instance_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("workflow_data", postgresql.JSON(), nullable=True),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_reason", sa.String(500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("appointment_number"),
    )
    op.create_table(
        "prescriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("prescription_number", sa.String(50), nullable=True),
        sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("doctor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("health_unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("items", postgresql.JSON(), nullable=True),
        sa.Column("clinical_notes", sa.String(2000), nullable=True),
        sa.Column("recommendations", sa.String(2000), nullable=True),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="ATIVA"),
        sa.Column("workflow_instance_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dispensed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("prescription_number"),
    )
    op.create_table(
        "medical_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("record_number", sa.String(50), nullable=True),
        sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("health_unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("doctor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chief_complaint", sa.String(500), nullable=False),
        sa.Column("history_of_present_illness", sa.String(2000), nullable=True),
        sa.Column("past_medical_history", sa.String(2000), nullable=True),
        sa.Column("family_history", sa.String(1000), nullable=True),
        sa.Column("social_history", sa.String(1000), nullable=True),
        sa.Column("allergies", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("vital_signs", postgresql.JSON(), nullable=True),
        sa.Column("physical_exam", sa.String(2000), nullable=True),
        sa.Column("diagnosis", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("diagnosis_codes", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("treatment_plan", sa.String(2000), nullable=True),
        sa.Column("recommendations", sa.String(1000), nullable=True),
        sa.Column("follow_up_date", sa.Date(), nullable=True),
        sa.Column("prescription_ids", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("exam_request_ids", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("record_number"),
    )
    op.create_table(
        "vaccines",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.String(1000), nullable=True),
        sa.Column("manufacturer", sa.String(200), nullable=False),
        sa.Column("doses_required", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("dose_interval_days", sa.Integer(), nullable=True),
        sa.Column("min_age_months", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_age_months", sa.Integer(), nullable=True),
        sa.Column("contraindications", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_mandatory", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "vaccine_doses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("vaccine_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("health_unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("applied_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dose_number", sa.Integer(), nullable=False),
        sa.Column("batch_number", sa.String(100), nullable=False),
        sa.Column("application_date", sa.Date(), nullable=False),
        sa.Column("next_dose_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="APLICADA"),
        sa.Column("adverse_reactions", sa.String(2000), nullable=True),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "health_units",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("unit_type", sa.String(50), nullable=False),
        sa.Column("province", sa.String(100), nullable=False),
        sa.Column("municipality", sa.String(100), nullable=False),
        sa.Column("commune", sa.String(100), nullable=True),
        sa.Column("address", sa.String(500), nullable=False),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("email", sa.String(100), nullable=True),
        sa.Column("beds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("has_emergency", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("has_laboratory", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("has_pharmacy", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("specialties", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("opening_hours", postgresql.JSON(), nullable=True),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "health_professionals",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("health_unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("license_number", sa.String(100), nullable=False),
        sa.Column("specialization", sa.String(200), nullable=False),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "exam_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_number", sa.String(50), nullable=True),
        sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("doctor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("health_unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("exam_type", sa.String(100), nullable=False),
        sa.Column("exam_description", sa.String(1000), nullable=False),
        sa.Column("clinical_indication", sa.String(1000), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="SOLICITADO"),
        sa.Column("priority", sa.String(20), nullable=False, server_default="MEDIA"),
        sa.Column("requested_date", sa.Date(), nullable=False),
        sa.Column("scheduled_date", sa.Date(), nullable=True),
        sa.Column("collection_date", sa.Date(), nullable=True),
        sa.Column("result_date", sa.Date(), nullable=True),
        sa.Column("result_file", sa.String(500), nullable=True),
        sa.Column("result_notes", sa.String(2000), nullable=True),
        sa.Column("workflow_instance_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("metadata_", postgresql.JSON(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("request_number"),
    )


def downgrade():
    """Drop health tables"""
    op.drop_table("exam_requests")
    op.drop_table("health_professionals")
    op.drop_table("health_units")
    op.drop_table("vaccine_doses")
    op.drop_table("vaccines")
    op.drop_table("medical_records")
    op.drop_table("prescriptions")
    op.drop_table("appointments")
