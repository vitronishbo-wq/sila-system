"""Set locations parent FK to ON DELETE CASCADE

Revision ID: 20260318_1500_locations_parent_cascade
Revises: 20260318_1200_create_sla_engine_tables
Create Date: 2026-03-18 15:00:00.000000
"""

from __future__ import annotations

from alembic import op

revision: str = "20260318_1500_locations_parent_cascade"
down_revision: str = "20260318_1200_create_sla_engine_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("locations_parent_id_fkey", "locations", type_="foreignkey")
    op.create_foreign_key(
        "locations_parent_id_fkey",
        "locations",
        "locations",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("locations_parent_id_fkey", "locations", type_="foreignkey")
    op.create_foreign_key(
        "locations_parent_id_fkey",
        "locations",
        "locations",
        ["parent_id"],
        ["id"],
    )
