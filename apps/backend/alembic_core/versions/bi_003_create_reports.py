"""Create BI reports table

Revision ID: bi_003_create_reports
Revises: bi_002_create_dashboards
Create Date: 2026-02-18
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'bi_003_create_reports'
down_revision = 'bi_002_create_dashboards'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bi_reports',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('query', sa.Text, nullable=False),
        sa.Column('parameters', postgresql.JSONB),
        sa.Column('created_by', sa.Integer),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('bi_reports')
