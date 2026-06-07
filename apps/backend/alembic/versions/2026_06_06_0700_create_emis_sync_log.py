"""create educacao_emis_sync_log table for EMIS sync tracking

Revision ID: 20260606_0700_create_emis_sync_log
Revises: 20260606_0600_create_idempotency_keys_and_cancelled_at
Create Date: 2026-06-06 07:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "20260606_0700_create_emis_sync_log"
down_revision = "20260606_0600_create_idempotency_keys_and_cancelled_at"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "educacao_emis_sync_log",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("entity_type", sa.String(32), nullable=False, index=True),
        sa.Column("entity_id", sa.String(128), nullable=False, index=True),
        sa.Column("direction", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, index=True),
        sa.Column("payload", JSONB(), nullable=True),
        sa.Column("response", JSONB(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
    )


def downgrade():
    op.drop_table("educacao_emis_sync_log")
