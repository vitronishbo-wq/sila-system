"""create defesa_consumidor reclamacoes table

Revision ID: 20260306_050_defesa_consumidor_reclamacoes
Revises: 20260306_049_patrimonio_cultural_foundation
Create Date: 2026-03-06 12:05:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260306_050_defesa_consumidor_reclamacoes"
down_revision = "20260306_049_patrimonio_cultural_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dc_reclamacoes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("protocolo", sa.String(length=50), nullable=False),
        sa.Column("consumidor_id", sa.Integer(), nullable=False),
        sa.Column("estabelecimento_id", sa.Integer(), nullable=False),
        sa.Column("produto_servico", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("categoria", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="aberta"),
        sa.Column("prioridade", sa.String(length=32), nullable=False, server_default="media"),
        sa.Column("valor_reclamado", sa.Float(), nullable=True),
        sa.Column("data_abertura", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("data_resolucao", sa.DateTime(), nullable=True),
        sa.Column("resolvido", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("descricao_resposta", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("protocolo", name="uq_dc_reclamacoes_protocolo"),
        sa.CheckConstraint(
            "status IN ('aberta','em_analise','em_mediacao','aguardando_consumidor','aguardando_estabelecimento','encerrada','cancelada')",
            name="ck_dc_reclamacoes_status",
        ),
        sa.CheckConstraint(
            "prioridade IN ('baixa','media','alta','critica')",
            name="ck_dc_reclamacoes_prioridade",
        ),
        sa.CheckConstraint(
            "categoria IN ('produto_defectuoso','servico_nao_prestado','propaganda_enganosa','cobranca_indevida','atendimento_inadequado','recusa_venda','outros')",
            name="ck_dc_reclamacoes_categoria",
        ),
        sa.CheckConstraint(
            "valor_reclamado IS NULL OR valor_reclamado >= 0",
            name="ck_dc_reclamacoes_valor_reclamado",
        ),
    )

    op.create_index(
        "ix_dc_reclamacoes_consumidor_id",
        "dc_reclamacoes",
        ["consumidor_id"],
        unique=False,
    )
    op.create_index(
        "ix_dc_reclamacoes_estabelecimento_id",
        "dc_reclamacoes",
        ["estabelecimento_id"],
        unique=False,
    )
    op.create_index(
        "ix_dc_reclamacoes_status_data",
        "dc_reclamacoes",
        ["status", "data_abertura"],
        unique=False,
    )
    op.create_index(
        "ix_dc_reclamacoes_consumidor_status",
        "dc_reclamacoes",
        ["consumidor_id", "status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_dc_reclamacoes_consumidor_status", table_name="dc_reclamacoes")
    op.drop_index("ix_dc_reclamacoes_status_data", table_name="dc_reclamacoes")
    op.drop_index("ix_dc_reclamacoes_estabelecimento_id", table_name="dc_reclamacoes")
    op.drop_index("ix_dc_reclamacoes_consumidor_id", table_name="dc_reclamacoes")
    op.drop_table("dc_reclamacoes")
