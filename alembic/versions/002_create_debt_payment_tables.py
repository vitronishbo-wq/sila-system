"""Create debt and payment tables

Revision ID: 002_create_debt_payment_tables
Revises: 001_create_taxpayer_tables
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# Revision identifiers, used by Alembic.
revision = '002_create_debt_payment_tables'
down_revision = '001_create_taxpayer_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create debt table
    op.create_table(
        'payment_debts',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('debt_number', sa.String(50), nullable=False),
        sa.Column('taxpayer_id', sa.UUID(), nullable=False),
        sa.Column('tax_type', sa.String(50), nullable=False),
        sa.Column('original_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('current_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('interest', sa.Numeric(15, 2), nullable=False, server_default='0'),
        sa.Column('fines', sa.Numeric(15, 2), nullable=False, server_default='0'),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING'),
        sa.Column('due_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id', name='payment_debts_pkey'),
        sa.ForeignKeyConstraint(['taxpayer_id'], ['payment_taxpayers.id'], name='fk_debt_taxpayer', ondelete='CASCADE'),
        sa.UniqueConstraint('debt_number', name='payment_debts_number_unique'),
    )
    
    # Create indexes on debt table
    op.create_index('idx_debt_taxpayer_status', 'payment_debts', ['taxpayer_id', 'status'])
    op.create_index('idx_debt_due_date_status', 'payment_debts', ['due_date', 'status'])
    op.create_index('idx_debt_overdue', 'payment_debts', ['due_date', 'status'], 
                    postgresql_where=sa.text("status IN ('PENDING', 'PARTIAL')"))
    
    # Create payment table
    op.create_table(
        'payment_payments',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('payment_number', sa.String(50), nullable=False),
        sa.Column('taxpayer_id', sa.UUID(), nullable=False),
        sa.Column('debt_id', sa.UUID(), nullable=True),
        sa.Column('amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('payment_method', sa.String(50), nullable=False),
        sa.Column('payment_date', sa.DateTime(), nullable=False),
        sa.Column('reference', sa.String(100), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='COMPLETED'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id', name='payment_payments_pkey'),
        sa.ForeignKeyConstraint(['taxpayer_id'], ['payment_taxpayers.id'], name='fk_payment_taxpayer', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['debt_id'], ['payment_debts.id'], name='fk_payment_debt', ondelete='CASCADE'),
        sa.UniqueConstraint('payment_number', name='payment_payments_number_unique'),
    )
    
    # Create indexes on payment table
    op.create_index('idx_payment_taxpayer_date', 'payment_payments', ['taxpayer_id', 'payment_date'])
    op.create_index('idx_payment_debt', 'payment_payments', ['debt_id'])
    op.create_index('idx_payment_reference', 'payment_payments', ['reference'])
    op.create_index('idx_payment_method', 'payment_payments', ['payment_method'])


def downgrade() -> None:
    op.drop_index('idx_payment_method', table_name='payment_payments')
    op.drop_index('idx_payment_reference', table_name='payment_payments')
    op.drop_index('idx_payment_debt', table_name='payment_payments')
    op.drop_index('idx_payment_taxpayer_date', table_name='payment_payments')
    op.drop_table('payment_payments')
    
    op.drop_index('idx_debt_overdue', table_name='payment_debts')
    op.drop_index('idx_debt_due_date_status', table_name='payment_debts')
    op.drop_index('idx_debt_taxpayer_status', table_name='payment_debts')
    op.drop_table('payment_debts')
