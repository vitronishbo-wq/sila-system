"""Create citizen table for identidade_civil module

Revision ID: 002_create_citizen_table
Revises: 001
Create Date: 2026-02-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_create_citizen_table'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create citizen table for Identidade Civil module."""
    op.create_table(
        'citizen',
        sa.Column('citizen_id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.func.gen_random_uuid(), primary_key=True),
        sa.Column('full_name', sa.String(255), nullable=False, index=True),
        sa.Column('document_number', sa.String(50), nullable=True, unique=True, index=True),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(10), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True, index=True),
        sa.Column('vital_status', sa.String(20), nullable=False, server_default='alive'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('fuc_sync_timestamp', sa.DateTime(timezone=True), nullable=True),
    )
    
    # Create composite indexes
    op.create_index('idx_citizen_full_name_vital_status', 'citizen', ['full_name', 'vital_status'])
    op.create_index('idx_citizen_created_at', 'citizen', ['created_at'])
    op.create_index('idx_citizen_fuc_sync_timestamp', 'citizen', ['fuc_sync_timestamp'])


def downgrade() -> None:
    """Drop citizen table."""
    # Drop indexes
    op.drop_index('idx_citizen_fuc_sync_timestamp', table_name='citizen')
    op.drop_index('idx_citizen_created_at', table_name='citizen')
    op.drop_index('idx_citizen_full_name_vital_status', table_name='citizen')
    
    # Drop table
    op.drop_table('citizen')
