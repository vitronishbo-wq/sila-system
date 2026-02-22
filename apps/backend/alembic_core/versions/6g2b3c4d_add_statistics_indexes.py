"""Add indexes for statistics timeseries

Revision ID: 6g2b3c4d
Revises: 5f1a2b3c
Create Date: 2026-02-18
"""
from alembic import op
import sqlalchemy as sa

revision = '6g2b3c4d'
down_revision = '5f1a2b3c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('ix_statistics_code', 'statistics', ['code'])
    op.create_index('ix_timeseries_statistic_id', 'statistics_timeseries', ['statistic_id'])
    op.create_index('ix_timeseries_period_start', 'statistics_timeseries', ['period_start'])


def downgrade():
    op.drop_index('ix_timeseries_period_start', table_name='statistics_timeseries')
    op.drop_index('ix_timeseries_statistic_id', table_name='statistics_timeseries')
    op.drop_index('ix_statistics_code', table_name='statistics')
