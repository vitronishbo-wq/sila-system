"""create citizen_documents table with versioning and indexes

Revision ID: 20260220_001_create_citizen_documents
Revises: 003_add_iam_system
Create Date: 2026-02-20
"""

import enum
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from alembic import context, op

# revision identifiers, used by Alembic.
revision = "20260220_001_create_citizen_documents"
down_revision = "003_add_iam_system"
branch_labels = None
depends_on = None


class DocumentTypeEnum(enum.StrEnum):
    BI = "BI"
    PASSPORT = "PASSPORT"
    BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    PHOTO = "PHOTO"


def upgrade():
    offline = context.is_offline_mode()
    existing_tables = set()
    bind = None
    inspector = None

    if not offline:
        bind = op.get_bind()
        inspector = sa.inspect(bind)
        existing_tables = set(inspector.get_table_names())
        if "citizen_documents" in existing_tables:
            return

    # Resolve FK target on heterogeneous schemas.
    citizen_fk = None
    if not offline and "citizen" in existing_tables:
        citizen_columns = {col["name"] for col in inspector.get_columns("citizen")}
        if "citizen_id" in citizen_columns:
            citizen_fk = "citizen.citizen_id"
        elif "id" in citizen_columns:
            citizen_fk = "citizen.id"

    if offline:
        op.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'documenttypeenum') THEN
                    CREATE TYPE documenttypeenum AS ENUM (
                        'BI', 'PASSPORT', 'BIRTH_CERTIFICATE', 'DRIVER_LICENSE', 'PHOTO'
                    );
                END IF;
            END
            $$;
            """
        )

    enum_type = pg.ENUM(
        *(item.value for item in DocumentTypeEnum),
        name="documenttypeenum",
        create_type=False,
    )
    if not offline:
        enum_type.create(bind, checkfirst=True)

    citizen_column_args = [pg.UUID(as_uuid=True)]
    if citizen_fk:
        citizen_column_args.append(sa.ForeignKey(citizen_fk))

    op.create_table(
        "citizen_documents",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("citizen_id", *citizen_column_args, nullable=False),
        sa.Column("type", enum_type, nullable=False),
        sa.Column("file_path", sa.String(256), nullable=False),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column("updated_at", sa.DateTime, nullable=False, default=datetime.utcnow),
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_citizen_documents_citizen_id "
        "ON citizen_documents (citizen_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_citizen_documents_type ON citizen_documents (type)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_citizen_documents_version ON citizen_documents (version)"
    )


def downgrade():
    op.drop_index("ix_citizen_documents_version", table_name="citizen_documents")
    op.drop_index("ix_citizen_documents_type", table_name="citizen_documents")
    op.drop_index("ix_citizen_documents_citizen_id", table_name="citizen_documents")
    op.drop_table("citizen_documents")
