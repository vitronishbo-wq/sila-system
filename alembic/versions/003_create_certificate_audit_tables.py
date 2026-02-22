"""Create certificate and audit tables

Revision ID: 003_create_certificate_audit_tables
Revises: 002_create_debt_payment_tables
Create Date: 2024-01-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# Revision identifiers, used by Alembic.
revision = '003_create_certificate_audit_tables'
down_revision = '002_create_debt_payment_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create certificate table
    op.create_table(
        'payment_certificates',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('certificate_number', sa.String(50), nullable=False),
        sa.Column('taxpayer_id', sa.UUID(), nullable=False),
        sa.Column('certificate_type', sa.String(50), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING'),
        sa.Column('file_url', sa.String(500), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('agt_reference', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id', name='payment_certificates_pkey'),
        sa.ForeignKeyConstraint(['taxpayer_id'], ['payment_taxpayers.id'], name='fk_certificate_taxpayer', ondelete='CASCADE'),
        sa.UniqueConstraint('certificate_number', name='payment_certificates_number_unique'),
    )
    
    # Create indexes on certificate table
    op.create_index('idx_certificate_taxpayer_type', 'payment_certificates', ['taxpayer_id', 'certificate_type'])
    op.create_index('idx_certificate_expires_at', 'payment_certificates', ['expires_at'])
    op.create_index('idx_certificate_status', 'payment_certificates', ['status'])
    
    # Create audit table
    op.create_table(
        'payment_audits',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('entity_type', sa.String(100), nullable=False),
        sa.Column('entity_id', sa.String(100), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('level', sa.String(20), nullable=False, server_default='INFO'),
        sa.Column('old_values', postgresql.JSONB(), nullable=True),
        sa.Column('new_values', postgresql.JSONB(), nullable=True),
        sa.Column('details', postgresql.JSONB(), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id', name='payment_audits_pkey'),
    )
    
    # Create indexes on audit table
    op.create_index('idx_audit_entity', 'payment_audits', ['entity_type', 'entity_id', 'created_at'])
    op.create_index('idx_audit_user_action', 'payment_audits', ['user_id', 'action', 'created_at'])
    op.create_index('idx_audit_action', 'payment_audits', ['action'])


def downgrade() -> None:
    op.drop_index('idx_audit_action', table_name='payment_audits')
    op.drop_index('idx_audit_user_action', table_name='payment_audits')
    op.drop_index('idx_audit_entity', table_name='payment_audits')
    op.drop_table('payment_audits')
    
    op.drop_index('idx_certificate_status', table_name='payment_certificates')
    op.drop_index('idx_certificate_expires_at', table_name='payment_certificates')
    op.drop_index('idx_certificate_taxpayer_type', table_name='payment_certificates')
    op.drop_table('payment_certificates')
