"""add audit columns to transportes_logistica tables

Revision ID: 20260314_052_transportes_logistica_audit_columns
Revises: 20260313_051_energy_logistics_justice_pillars
Create Date: 2026-03-14 06:00:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260314_052_transportes_logistica_audit_columns"
down_revision = "20260313_051_energy_logistics_justice_pillars"
branch_labels = None
depends_on = None


TABLES: tuple[str, ...] = (
    "transportes_logistica_viagens",
    "transportes_logistica_frotas",
    "transportes_logistica_linhas",
    "transportes_logistica_veiculos",
    "transportes_logistica_bilhetagem_eventos",
)


def upgrade() -> None:
    for table in TABLES:
        op.execute(
            f"""
            ALTER TABLE {table}
            ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ,
            ADD COLUMN IF NOT EXISTS created_by VARCHAR(50),
            ADD COLUMN IF NOT EXISTS updated_by VARCHAR(50),
            ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE
            """
        )


def downgrade() -> None:
    for table in TABLES:
        op.execute(f"ALTER TABLE {table} DROP COLUMN IF EXISTS is_active")
        op.execute(f"ALTER TABLE {table} DROP COLUMN IF EXISTS updated_by")
        op.execute(f"ALTER TABLE {table} DROP COLUMN IF EXISTS created_by")
        op.execute(f"ALTER TABLE {table} DROP COLUMN IF EXISTS updated_at")
