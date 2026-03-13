"""create urbanismo_habitacao orm core tables

Revision ID: 20260304_036_urbanismo_habitacao_orm_core
Revises: 20260304_035_gestao_fundiaria_orm_core
Create Date: 2026-03-04 15:30:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260304_036_urbanismo_habitacao_orm_core"
down_revision = "20260304_035_gestao_fundiaria_orm_core"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_planos_diretores (
            id UUID PRIMARY KEY,
            codigo_plano VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            ano_elaboracao INTEGER NOT NULL,
            orgao_responsavel_id UUID NOT NULL,
            municipio VARCHAR(100),
            ano_aprovacao INTEGER,
            ano_publicacao INTEGER,
            periodo_validade_inicio DATE,
            periodo_validade_fim DATE,
            lei_aprovacao VARCHAR(120),
            participantes_consulta INTEGER,
            audiencias_publicas INTEGER,
            documento_url VARCHAR(500),
            mapa_url VARCHAR(500),
            area_total_urbana NUMERIC(18,2),
            area_total_rural NUMERIC(18,2),
            populacao_estimada INTEGER,
            densidade_media NUMERIC(12,4),
            macrozoneamento JSONB,
            diretrizes_gerais TEXT,
            objetivos_estrategicos TEXT,
            observacoes TEXT,
            data_publicacao DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_zoneamentos (
            id UUID PRIMARY KEY,
            codigo_zoneamento VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo_zona VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            plano_diretor_id UUID NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            usos_permitidos JSONB NOT NULL DEFAULT '[]'::jsonb,
            municipio VARCHAR(100),
            coeficiente_aproveitamento_max NUMERIC(12,4),
            taxa_ocupacao_max NUMERIC(12,4),
            gabarito_maximo INTEGER,
            recuo_frontal_minimo NUMERIC(12,4),
            permeabilidade_minima NUMERIC(12,4),
            area_lote_minima NUMERIC(18,2),
            data_inicio_vigencia DATE,
            data_cadastro DATE NOT NULL,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_operacoes_urbanas (
            id UUID PRIMARY KEY,
            codigo_operacao VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(64) NOT NULL,
            status VARCHAR(40) NOT NULL,
            plano_diretor_id UUID NOT NULL,
            orgao_responsavel_id UUID NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            municipio VARCHAR(100),
            area_intervencao NUMERIC(18,2),
            investimento_previsto NUMERIC(18,2),
            investimento_executado NUMERIC(18,2),
            data_inicio_prevista DATE,
            data_fim_prevista DATE,
            data_inicio_real DATE,
            data_fim_real DATE,
            percentual_execucao NUMERIC(5,2) NOT NULL DEFAULT 0,
            data_cadastro DATE NOT NULL,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_parcelamentos (
            id UUID PRIMARY KEY,
            codigo_parcelamento VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            plano_diretor_id UUID NOT NULL,
            zoneamento_id UUID NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            area_total NUMERIC(18,2) NOT NULL,
            quantidade_unidades_prevista INTEGER NOT NULL,
            municipio VARCHAR(100),
            area_publica_prevista NUMERIC(18,2),
            area_sistema_viario_prevista NUMERIC(18,2),
            quantidade_unidades_resultante INTEGER,
            data_cadastro DATE NOT NULL,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_loteamentos (
            id UUID PRIMARY KEY,
            codigo_loteamento VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            parcelamento_id UUID NOT NULL,
            plano_diretor_id UUID NOT NULL,
            zoneamento_id UUID NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            area_total NUMERIC(18,2) NOT NULL,
            quantidade_lotes_prevista INTEGER NOT NULL,
            municipio VARCHAR(100),
            quantidade_lotes_implantada INTEGER NOT NULL DEFAULT 0,
            area_lotes NUMERIC(18,2),
            area_verde NUMERIC(18,2),
            area_institucional NUMERIC(18,2),
            data_inicio_prevista DATE,
            data_fim_prevista DATE,
            data_inicio_real DATE,
            data_fim_real DATE,
            data_cadastro DATE NOT NULL,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_licencas_urbanisticas (
            id UUID PRIMARY KEY,
            codigo_licenca VARCHAR(40) NOT NULL UNIQUE,
            numero_processo VARCHAR(80) NOT NULL,
            tipo_alvara VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            requerente_id UUID NOT NULL,
            zoneamento_id UUID NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            municipio VARCHAR(100),
            endereco_obra VARCHAR(255),
            area_construida_prevista NUMERIC(18,2),
            data_requerimento DATE NOT NULL,
            data_emissao DATE,
            data_validade DATE,
            tecnico_responsavel_id UUID,
            observacoes TEXT,
            data_atualizacao DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_alvaras (
            id UUID PRIMARY KEY,
            codigo_alvara VARCHAR(40) NOT NULL UNIQUE,
            numero_processo VARCHAR(80) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            licenca_urbanistica_id UUID NOT NULL,
            requerente_id UUID NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            municipio VARCHAR(100),
            endereco_obra VARCHAR(255),
            area_autorizada NUMERIC(18,2),
            data_requerimento DATE NOT NULL,
            data_emissao DATE,
            data_validade DATE,
            analista_id UUID,
            observacoes TEXT,
            data_atualizacao DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS urbanismo_habitacao_habite_se (
            id UUID PRIMARY KEY,
            codigo_habite_se VARCHAR(40) NOT NULL UNIQUE,
            numero_processo VARCHAR(80) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            alvara_id UUID NOT NULL,
            requerente_id UUID NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            municipio VARCHAR(100),
            endereco_imovel VARCHAR(255),
            area_vistoriada NUMERIC(18,2),
            data_requerimento DATE NOT NULL,
            data_vistoria DATE,
            data_emissao DATE,
            data_validade DATE,
            tecnico_vistoriador_id UUID,
            observacoes TEXT,
            data_atualizacao DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_pd_codigo ON urbanismo_habitacao_planos_diretores (codigo_plano)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_pd_tipo ON urbanismo_habitacao_planos_diretores (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_pd_status ON urbanismo_habitacao_planos_diretores (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_pd_provincia ON urbanismo_habitacao_planos_diretores (provincia)")

    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_zon_codigo ON urbanismo_habitacao_zoneamentos (codigo_zoneamento)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_zon_tipo ON urbanismo_habitacao_zoneamentos (tipo_zona)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_zon_status ON urbanismo_habitacao_zoneamentos (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_zon_provincia ON urbanismo_habitacao_zoneamentos (provincia)")

    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_opu_codigo ON urbanismo_habitacao_operacoes_urbanas (codigo_operacao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_opu_tipo ON urbanismo_habitacao_operacoes_urbanas (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_opu_status ON urbanismo_habitacao_operacoes_urbanas (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_opu_provincia ON urbanismo_habitacao_operacoes_urbanas (provincia)")

    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_par_codigo ON urbanismo_habitacao_parcelamentos (codigo_parcelamento)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_par_tipo ON urbanismo_habitacao_parcelamentos (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_par_status ON urbanismo_habitacao_parcelamentos (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_par_provincia ON urbanismo_habitacao_parcelamentos (provincia)")

    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_lot_codigo ON urbanismo_habitacao_loteamentos (codigo_loteamento)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_lot_tipo ON urbanismo_habitacao_loteamentos (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_lot_status ON urbanismo_habitacao_loteamentos (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_lot_provincia ON urbanismo_habitacao_loteamentos (provincia)")

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_uh_lic_codigo ON urbanismo_habitacao_licencas_urbanisticas (codigo_licenca)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_uh_lic_tipo ON urbanismo_habitacao_licencas_urbanisticas (tipo_alvara)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_uh_lic_status ON urbanismo_habitacao_licencas_urbanisticas (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_uh_lic_provincia ON urbanismo_habitacao_licencas_urbanisticas (provincia)"
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_alv_codigo ON urbanismo_habitacao_alvaras (codigo_alvara)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_alv_tipo ON urbanismo_habitacao_alvaras (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_alv_status ON urbanismo_habitacao_alvaras (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_alv_provincia ON urbanismo_habitacao_alvaras (provincia)")

    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_hbt_codigo ON urbanismo_habitacao_habite_se (codigo_habite_se)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_hbt_tipo ON urbanismo_habitacao_habite_se (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_hbt_status ON urbanismo_habitacao_habite_se (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_uh_hbt_provincia ON urbanismo_habitacao_habite_se (provincia)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_uh_hbt_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_hbt_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_hbt_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_hbt_codigo")
    op.execute("DROP INDEX IF EXISTS ix_uh_alv_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_alv_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_alv_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_alv_codigo")
    op.execute("DROP INDEX IF EXISTS ix_uh_lic_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_lic_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_lic_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_lic_codigo")
    op.execute("DROP INDEX IF EXISTS ix_uh_lot_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_lot_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_lot_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_lot_codigo")
    op.execute("DROP INDEX IF EXISTS ix_uh_par_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_par_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_par_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_par_codigo")
    op.execute("DROP INDEX IF EXISTS ix_uh_opu_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_opu_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_opu_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_opu_codigo")
    op.execute("DROP INDEX IF EXISTS ix_uh_zon_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_zon_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_zon_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_zon_codigo")
    op.execute("DROP INDEX IF EXISTS ix_uh_pd_provincia")
    op.execute("DROP INDEX IF EXISTS ix_uh_pd_status")
    op.execute("DROP INDEX IF EXISTS ix_uh_pd_tipo")
    op.execute("DROP INDEX IF EXISTS ix_uh_pd_codigo")

    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_habite_se")
    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_alvaras")
    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_licencas_urbanisticas")
    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_loteamentos")
    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_parcelamentos")
    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_operacoes_urbanas")
    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_zoneamentos")
    op.execute("DROP TABLE IF EXISTS urbanismo_habitacao_planos_diretores")
