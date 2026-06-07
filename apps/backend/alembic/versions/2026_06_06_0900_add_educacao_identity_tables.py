"""add educacao identity tables for FASE 3.2E

Revision ID: 20260606_0900_add_educacao_identity_tables
Revises: 20260606_0800_add_emis_retry_columns
Create Date: 2026-06-06 09:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "20260606_0900_add_educacao_identity_tables"
down_revision = "20260606_0800_add_emis_retry_columns"
branch_labels = None
depends_on = None


def upgrade():
    # academic identities
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS educacao_academic_identities (
            id UUID PRIMARY KEY,
            national_student_number VARCHAR(64) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            gender VARCHAR(32),
            nationality VARCHAR(64),
            guardian_id UUID,
            current_institution_id UUID,
            current_grade VARCHAR(32),
            academic_status VARCHAR(32),
            identity_status VARCHAR(32),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ,
            created_by VARCHAR(50),
            updated_by VARCHAR(50),
            is_active BOOLEAN NOT NULL DEFAULT TRUE
        )
        """
    )
    op.create_index("ix_educacao_academic_identities_nsn",
                     "educacao_academic_identities", ["national_student_number"],
                     unique=True, if_not_exists=True)
    op.create_index("ix_educacao_academic_identities_full_name",
                     "educacao_academic_identities", ["full_name"],
                     if_not_exists=True)
    op.create_index("ix_educacao_academic_identities_guardian_id",
                     "educacao_academic_identities", ["guardian_id"],
                     if_not_exists=True)
    op.create_index("ix_educacao_academic_identities_academic_status",
                     "educacao_academic_identities", ["academic_status"],
                     if_not_exists=True)
    op.create_index("ix_educacao_academic_identities_identity_status",
                     "educacao_academic_identities", ["identity_status"],
                     if_not_exists=True)

    # guardians
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_guardians (
            id UUID PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            relationship VARCHAR(32) NOT NULL,
            document_id VARCHAR(64),
            phone VARCHAR(32),
            email VARCHAR(128),
            address TEXT,
            province VARCHAR(64),
            municipio VARCHAR(64),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ,
            created_by VARCHAR(50),
            updated_by VARCHAR(50),
            is_active BOOLEAN NOT NULL DEFAULT TRUE
        )
        """
    )
    op.create_index("ix_educacao_guardians_full_name",
                     "educacao_guardians", ["full_name"],
                     if_not_exists=True)
    op.create_index("ix_educacao_guardians_document_id",
                     "educacao_guardians", ["document_id"],
                     if_not_exists=True)

    # guardian-student N:N link
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_guardian_student_links (
            id UUID PRIMARY KEY,
            guardian_id UUID NOT NULL,
            student_id UUID NOT NULL,
            relationship VARCHAR(32) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            created_by VARCHAR(50),
            updated_by VARCHAR(50),
            is_active BOOLEAN NOT NULL DEFAULT TRUE
        )
        """
    )
    op.create_index("ix_educacao_guardian_student_links_guardian_id",
                     "educacao_guardian_student_links", ["guardian_id"],
                     if_not_exists=True)
    op.create_index("ix_educacao_guardian_student_links_student_id",
                     "educacao_guardian_student_links", ["student_id"],
                     if_not_exists=True)

    # identity merge proposals
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_identity_merges (
            id UUID PRIMARY KEY,
            primary_identity_id UUID NOT NULL,
            duplicate_identity_id UUID NOT NULL,
            reason TEXT NOT NULL,
            confidence VARCHAR(16) NOT NULL DEFAULT 'MEDIUM',
            status VARCHAR(16) NOT NULL DEFAULT 'PENDING',
            resolved_by VARCHAR(128),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            resolved_at TIMESTAMPTZ,
            created_by VARCHAR(50),
            updated_by VARCHAR(50),
            is_active BOOLEAN NOT NULL DEFAULT TRUE
        )
        """
    )
    op.create_index("ix_educacao_identity_merges_primary_id",
                     "educacao_identity_merges", ["primary_identity_id"],
                     if_not_exists=True)
    op.create_index("ix_educacao_identity_merges_duplicate_id",
                     "educacao_identity_merges", ["duplicate_identity_id"],
                     if_not_exists=True)
    op.create_index("ix_educacao_identity_merges_status",
                     "educacao_identity_merges", ["status"],
                     if_not_exists=True)

    # student number sequence counters
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_student_number_counters (
            id SERIAL NOT NULL,
            year VARCHAR(4) NOT NULL,
            last_sequence INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
            created_by VARCHAR(50),
            updated_by VARCHAR(50),
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            PRIMARY KEY (id),
            UNIQUE (year)
        )
        """
    )
    op.create_index("ix_educacao_student_number_counters_year",
                     "educacao_student_number_counters", ["year"],
                     unique=True, if_not_exists=True)

    # ensure CoreBase columns exist on all tables (for tables created manually without them)
    for _tbl in ["educacao_academic_identities", "educacao_guardians",
                  "educacao_guardian_student_links", "educacao_identity_merges",
                  "educacao_academic_records"]:
        for _col in ["created_by VARCHAR(50)", "updated_by VARCHAR(50)",
                      "is_active BOOLEAN NOT NULL DEFAULT TRUE"]:
            op.execute(f"ALTER TABLE {_tbl} ADD COLUMN IF NOT EXISTS {_col}")

    # add academic_identity_id to educacao_enrollments (if table exists)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if "educacao_enrollments" in inspector.get_table_names():
        op.execute(
            "ALTER TABLE educacao_enrollments ADD COLUMN IF NOT EXISTS academic_identity_id UUID"
        )
        op.create_index("ix_educacao_enrollments_academic_identity_id",
                         "educacao_enrollments", ["academic_identity_id"],
                         if_not_exists=True)


def downgrade():
    op.drop_column("educacao_enrollments", "academic_identity_id")
    op.execute("DROP TABLE IF EXISTS educacao_student_number_counters")
    op.execute("DROP TABLE IF EXISTS educacao_identity_merges")
    op.execute("DROP TABLE IF EXISTS educacao_guardian_student_links")
    op.execute("DROP TABLE IF EXISTS educacao_guardians")
    op.execute("DROP TABLE IF EXISTS educacao_academic_identities")
