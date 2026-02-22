"""Create BI dashboards table

Revision ID: bi_002_create_dashboards
Revises: bi_001_create_metrics
Create Date: 2026-02-18
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'bi_002_create_dashboards'
down_revision = 'bi_001_create_metrics'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bi_dashboards',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('owner_id', sa.Integer),
        sa.Column('layout', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_bi_dashboards_owner', 'bi_dashboards', ['owner_id'])


def downgrade():
    op.drop_index('ix_bi_dashboards_owner', table_name='bi_dashboards')
    op.drop_table('bi_dashboards')
