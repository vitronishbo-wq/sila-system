"""Migração: Criar tabela de auditoria financeira

Revision ID: 003_create_audit_logs_table
Revises: 002_create_payments_table
Create Date: 2026-02-11 00:30:00

Schema:
- audit_id (PK): ID sequencial para auditoria
- audit_uuid: UUID para auditoria distribuída
- operation: Nome da operação (ex: INVOICE_CREATION, PAYMENT_PROCESSED)
- citizen_id: ID do cidadão afetado
- invoice_id, payment_id: Entidades afetadas
- module: Módulo origem (ex: FINANCAS, CITIZEN)
- actor: Quem executou (ex: SYSTEM, USER_ID)
- status: SUCCESS, FAILED, ERROR
- payload: Dados completos da operação (JSONB)
- created_at: Timestamp imutável

Design:
- INSERTS ONLY: Nenhum UPDATE ou DELETE permitido
- Índices para buscar por cidadão, operação, data
- Conformidade com regulamentações de auditoria
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        "financial_audit_logs",
        sa.Column("audit_id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("audit_uuid", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("operation", sa.String(length=100), nullable=False, index=True),
        sa.Column("citizen_id", sa.String(length=50), nullable=True, index=True),
        sa.Column("invoice_id", sa.String(length=50), nullable=True, index=True),
        sa.Column("payment_id", sa.String(length=50), nullable=True, index=True),
        sa.Column("module", sa.String(length=50), nullable=False, server_default="FINANCAS"),
        sa.Column("actor", sa.String(length=100), nullable=False, server_default="SYSTEM"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="SUCCESS"),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now(), index=True
        ),
        sa.PrimaryKeyConstraint("audit_id", name="pk_financial_audit_logs"),
        sa.Index("idx_audit_citizen_date", "citizen_id", "created_at"),
        sa.Index("idx_audit_invoice_date", "invoice_id", "created_at"),
        sa.Index("idx_audit_operation_date", "operation", "created_at"),
    )


def downgrade():
    op.drop_table("financial_audit_logs")
