"""Add views and performance tuning

Revision ID: 007_add_views_performance
Revises: 006_add_triggers
Create Date: 2024-01-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '007_add_views_performance'
down_revision = '006_add_triggers'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create view for taxpayer summary
    op.execute("""
    CREATE OR REPLACE VIEW vw_taxpayer_summary AS
    SELECT 
        t.id,
        t.nif,
        t.name,
        t.email,
        t.phone,
        t.status,
        COUNT(DISTINCT d.id) as declaration_count,
        COUNT(DISTINCT debt.id) as debt_count,
        COUNT(DISTINCT p.id) as payment_count,
        COALESCE(SUM(debt.current_amount), 0) as total_debt,
        COALESCE(SUM(p.amount), 0) as total_paid,
        t.created_at
    FROM payment_taxpayers t
    LEFT JOIN payment_declarations d ON t.id = d.taxpayer_id
    LEFT JOIN payment_debts debt ON t.id = debt.taxpayer_id AND debt.status NOT IN ('PAID', 'CANCELLED')
    LEFT JOIN payment_payments p ON t.id = p.taxpayer_id
    GROUP BY t.id, t.nif, t.name, t.email, t.phone, t.status, t.created_at;
    """)
    
    # Create view for pending declarations
    op.execute("""
    CREATE OR REPLACE VIEW vw_pending_declarations AS
    SELECT 
        d.id,
        d.declaration_number,
        t.nif,
        t.name,
        d.tax_type,
        d.tax_period,
        d.gross_amount,
        d.net_amount,
        d.status,
        d.due_date,
        d.submitted_at,
        COALESCE((EXTRACT(DAY FROM NOW() - d.due_date))::INTEGER, 0) as days_overdue
    FROM payment_declarations d
    JOIN payment_taxpayers t ON d.taxpayer_id = t.id
    WHERE d.status = 'PENDING'
    ORDER BY d.due_date ASC;
    """)
    
    # Create view for overdue debts
    op.execute("""
    CREATE OR REPLACE VIEW vw_overdue_debts AS
    SELECT 
        debt.id,
        debt.debt_number,
        t.nif,
        t.name,
        debt.tax_type,
        debt.original_amount,
        debt.current_amount,
        debt.interest,
        debt.fines,
        debt.status,
        debt.due_date,
        EXTRACT(DAY FROM NOW() - debt.due_date)::INTEGER as days_overdue
    FROM payment_debts debt
    JOIN payment_taxpayers t ON debt.taxpayer_id = t.id
    WHERE debt.status IN ('PENDING', 'PARTIAL')
    AND debt.due_date < NOW()
    ORDER BY debt.due_date ASC;
    """)
    
    # Create view for certificate status
    op.execute("""
    CREATE OR REPLACE VIEW vw_certificate_status AS
    SELECT 
        c.id,
        c.certificate_number,
        t.nif,
        t.name,
        c.certificate_type,
        c.year,
        c.status,
        c.expires_at,
        CASE 
            WHEN c.expires_at IS NULL THEN 'N/A'
            WHEN c.expires_at < NOW() THEN 'EXPIRED'
            WHEN c.expires_at < NOW() + INTERVAL '30 days' THEN 'EXPIRING_SOON'
            ELSE 'VALID'
        END as validity_status,
        c.created_at
    FROM payment_certificates c
    JOIN payment_taxpayers t ON c.taxpayer_id = t.id
    ORDER BY c.expires_at ASC;
    """)
    
    # Create materialized view for analytics (monthly summary)
    op.execute("""
    CREATE MATERIALIZED VIEW mv_monthly_summary AS
    SELECT 
        DATE_TRUNC('month', p.payment_date)::DATE as month,
        COUNT(DISTINCT p.payload_id) as payment_count,
        COALESCE(SUM(p.amount), 0) as total_amount,
        COUNT(DISTINCT t.id) as taxpayer_count,
        COUNT(DISTINCT CASE WHEN d.id IS NOT NULL THEN d.id END) as paid_debts
    FROM payment_payments p
    LEFT JOIN payment_taxpayers t ON p.taxpayer_id = t.id
    LEFT JOIN payment_debts d ON p.debt_id = d.id
    GROUP BY DATE_TRUNC('month', p.payment_date)
    ORDER BY month DESC;
    """)
    
    # Create indexes for view optimization
    op.create_index('idx_declaration_status_due_date', 'payment_declarations', 
                    ['status', 'due_date'], postgresql_where=sa.text("status = 'PENDING'"))
    op.create_index('idx_debt_status_due_date', 'payment_debts', 
                    ['status', 'due_date'], postgresql_where=sa.text("status IN ('PENDING', 'PARTIAL')"))
    op.create_index('idx_certificate_expires_status', 'payment_certificates', 
                    ['expires_at', 'status'], postgresql_where=sa.text("status = 'ISSUED'"))
    
    # Create index on audit for time range queries
    op.create_index('idx_audit_created_at', 'payment_audits', ['created_at'])
    
    # Add stats to tables for query planning
    op.execute("ANALYZE payment_taxpayers")
    op.execute("ANALYZE payment_declarations")
    op.execute("ANALYZE payment_debts")
    op.execute("ANALYZE payment_payments")
    op.execute("ANALYZE payment_certificates")
    op.execute("ANALYZE payment_audits")


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_monthly_summary")
    op.execute("DROP VIEW IF EXISTS vw_certificate_status")
    op.execute("DROP VIEW IF EXISTS vw_overdue_debts")
    op.execute("DROP VIEW IF EXISTS vw_pending_declarations")
    op.execute("DROP VIEW IF EXISTS vw_taxpayer_summary")
    
    op.drop_index('idx_audit_created_at', table_name='payment_audits')
    op.drop_index('idx_certificate_expires_status', table_name='payment_certificates')
    op.drop_index('idx_debt_status_due_date', table_name='payment_debts')
    op.drop_index('idx_declaration_status_due_date', table_name='payment_declarations')
