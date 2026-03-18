"""Add constraints and check conditions

Revision ID: 005_add_constraints
Revises: 004_create_sequence_table
Create Date: 2024-01-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '005_add_constraints'
down_revision = '004_create_sequence_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add check constraints for amounts
    op.create_check_constraint(
        'ck_declaration_amounts',
        'payment_declarations',
        'gross_amount >= 0 AND net_amount >= 0 AND net_amount <= gross_amount'
    )
    
    op.create_check_constraint(
        'ck_debt_amounts',
        'payment_debts',
        'original_amount > 0 AND current_amount >= 0 AND interest >= 0 AND fines >= 0'
    )
    
    op.create_check_constraint(
        'ck_payment_amount',
        'payment_payments',
        'amount > 0'
    )
    
    # Add check for valid statuses
    op.create_check_constraint(
        'ck_taxpayer_status',
        'payment_taxpayers',
        "status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'DELETED')"
    )
    
    op.create_check_constraint(
        'ck_declaration_status',
        'payment_declarations',
        "status IN ('PENDING', 'PROCESSING', 'APPROVED', 'REJECTED', 'CANCELLED')"
    )
    
    op.create_check_constraint(
        'ck_debt_status',
        'payment_debts',
        "status IN ('PENDING', 'PARTIAL', 'PAID', 'CANCELLED')"
    )
    
    op.create_check_constraint(
        'ck_payment_status',
        'payment_payments',
        "status IN ('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED')"
    )
    
    op.create_check_constraint(
        'ck_certificate_status',
        'payment_certificates',
        "status IN ('PENDING', 'GENERATING', 'ISSUED', 'EXPIRED', 'REVOKED')"
    )
    
    op.create_check_constraint(
        'ck_audit_level',
        'payment_audits',
        "level IN ('INFO', 'WARNING', 'ERROR', 'CRITICAL')"
    )


def downgrade() -> None:
    op.drop_constraint('ck_audit_level', 'payment_audits', type_='check')
    op.drop_constraint('ck_certificate_status', 'payment_certificates', type_='check')
    op.drop_constraint('ck_payment_status', 'payment_payments', type_='check')
    op.drop_constraint('ck_debt_status', 'payment_debts', type_='check')
    op.drop_constraint('ck_declaration_status', 'payment_declarations', type_='check')
    op.drop_constraint('ck_taxpayer_status', 'payment_taxpayers', type_='check')
    op.drop_constraint('ck_payment_amount', 'payment_payments', type_='check')
    op.drop_constraint('ck_debt_amounts', 'payment_debts', type_='check')
    op.drop_constraint('ck_declaration_amounts', 'payment_declarations', type_='check')
