"""Merge heads: workflow + health indexes

Revision ID: 005_merge_heads
Revises: 001_create_workflow_tables, 004_add_health_indexes
Create Date: 2026-02-18
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '005_merge_heads'
down_revision = ('001_create_workflow_tables', '004_add_health_indexes')
branch_labels = None
depends_on = None


def upgrade():
    # merge-only migration: no DB changes, only unify heads
    pass


def downgrade():
    # cannot reliably downgrade a merge-only migration
    pass
