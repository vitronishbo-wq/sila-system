"""merge legacy alembic heads into a single chain

Revision ID: 20260228_001_merge_legacy_heads
Revises: add_import_batch_id_to_territory, 20231027001
Create Date: 2026-02-28 02:30:00.000000
"""

from alembic import op


revision = "20260228_001_merge_legacy_heads"
down_revision = ("add_import_batch_id_to_territory", "20231027001")
branch_labels = None
depends_on = None


def upgrade():
    # Merge revision: no DDL required.
    pass


def downgrade():
    # Merge revision: no DDL required.
    pass

