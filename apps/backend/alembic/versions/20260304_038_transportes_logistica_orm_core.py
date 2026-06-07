"""create transportes_logistica orm core tables

Revision ID: 20260304_038_transportes_logistica_orm_core
Revises: 20260304_037_obras_publicas_orm_core
Create Date: 2026-03-04 21:30:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260304_038_transportes_logistica_orm_core"
down_revision = "20260304_037_obras_publicas_orm_core"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS transportes_logistica_viagens (
            id UUID PRIMARY KEY,
            linha_id UUID NOT NULL,
            veiculo_id UUID NOT NULL,
            motorista_id UUID NOT NULL,
            data_hora_saida TIMESTAMP NOT NULL,
            data_hora_chegada_prevista TIMESTAMP NOT NULL,
            origem VARCHAR(120) NOT NULL,
            destino VARCHAR(120) NOT NULL,
            itinerario JSONB NOT NULL DEFAULT '[]'::jsonb,
            status VARCHAR(40) NOT NULL,
            data_hora_chegada_real TIMESTAMP,
            paradas JSONB,
            passageiros_embarcados INTEGER,
            passageiros_desembarcados INTEGER,
            passageiros_transbordo INTEGER,
            carga JSONB,
            volume_carga NUMERIC(12,2),
            peso_carga NUMERIC(12,2),
            valor_frete NUMERIC(14,2),
            quilometragem_inicial INTEGER,
            quilometragem_final INTEGER,
            consumo_combustivel NUMERIC(12,2),
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS transportes_logistica_frotas (
            id UUID PRIMARY KEY,
            codigo_frota VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            operadora_id UUID NOT NULL,
            municipio VARCHAR(120) NOT NULL,
            provincia VARCHAR(120) NOT NULL,
            status VARCHAR(32) NOT NULL,
            data_cadastro DATE NOT NULL,
            data_atualizacao DATE,
            observacoes TEXT,
            veiculos JSONB NOT NULL DEFAULT '[]'::jsonb,
            manutencoes JSONB NOT NULL DEFAULT '[]'::jsonb,
            fiscalizacoes JSONB NOT NULL DEFAULT '[]'::jsonb,
            tarifas JSONB NOT NULL DEFAULT '[]'::jsonb,
            trilha_auditoria JSONB NOT NULL DEFAULT '[]'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_viagem_linha ON transportes_logistica_viagens (linha_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_viagem_veiculo ON transportes_logistica_viagens (veiculo_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_viagem_motorista ON transportes_logistica_viagens (motorista_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_viagem_saida ON transportes_logistica_viagens (data_hora_saida)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_viagem_origem ON transportes_logistica_viagens (origem)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_viagem_destino ON transportes_logistica_viagens (destino)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_viagem_status ON transportes_logistica_viagens (status)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_frota_codigo ON transportes_logistica_frotas (codigo_frota)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_frota_operadora ON transportes_logistica_frotas (operadora_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_frota_municipio ON transportes_logistica_frotas (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_frota_provincia ON transportes_logistica_frotas (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_frota_status ON transportes_logistica_frotas (status)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_tl_frota_status")
    op.execute("DROP INDEX IF EXISTS ix_tl_frota_provincia")
    op.execute("DROP INDEX IF EXISTS ix_tl_frota_municipio")
    op.execute("DROP INDEX IF EXISTS ix_tl_frota_operadora")
    op.execute("DROP INDEX IF EXISTS ix_tl_frota_codigo")
    op.execute("DROP INDEX IF EXISTS ix_tl_viagem_status")
    op.execute("DROP INDEX IF EXISTS ix_tl_viagem_destino")
    op.execute("DROP INDEX IF EXISTS ix_tl_viagem_origem")
    op.execute("DROP INDEX IF EXISTS ix_tl_viagem_saida")
    op.execute("DROP INDEX IF EXISTS ix_tl_viagem_motorista")
    op.execute("DROP INDEX IF EXISTS ix_tl_viagem_veiculo")
    op.execute("DROP INDEX IF EXISTS ix_tl_viagem_linha")

    op.execute("DROP TABLE IF EXISTS transportes_logistica_frotas")
    op.execute("DROP TABLE IF EXISTS transportes_logistica_viagens")
