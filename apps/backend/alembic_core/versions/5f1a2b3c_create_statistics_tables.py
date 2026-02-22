"""Create statistics tables

Revision ID: 5f1a2b3c
Revises: bi_003_create_reports
Create Date: 2026-02-18
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '5f1a2b3c'
down_revision = 'bi_003_create_reports'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'statistics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('unit', sa.String(50)),
        sa.Column('source_module', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        'statistics_timeseries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('statistic_id', sa.Integer, nullable=False),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('period_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('period_end', sa.DateTime(timezone=True)),
        sa.Column('dimensions', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        'statistics_aggregations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('statistic_id', sa.Integer, nullable=False),
        sa.Column('method', sa.String(20), nullable=False),
        sa.Column('parameters', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('statistics_aggregations')
    op.drop_table('statistics_timeseries')
    op.drop_table('statistics')
