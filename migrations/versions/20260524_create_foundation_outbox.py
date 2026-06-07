"""create foundation_outbox table

Revision ID: 20260524_create_foundation_outbox
Revises: 
Create Date: 2026-05-24 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260524_create_foundation_outbox'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'foundation_outbox',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('topic', sa.String(length=255), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('dispatched', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('dispatched_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('locked_by', sa.String(length=64), nullable=True),
        sa.Column('locked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
    )
    op.create_index('ix_foundation_outbox_dispatched', 'foundation_outbox', ['dispatched'])
    op.create_index('ix_foundation_outbox_locked_by', 'foundation_outbox', ['locked_by'])
    op.create_index('ix_foundation_outbox_created_at', 'foundation_outbox', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_foundation_outbox_created_at', table_name='foundation_outbox')
    op.drop_index('ix_foundation_outbox_locked_by', table_name='foundation_outbox')
    op.drop_index('ix_foundation_outbox_dispatched', table_name='foundation_outbox')
    op.drop_table('foundation_outbox')
