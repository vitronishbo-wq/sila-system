"""Complete citizen_requests model for Phase 2 Freeze

Revision ID: 20260212005
Revises: 20260212004
Create Date: 2026-02-12 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON

revision = "20260212005"
down_revision = "20260212004"
branch_labels = None
depends_on = None


def upgrade():
    # 1. Adicionar neighborhood_id (opcional)
    op.add_column(
        "citizen_requests",
        sa.Column(
            "neighborhood_id",
            UUID(as_uuid=True),
            nullable=True,
            comment="FK para o bairro (opcional)"
        )
    )
    
    # 2. Adicionar current_territory_id (obrigatório - onde está agora em processamento)
    op.add_column(
        "citizen_requests",
        sa.Column(
            "current_territory_id",
            UUID(as_uuid=True),
            nullable=True,
            comment="FK para o território atual de processamento"
        )
    )
    
    # 3. Adicionar escalation_level (enum-like)
    op.add_column(
        "citizen_requests",
        sa.Column(
            "escalation_level",
            sa.String(20),
            nullable=True,
            comment="Nível de escalamento: municipality, province, central"
        )
    )
    
    # 4. Adicionar escalated_from_id (referência circular)
    op.add_column(
        "citizen_requests",
        sa.Column(
            "escalated_from_id",
            UUID(as_uuid=True),
            nullable=True,
            comment="ID do pedido original, se este for escalado"
        )
    )
    
    # 5. Adicionar assigned_at
    op.add_column(
        "citizen_requests",
        sa.Column(
            "assigned_at",
            sa.DateTime,
            nullable=True,
            comment="Data de atribuição do pedido"
        )
    )
    
    # 6. Adicionar data (JSON para informações dinâmicas)
    op.add_column(
        "citizen_requests",
        sa.Column(
            "data",
            JSON,
            nullable=True,
            comment="Dados adicionais do pedido em formato JSON"
        )
    )
    
    # 7. Adicionar routing_justification
    op.add_column(
        "citizen_requests",
        sa.Column(
            "routing_justification",
            sa.Text,
            nullable=True,
            comment="Justificação para encaminhamento/escalamento"
        )
    )
    
    # 8. Adicionar resolved_by_id
    op.add_column(
        "citizen_requests",
        sa.Column(
            "resolved_by_id",
            UUID(as_uuid=True),
            nullable=True,
            comment="ID do utilizador que resolveu"
        )
    )
    
    # 9. Renomear resolution_note para resolution_notes (plural)
    # Primeiro adicionar a nova coluna
    op.add_column(
        "citizen_requests",
        sa.Column(
            "resolution_notes",
            sa.Text,
            nullable=True,
            comment="Notas de resolução"
        )
    )
    
    # Copiar dados se existirem
    try:
        op.execute(
            "UPDATE citizen_requests SET resolution_notes = resolution_note WHERE resolution_note IS NOT NULL"
        )
    except:
        pass  # Coluna pode não existir
    
    # Criar Foreign Keys
    op.create_foreign_key(
        "fk_citizen_requests_neighborhood_id",
        "citizen_requests",
        "territories",
        ["neighborhood_id"],
        ["id"],
        ondelete="SET NULL"
    )
    
    op.create_foreign_key(
        "fk_citizen_requests_current_territory_id",
        "citizen_requests",
        "territories",
        ["current_territory_id"],
        ["id"],
        ondelete="SET NULL"
    )
    
    op.create_foreign_key(
        "fk_citizen_requests_escalated_from_id",
        "citizen_requests",
        "citizen_requests",
        ["escalated_from_id"],
        ["id"],
        ondelete="SET NULL"
    )
    
    op.create_foreign_key(
        "fk_citizen_requests_resolved_by_id",
        "citizen_requests",
        "user",
        ["resolved_by_id"],
        ["id"],
        ondelete="SET NULL"
    )
    
    # Criar índices para performance
    op.create_index(
        "ix_citizen_requests_neighborhood_id",
        "citizen_requests",
        ["neighborhood_id"]
    )
    
    op.create_index(
        "ix_citizen_requests_current_territory_id",
        "citizen_requests",
        ["current_territory_id"]
    )
    
    op.create_index(
        "ix_citizen_requests_escalation_level",
        "citizen_requests",
        ["escalation_level"]
    )
    
    op.create_index(
        "ix_citizen_requests_escalated_from_id",
        "citizen_requests",
        ["escalated_from_id"]
    )
    
    op.create_index(
        "ix_citizen_requests_assigned_at",
        "citizen_requests",
        ["assigned_at"]
    )


def downgrade():
    # Remover índices
    op.drop_index("ix_citizen_requests_assigned_at")
    op.drop_index("ix_citizen_requests_escalated_from_id")
    op.drop_index("ix_citizen_requests_escalation_level")
    op.drop_index("ix_citizen_requests_current_territory_id")
    op.drop_index("ix_citizen_requests_neighborhood_id")
    
    # Remover foreign keys
    op.drop_constraint("fk_citizen_requests_resolved_by_id", "citizen_requests")
    op.drop_constraint("fk_citizen_requests_escalated_from_id", "citizen_requests")
    op.drop_constraint("fk_citizen_requests_current_territory_id", "citizen_requests")
    op.drop_constraint("fk_citizen_requests_neighborhood_id", "citizen_requests")
    
    # Remover colunas
    op.drop_column("citizen_requests", "resolution_notes")
    op.drop_column("citizen_requests", "resolved_by_id")
    op.drop_column("citizen_requests", "routing_justification")
    op.drop_column("citizen_requests", "data")
    op.drop_column("citizen_requests", "assigned_at")
    op.drop_column("citizen_requests", "escalated_from_id")
    op.drop_column("citizen_requests", "escalation_level")
    op.drop_column("citizen_requests", "current_territory_id")
    op.drop_column("citizen_requests", "neighborhood_id")
