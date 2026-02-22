"""Create BI metrics table

Revision ID: bi_001_create_metrics
Revises: 005_merge_heads
Create Date: 2026-02-18
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'bi_001_create_metrics'
down_revision = '005_merge_heads'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bi_metrics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('source', sa.String(100), nullable=False),
        sa.Column('dimension', sa.String(100)),
        sa.Column('period', sa.String(50), nullable=False),
        sa.Column('extra', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_bi_metrics_code', 'bi_metrics', ['code'])
    op.create_index('ix_bi_metrics_period', 'bi_metrics', ['period'])


def downgrade():
    op.drop_index('ix_bi_metrics_code', table_name='bi_metrics')
    op.drop_index('ix_bi_metrics_period', table_name='bi_metrics')
    op.drop_table('bi_metrics')
