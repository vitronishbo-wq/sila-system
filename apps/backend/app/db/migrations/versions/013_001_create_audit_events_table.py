"""Migração: Criar tabela audit_events

Revision ID: 013_001_create_audit_events_table
Revises: 012_001_expand_service_catalog_governance
Create Date: 2026-05-24 00:00:00

Schema:
- id: Primary key autoincrement
- event_type: Tipo de evento de auditoria
- aggregate_type: Tipo de agregado afetado
- aggregate_id: Identificador do agregado
- actor_id: Agente que realizou a ação
- correlation_id: Identificador de correlação para rastreamento de fluxo
- payload: Dados do evento em JSON
- created_at: Timestamp de criação do evento
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("aggregate_type", sa.String(length=100), nullable=True),
        sa.Column("aggregate_id", sa.String(length=100), nullable=True),
        sa.Column("actor_id", sa.String(length=100), nullable=True),
        sa.Column("correlation_id", sa.String(length=100), nullable=True),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id", name="pk_audit_events"),
        sa.Index("idx_audit_events_aggregate", "aggregate_type", "aggregate_id"),
        sa.Index("idx_audit_events_created_at", "created_at"),
    )


def downgrade():
    op.drop_table("audit_events")
