"""Add citizen_id column to invoices table

Revision ID: 004_add_citizen_id
Revises: 001_create_invoices_table
Create Date: 2026-02-10 22:00:00

Nota: Stub documental. O campo citizen_id já faz parte do modelo Invoice
desde a criação inicial. Este ficheiro existe para documentar a intenção
arquitectural de que citizen_id é parte integrante do contrato de faturação.
"""

import sqlalchemy as sa
from alembic import op

revision = "004_add_citizen_id"
down_revision = "001_create_invoices_table"
branch_labels = None
depends_on = None


def upgrade():
    # citizen_id já existe no modelo Invoice desde a criação.
    # Esta migração garante retrocompatibilidade caso a tabela tenha sido
    # criada sem este campo em ambientes legados.
    op.add_column(
        "invoices",
        sa.Column("citizen_id", sa.String(length=50), nullable=False, index=True),
    )


def downgrade():
    op.drop_column("invoices", "citizen_id")
