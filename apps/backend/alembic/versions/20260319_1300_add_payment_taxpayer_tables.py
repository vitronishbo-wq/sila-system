"""add payment taxpayer tables and performance views

Revision ID: 20260319_1300_add_payment_taxpayer_tables
Revises: 20260319_1200_repair_service_catalog_tables
Create Date: 2026-03-19 13:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql

revision = "20260319_1300_add_payment_taxpayer_tables"
down_revision = "20260319_1200_repair_service_catalog_tables"
branch_labels = None
depends_on = None


def _has_table(inspector: sa.Inspector, name: str) -> bool:
    return inspector.has_table(name)


def _has_index(inspector: sa.Inspector, table: str, name: str) -> bool:
    return any(idx.get("name") == name for idx in inspector.get_indexes(table))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    has_taxpayers = _has_table(inspector, "payment_taxpayers")
    if not has_taxpayers:
        op.create_table(
            "payment_taxpayers",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("nif", sa.String(length=20), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=True),
            sa.Column("phone", sa.String(length=20), nullable=True),
            sa.Column("address", sa.String(length=500), nullable=True),
            sa.Column("tax_regime", sa.String(length=50), nullable=False),
            sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
            sa.Column("agt_status", sa.String(length=50), nullable=True),
            sa.Column("agt_data", postgresql.JSONB(), nullable=True),
            sa.Column("registered_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.PrimaryKeyConstraint("id", name="payment_taxpayers_pkey"),
            sa.UniqueConstraint("nif", name="payment_taxpayers_nif_unique"),
        )
        has_taxpayers = True

    if has_taxpayers:
        inspector = inspect(bind)
        if not _has_index(inspector, "payment_taxpayers", "idx_taxpayer_nif_status"):
            op.create_index(
                "idx_taxpayer_nif_status",
                "payment_taxpayers",
                ["nif", "status"],
            )
        if not _has_index(inspector, "payment_taxpayers", "idx_taxpayer_email_status"):
            op.create_index(
                "idx_taxpayer_email_status",
                "payment_taxpayers",
                ["email", "status"],
            )
        if not _has_index(inspector, "payment_taxpayers", "idx_taxpayer_registered_at"):
            op.create_index(
                "idx_taxpayer_registered_at",
                "payment_taxpayers",
                ["registered_at"],
            )
        if not _has_index(inspector, "payment_taxpayers", "idx_taxpayer_agt_sync"):
            op.create_index(
                "idx_taxpayer_agt_sync",
                "payment_taxpayers",
                ["agt_status", "updated_at"],
            )

    has_declarations = _has_table(inspector, "payment_declarations")
    if not has_declarations:
        op.create_table(
            "payment_declarations",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("declaration_number", sa.String(length=50), nullable=False),
            sa.Column("taxpayer_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("tax_type", sa.String(length=50), nullable=False),
            sa.Column("tax_period", sa.String(length=30), nullable=False),
            sa.Column("gross_amount", sa.Numeric(15, 2), nullable=False),
            sa.Column("net_amount", sa.Numeric(15, 2), nullable=False),
            sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
            sa.Column("protocol", sa.String(length=50), nullable=True),
            sa.Column("processor_id", sa.String(length=100), nullable=True),
            sa.Column("due_date", sa.DateTime(), nullable=True),
            sa.Column("submitted_at", sa.DateTime(), nullable=True),
            sa.Column("processed_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.PrimaryKeyConstraint("id", name="payment_declarations_pkey"),
            sa.ForeignKeyConstraint(
                ["taxpayer_id"],
                ["payment_taxpayers.id"],
                name="fk_declaration_taxpayer",
                ondelete="CASCADE",
            ),
            sa.UniqueConstraint("declaration_number", name="payment_declarations_number_unique"),
        )
        has_declarations = True

    if has_declarations:
        inspector = inspect(bind)
        if not _has_index(inspector, "payment_declarations", "idx_declaration_taxpayer_period"):
            op.create_index(
                "idx_declaration_taxpayer_period",
                "payment_declarations",
                ["taxpayer_id", "tax_period"],
            )
        if not _has_index(inspector, "payment_declarations", "idx_declaration_status_date"):
            op.create_index(
                "idx_declaration_status_date",
                "payment_declarations",
                ["status", "processed_at"],
            )
        if not _has_index(inspector, "payment_declarations", "idx_declaration_due_date"):
            op.create_index(
                "idx_declaration_due_date",
                "payment_declarations",
                ["due_date"],
            )
        if not _has_index(inspector, "payment_declarations", "idx_declaration_protocol"):
            op.create_index(
                "idx_declaration_protocol",
                "payment_declarations",
                ["protocol"],
            )

    has_debts = _has_table(inspector, "payment_debts")
    has_payments = _has_table(inspector, "payment_payments")
    has_certificates = _has_table(inspector, "payment_certificates")
    has_audits = _has_table(inspector, "payment_audits")

    if has_taxpayers and has_declarations and has_debts and has_payments:
        op.execute(
            """
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
            """
        )

    if has_taxpayers and has_declarations:
        op.execute(
            """
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
            """
        )

    if has_debts and has_taxpayers:
        op.execute(
            """
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
            """
        )

    if has_certificates and has_taxpayers:
        op.execute(
            """
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
            """
        )

    if has_payments and has_taxpayers and has_debts:
        op.execute(
            """
            CREATE MATERIALIZED VIEW IF NOT EXISTS mv_monthly_summary AS
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
            """
        )

    if has_declarations and not _has_index(
        inspector, "payment_declarations", "idx_declaration_status_due_date"
    ):
        op.create_index(
            "idx_declaration_status_due_date",
            "payment_declarations",
            ["status", "due_date"],
            postgresql_where=sa.text("status = 'PENDING'"),
        )

    if has_debts and not _has_index(inspector, "payment_debts", "idx_debt_status_due_date"):
        op.create_index(
            "idx_debt_status_due_date",
            "payment_debts",
            ["status", "due_date"],
            postgresql_where=sa.text("status IN ('PENDING', 'PARTIAL')"),
        )

    if has_certificates and not _has_index(
        inspector, "payment_certificates", "idx_certificate_expires_status"
    ):
        op.create_index(
            "idx_certificate_expires_status",
            "payment_certificates",
            ["expires_at", "status"],
            postgresql_where=sa.text("status = 'ISSUED'"),
        )

    if has_audits and not _has_index(inspector, "payment_audits", "idx_audit_created_at"):
        op.create_index(
            "idx_audit_created_at",
            "payment_audits",
            ["created_at"],
        )


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_monthly_summary;")
    op.execute("DROP VIEW IF EXISTS vw_certificate_status;")
    op.execute("DROP VIEW IF EXISTS vw_overdue_debts;")
    op.execute("DROP VIEW IF EXISTS vw_pending_declarations;")
    op.execute("DROP VIEW IF EXISTS vw_taxpayer_summary;")

    op.execute("DROP INDEX IF EXISTS idx_audit_created_at;")
    op.execute("DROP INDEX IF EXISTS idx_certificate_expires_status;")
    op.execute("DROP INDEX IF EXISTS idx_debt_status_due_date;")
    op.execute("DROP INDEX IF EXISTS idx_declaration_status_due_date;")

    op.execute("DROP INDEX IF EXISTS idx_declaration_protocol;")
    op.execute("DROP INDEX IF EXISTS idx_declaration_due_date;")
    op.execute("DROP INDEX IF EXISTS idx_declaration_status_date;")
    op.execute("DROP INDEX IF EXISTS idx_declaration_taxpayer_period;")
    op.execute("DROP TABLE IF EXISTS payment_declarations;")

    op.execute("DROP INDEX IF EXISTS idx_taxpayer_agt_sync;")
    op.execute("DROP INDEX IF EXISTS idx_taxpayer_registered_at;")
    op.execute("DROP INDEX IF EXISTS idx_taxpayer_email_status;")
    op.execute("DROP INDEX IF EXISTS idx_taxpayer_nif_status;")
    op.execute("DROP TABLE IF EXISTS payment_taxpayers;")
