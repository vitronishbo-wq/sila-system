"""Add territorial hierarchy fields to citizen_requests

Revision ID: 20260212004
Revises: 20260212003
Create Date: 2026-02-12 14:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "20260212004"
down_revision = "20260212003"
branch_labels = None
depends_on = None


def upgrade():
    # Adicionar campos territoriais e escalamento
    op.add_column(
        "citizen_requests",
        sa.Column(
            "commune_id",
            UUID(as_uuid=True),
            nullable=True,
            comment="FK para a Comuna"
        )
    )
    
    op.add_column(
        "citizen_requests",
        sa.Column(
            "municipality_id",
            UUID(as_uuid=True),
            nullable=True,
            comment="FK para o Município"
        )
    )
    
    op.add_column(
        "citizen_requests",
        sa.Column(
            "province_id",
            UUID(as_uuid=True),
            nullable=True,
            comment="FK para a Província"
        )
    )
    
    op.add_column(
        "citizen_requests",
        sa.Column(
            "is_escalated",
            sa.Boolean,
            nullable=False,
            server_default="false",
            comment="Indica se o pedido foi escalado"
        )
    )
    
    # Criar Foreign Keys
    op.create_foreign_key(
        "fk_citizen_requests_commune_id",
        "citizen_requests",
        "territories",
        ["commune_id"],
        ["id"],
        ondelete="SET NULL"
    )
    
    op.create_foreign_key(
        "fk_citizen_requests_municipality_id",
        "citizen_requests",
        "territories",
        ["municipality_id"],
        ["id"],
        ondelete="SET NULL"
    )
    
    op.create_foreign_key(
        "fk_citizen_requests_province_id",
        "citizen_requests",
        "territories",
        ["province_id"],
        ["id"],
        ondelete="SET NULL"
    )
    
    # Criar índices para performance
    op.create_index(
        "ix_citizen_requests_commune_id",
        "citizen_requests",
        ["commune_id"]
    )
    
    op.create_index(
        "ix_citizen_requests_municipality_id",
        "citizen_requests",
        ["municipality_id"]
    )
    
    op.create_index(
        "ix_citizen_requests_province_id",
        "citizen_requests",
        ["province_id"]
    )
    
    op.create_index(
        "ix_citizen_requests_is_escalated",
        "citizen_requests",
        ["is_escalated"]
    )


def downgrade():
    # Remover índices
    op.drop_index("ix_citizen_requests_is_escalated", table_name="citizen_requests")
    op.drop_index("ix_citizen_requests_province_id", table_name="citizen_requests")
    op.drop_index("ix_citizen_requests_municipality_id", table_name="citizen_requests")
    op.drop_index("ix_citizen_requests_commune_id", table_name="citizen_requests")
    
    # Remover Foreign Keys
    op.drop_constraint(
        "fk_citizen_requests_province_id",
        "citizen_requests",
        type_="foreignkey"
    )
    op.drop_constraint(
        "fk_citizen_requests_municipality_id",
        "citizen_requests",
        type_="foreignkey"
    )
    op.drop_constraint(
        "fk_citizen_requests_commune_id",
        "citizen_requests",
        type_="foreignkey"
    )
    
    # Remover colunas
    op.drop_column("citizen_requests", "is_escalated")
    op.drop_column("citizen_requests", "province_id")
    op.drop_column("citizen_requests", "municipality_id")
    op.drop_column("citizen_requests", "commune_id")
