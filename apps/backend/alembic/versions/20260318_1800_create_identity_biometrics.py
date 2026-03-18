"""create identity biometrics table

Revision ID: 20260318_1800_create_identity_biometrics
Revises: 20260318_1715_add_economy_audit_columns
Create Date: 2026-03-18 18:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision: str = '20260318_1800_create_identity_biometrics'
down_revision = '20260318_1715_add_economy_audit_columns'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'identity_biometrics',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('citizen_id', sa.String(64), nullable=False),
        sa.Column('biometric_type', sa.String(32), nullable=False),
        sa.Column('biometric_data', sa.Text, nullable=False),
        sa.Column('quality_score', sa.Numeric(5, 2), nullable=False),
        sa.Column('quality_threshold', sa.Numeric(5, 2), nullable=True),
        sa.Column('device_id', sa.String(128), nullable=True),
        sa.Column('location', sa.String(128), nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default='ENROLLED'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('ix_identity_biometrics_citizen_id', 'identity_biometrics', ['citizen_id'])
    op.create_index('ix_identity_biometrics_type', 'identity_biometrics', ['biometric_type'])
    op.create_index('ix_identity_biometrics_status', 'identity_biometrics', ['status'])


def downgrade() -> None:
    op.drop_index('ix_identity_biometrics_status', table_name='identity_biometrics')
    op.drop_index('ix_identity_biometrics_type', table_name='identity_biometrics')
    op.drop_index('ix_identity_biometrics_citizen_id', table_name='identity_biometrics')
    op.drop_table('identity_biometrics')
