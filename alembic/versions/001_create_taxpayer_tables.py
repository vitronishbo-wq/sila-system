"""Create taxpayer and declaration tables

Revision ID: 001_create_taxpayer_tables
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# Revision identifiers, used by Alembic.
revision = '001_create_taxpayer_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create taxpayer table
    op.create_table(
        'payment_taxpayers',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('nif', sa.String(20), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('tax_regime', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='ACTIVE'),
        sa.Column('agt_status', sa.String(50), nullable=True),
        sa.Column('agt_data', postgresql.JSONB(), nullable=True),
        sa.Column('registered_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id', name='payment_taxpayers_pkey'),
        sa.UniqueConstraint('nif', name='payment_taxpayers_nif_unique'),
    )
    
    # Create indexes on taxpayer table
    op.create_index('idx_taxpayer_nif_status', 'payment_taxpayers', ['nif', 'status'])
    op.create_index('idx_taxpayer_email_status', 'payment_taxpayers', ['email', 'status'])
    op.create_index('idx_taxpayer_registered_at', 'payment_taxpayers', ['registered_at'])
    op.create_index('idx_taxpayer_agt_sync', 'payment_taxpayers', ['agt_status', 'updated_at'])
    
    # Create declaration table
    op.create_table(
        'payment_declarations',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('declaration_number', sa.String(50), nullable=False),
        sa.Column('taxpayer_id', sa.UUID(), nullable=False),
        sa.Column('tax_type', sa.String(50), nullable=False),
        sa.Column('tax_period', sa.String(30), nullable=False),
        sa.Column('gross_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('net_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING'),
        sa.Column('protocol', sa.String(50), nullable=True),
        sa.Column('processor_id', sa.String(100), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id', name='payment_declarations_pkey'),
        sa.ForeignKeyConstraint(['taxpayer_id'], ['payment_taxpayers.id'], name='fk_declaration_taxpayer', ondelete='CASCADE'),
        sa.UniqueConstraint('declaration_number', name='payment_declarations_number_unique'),
    )
    
    # Create indexes on declaration table
    op.create_index('idx_declaration_taxpayer_period', 'payment_declarations', ['taxpayer_id', 'tax_period'])
    op.create_index('idx_declaration_status_date', 'payment_declarations', ['status', 'processed_at'])
    op.create_index('idx_declaration_due_date', 'payment_declarations', ['due_date'])
    op.create_index('idx_declaration_protocol', 'payment_declarations', ['protocol'])


def downgrade() -> None:
    op.drop_index('idx_declaration_protocol', table_name='payment_declarations')
    op.drop_index('idx_declaration_due_date', table_name='payment_declarations')
    op.drop_index('idx_declaration_status_date', table_name='payment_declarations')
    op.drop_index('idx_declaration_taxpayer_period', table_name='payment_declarations')
    op.drop_table('payment_declarations')
    
    op.drop_index('idx_taxpayer_agt_sync', table_name='payment_taxpayers')
    op.drop_index('idx_taxpayer_registered_at', table_name='payment_taxpayers')
    op.drop_index('idx_taxpayer_email_status', table_name='payment_taxpayers')
    op.drop_index('idx_taxpayer_nif_status', table_name='payment_taxpayers')
    op.drop_table('payment_taxpayers')
