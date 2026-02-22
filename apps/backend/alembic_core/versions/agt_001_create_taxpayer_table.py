"""create taxpayer table

Revision ID: agt_001
Revises: 
Create Date: 2026-02-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'agt_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'taxpayers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('citizen_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nif', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index(op.f('ix_taxpayers_nif'), 'taxpayers', ['nif'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_taxpayers_nif'), table_name='taxpayers')
    op.drop_table('taxpayers')
