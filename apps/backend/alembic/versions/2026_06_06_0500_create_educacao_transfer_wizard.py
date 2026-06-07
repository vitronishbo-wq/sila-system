"""create educacao transfer wizard tables

Revision ID: 20260606_0500_create_educacao_transfer_wizard
Revises: 20260606_0430_create_educacao_marketplace_tables
Create Date: 2026-06-06 05:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "20260606_0500_create_educacao_transfer_wizard"
down_revision = "20260606_0430_create_educacao_marketplace_tables"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "educacao_transfer_wizard",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("citizen_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("status", sa.String(24), nullable=False, default="em_curso", index=True),
        sa.Column("passo_atual", sa.Integer(), nullable=False, default=1),
        sa.Column("origem_escola_id", UUID(as_uuid=True), nullable=True),
        sa.Column("origem_turma_id", UUID(as_uuid=True), nullable=True),
        sa.Column("origem_classe", sa.String(32), nullable=True),
        sa.Column("destino_escola_id", UUID(as_uuid=True), nullable=True),
        sa.Column("destino_turma_id", UUID(as_uuid=True), nullable=True),
        sa.Column("destino_classe", sa.String(32), nullable=True),
        sa.Column("destino_turno", sa.String(32), nullable=True),
        sa.Column("motivo", sa.Text(), nullable=True),
        sa.Column("elegibilidade", JSONB(), nullable=True),
        sa.Column("reserva_id", UUID(as_uuid=True), nullable=True),
        sa.Column("transferencia_id", UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True, onupdate=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_transfer_wizard_citizen_status", "educacao_transfer_wizard", ["citizen_id", "status"])


def downgrade():
    op.drop_index("ix_transfer_wizard_citizen_status", table_name="educacao_transfer_wizard")
    op.drop_table("educacao_transfer_wizard")
