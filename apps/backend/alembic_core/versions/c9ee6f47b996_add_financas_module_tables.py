"""Add financas module tables

Revision ID: c9ee6f47b996
Revises: c99ae146736f
Create Date: 2026-02-21 21:10:00.533967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9ee6f47b996'
down_revision: Union[str, Sequence[str], None] = 'c99ae146736f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create financas_invoices table
    op.create_table(
        'financas_invoices',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('citizen_id', sa.String(), nullable=False),
        sa.Column('request_id', sa.String(), nullable=True),
        sa.Column('reference', sa.String(), nullable=False),
        sa.Column('revenue_code', sa.String(length=32), nullable=False),
        sa.Column('cost_center', sa.String(length=32), nullable=False),
        sa.Column('service_code', sa.String(length=32), nullable=False),
        sa.Column('service_name', sa.String(length=255), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='AOA'),
        sa.Column('status', sa.Enum('draft', 'issued', 'pending', 'paid', 'overdue', 'cancelled', 'disputed', name='invoicestatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reference'),
        schema=None
    )
    op.create_index(op.f('ix_financas_invoices_citizen_id'), 'financas_invoices', ['citizen_id'], unique=False)
    op.create_index(op.f('ix_financas_invoices_request_id'), 'financas_invoices', ['request_id'], unique=False)
    op.create_index(op.f('ix_financas_invoices_status'), 'financas_invoices', ['status'], unique=False)
    op.create_index(op.f('ix_financas_invoices_revenue_code'), 'financas_invoices', ['revenue_code'], unique=False)
    op.create_index(op.f('ix_financas_invoices_cost_center'), 'financas_invoices', ['cost_center'], unique=False)
    op.create_index(op.f('ix_financas_invoices_service_code'), 'financas_invoices', ['service_code'], unique=False)

    # Create financas_payments table
    op.create_table(
        'financas_payments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('invoice_id', sa.String(), nullable=False),
        sa.Column('citizen_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('gateway_reference', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'reconciled', 'failed', 'cancelled', 'refunded', 'disputed', name='paymentstatus'), nullable=False),
        sa.Column('payment_method', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('confirmed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['invoice_id'], ['financas_invoices.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('gateway_reference'),
        schema=None
    )
    op.create_index(op.f('ix_financas_payments_citizen_id'), 'financas_payments', ['citizen_id'], unique=False)
    op.create_index(op.f('ix_financas_payments_invoice_id'), 'financas_payments', ['invoice_id'], unique=False)
    op.create_index(op.f('ix_financas_payments_status'), 'financas_payments', ['status'], unique=False)

    # Create financial_audit_logs table
    op.create_table(
        'financial_audit_logs',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('previous_state', sa.JSON(), nullable=True),
        sa.Column('new_state', sa.JSON(), nullable=True),
        sa.Column('performed_by', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema=None
    )
    op.create_index(op.f('ix_financial_audit_logs_entity_type'), 'financial_audit_logs', ['entity_type'], unique=False)
    op.create_index(op.f('ix_financial_audit_logs_entity_id'), 'financial_audit_logs', ['entity_id'], unique=False)
    op.create_index(op.f('ix_financial_audit_logs_performed_by'), 'financial_audit_logs', ['performed_by'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_financial_audit_logs_performed_by'), table_name='financial_audit_logs')
    op.drop_index(op.f('ix_financial_audit_logs_entity_id'), table_name='financial_audit_logs')
    op.drop_index(op.f('ix_financial_audit_logs_entity_type'), table_name='financial_audit_logs')
    op.drop_table('financial_audit_logs')

    op.drop_index(op.f('ix_financas_payments_status'), table_name='financas_payments')
    op.drop_index(op.f('ix_financas_payments_invoice_id'), table_name='financas_payments')
    op.drop_index(op.f('ix_financas_payments_citizen_id'), table_name='financas_payments')
    op.drop_table('financas_payments')

    op.drop_index(op.f('ix_financas_invoices_service_code'), table_name='financas_invoices')
    op.drop_index(op.f('ix_financas_invoices_cost_center'), table_name='financas_invoices')
    op.drop_index(op.f('ix_financas_invoices_revenue_code'), table_name='financas_invoices')
    op.drop_index(op.f('ix_financas_invoices_status'), table_name='financas_invoices')
    op.drop_index(op.f('ix_financas_invoices_request_id'), table_name='financas_invoices')
    op.drop_index(op.f('ix_financas_invoices_citizen_id'), table_name='financas_invoices')
    op.drop_table('financas_invoices')
