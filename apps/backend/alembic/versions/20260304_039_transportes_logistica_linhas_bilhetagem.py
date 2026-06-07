"""expand transportes_logistica with linhas, veiculos and bilhetagem

Revision ID: 20260304_039_transportes_logistica_linhas_bilhetagem
Revises: 20260304_038_transportes_logistica_orm_core
Create Date: 2026-03-04 22:15:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260304_039_transportes_logistica_linhas_bilhetagem"
down_revision = "20260304_038_transportes_logistica_orm_core"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS transportes_logistica_linhas (
            id UUID PRIMARY KEY,
            codigo VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            modal VARCHAR(32) NOT NULL,
            tipo_viagem VARCHAR(32) NOT NULL,
            origem VARCHAR(120) NOT NULL,
            destino VARCHAR(120) NOT NULL,
            itinerario JSONB NOT NULL DEFAULT '[]'::jsonb,
            extensao_km NUMERIC(10,2) NOT NULL,
            tempo_estimado_minutos INTEGER NOT NULL,
            dias_operacao JSONB NOT NULL DEFAULT '[]'::jsonb,
            horario_inicio VARCHAR(5) NOT NULL,
            horario_fim VARCHAR(5) NOT NULL,
            tarifa_base NUMERIC(10,2) NOT NULL,
            operadora_id UUID NOT NULL,
            status VARCHAR(32) NOT NULL,
            data_cadastro DATE NOT NULL,
            frequencia_media_minutos INTEGER,
            concessionaria_id UUID,
            outorga_id UUID,
            data_inicio_operacao DATE,
            data_autorizacao DATE,
            data_validade_autorizacao DATE,
            frota_necessaria INTEGER,
            frota_operante INTEGER,
            demanda_media_diaria INTEGER,
            oferta_media_diaria INTEGER,
            ocupacao_media NUMERIC(5,2),
            regularidade NUMERIC(5,2),
            pontualidade NUMERIC(5,2),
            acessivel BOOLEAN NOT NULL DEFAULT FALSE,
            ar_condicionado BOOLEAN NOT NULL DEFAULT FALSE,
            wifi BOOLEAN NOT NULL DEFAULT FALSE,
            sanitario BOOLEAN NOT NULL DEFAULT FALSE,
            observacoes TEXT,
            data_atualizacao DATE,
            veiculos_ativos JSONB NOT NULL DEFAULT '[]'::jsonb,
            trilha_auditoria JSONB NOT NULL DEFAULT '[]'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS transportes_logistica_veiculos (
            id UUID PRIMARY KEY,
            placa VARCHAR(16) NOT NULL UNIQUE,
            tipo VARCHAR(40) NOT NULL,
            marca VARCHAR(80) NOT NULL,
            modelo VARCHAR(80) NOT NULL,
            ano_fabricacao INTEGER NOT NULL,
            ano_modelo INTEGER NOT NULL,
            proprietario_id UUID NOT NULL,
            proprietario_tipo VARCHAR(20) NOT NULL,
            data_aquisicao DATE NOT NULL,
            status VARCHAR(32) NOT NULL,
            capacidade_passageiros INTEGER,
            capacidade_carga_kg NUMERIC(12,2),
            capacidade_carga_m3 NUMERIC(12,2),
            comprimento NUMERIC(10,2),
            largura NUMERIC(10,2),
            altura NUMERIC(10,2),
            peso_bruto_total NUMERIC(12,2),
            numero_eixos INTEGER,
            combustivel VARCHAR(32),
            consumo_medio NUMERIC(12,2),
            operadora_id UUID,
            licenciamento JSONB,
            seguro JSONB,
            rastreador_id VARCHAR(100),
            data_ultima_manutencao DATE,
            data_proxima_manutencao DATE,
            quilometragem INTEGER,
            observacoes TEXT,
            data_atualizacao DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS transportes_logistica_bilhetagem_eventos (
            id UUID PRIMARY KEY,
            codigo_bilhete VARCHAR(64) NOT NULL,
            viagem_id UUID NOT NULL,
            tipo_tarifa VARCHAR(32) NOT NULL,
            valor_pago NUMERIC(12,2) NOT NULL,
            forma_pagamento VARCHAR(32) NOT NULL,
            data_evento TIMESTAMP NOT NULL,
            status_reconciliacao VARCHAR(20) NOT NULL,
            lancamento_financeiro_id VARCHAR(80),
            referencia_externa VARCHAR(120),
            metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_linha_codigo ON transportes_logistica_linhas (codigo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_linha_modal ON transportes_logistica_linhas (modal)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_linha_tipo_viagem ON transportes_logistica_linhas (tipo_viagem)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_linha_origem ON transportes_logistica_linhas (origem)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_linha_destino ON transportes_logistica_linhas (destino)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_linha_operadora ON transportes_logistica_linhas (operadora_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_linha_status ON transportes_logistica_linhas (status)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_veiculo_placa ON transportes_logistica_veiculos (placa)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_veiculo_tipo ON transportes_logistica_veiculos (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_veiculo_status ON transportes_logistica_veiculos (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_veiculo_operadora ON transportes_logistica_veiculos (operadora_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_veiculo_proprietario ON transportes_logistica_veiculos (proprietario_id)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_bilhetagem_codigo ON transportes_logistica_bilhetagem_eventos (codigo_bilhete)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_bilhetagem_viagem ON transportes_logistica_bilhetagem_eventos (viagem_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_bilhetagem_tarifa ON transportes_logistica_bilhetagem_eventos (tipo_tarifa)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_bilhetagem_data_evento ON transportes_logistica_bilhetagem_eventos (data_evento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_bilhetagem_status ON transportes_logistica_bilhetagem_eventos (status_reconciliacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_tl_bilhetagem_lancamento ON transportes_logistica_bilhetagem_eventos (lancamento_financeiro_id)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_tl_bilhetagem_lancamento")
    op.execute("DROP INDEX IF EXISTS ix_tl_bilhetagem_status")
    op.execute("DROP INDEX IF EXISTS ix_tl_bilhetagem_data_evento")
    op.execute("DROP INDEX IF EXISTS ix_tl_bilhetagem_tarifa")
    op.execute("DROP INDEX IF EXISTS ix_tl_bilhetagem_viagem")
    op.execute("DROP INDEX IF EXISTS ix_tl_bilhetagem_codigo")

    op.execute("DROP INDEX IF EXISTS ix_tl_veiculo_proprietario")
    op.execute("DROP INDEX IF EXISTS ix_tl_veiculo_operadora")
    op.execute("DROP INDEX IF EXISTS ix_tl_veiculo_status")
    op.execute("DROP INDEX IF EXISTS ix_tl_veiculo_tipo")
    op.execute("DROP INDEX IF EXISTS ix_tl_veiculo_placa")

    op.execute("DROP INDEX IF EXISTS ix_tl_linha_status")
    op.execute("DROP INDEX IF EXISTS ix_tl_linha_operadora")
    op.execute("DROP INDEX IF EXISTS ix_tl_linha_destino")
    op.execute("DROP INDEX IF EXISTS ix_tl_linha_origem")
    op.execute("DROP INDEX IF EXISTS ix_tl_linha_tipo_viagem")
    op.execute("DROP INDEX IF EXISTS ix_tl_linha_modal")
    op.execute("DROP INDEX IF EXISTS ix_tl_linha_codigo")

    op.execute("DROP TABLE IF EXISTS transportes_logistica_bilhetagem_eventos")
    op.execute("DROP TABLE IF EXISTS transportes_logistica_veiculos")
    op.execute("DROP TABLE IF EXISTS transportes_logistica_linhas")
