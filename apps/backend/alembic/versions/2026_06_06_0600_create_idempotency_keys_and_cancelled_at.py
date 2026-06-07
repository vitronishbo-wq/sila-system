"""create idempotency_keys table + cancelled_at column

Revision ID: 20260606_0600_create_idempotency_keys_and_cancelled_at
Revises: 20260606_0500_create_educacao_transfer_wizard
Create Date: 2026-06-06 06:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "20260606_0600_create_idempotency_keys_and_cancelled_at"
down_revision = "20260606_0500_create_educacao_transfer_wizard"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "idempotency_keys",
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("operation", sa.String(64), nullable=False, index=True),
        sa.Column("result", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.add_column("educacao_seat_reservations", sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True))


def downgrade():
    op.drop_column("educacao_seat_reservations", "cancelled_at")
    op.drop_table("idempotency_keys")
