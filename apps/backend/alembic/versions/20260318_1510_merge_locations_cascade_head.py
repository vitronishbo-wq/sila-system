"""merge locations cascade head

Revision ID: 20260318_1510_merge_locations_cascade_head
Revises: 22ab6d804070, 20260318_1500_locations_parent_cascade
Create Date: 2026-03-18 15:10:00.000000
"""

from __future__ import annotations

from alembic import op

revision: str = "20260318_1510_merge_locations_cascade_head"
down_revision = ("22ab6d804070", "20260318_1500_locations_parent_cascade")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
