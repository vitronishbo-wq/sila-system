"""create juventude expanded slices tables

Revision ID: 20260303_034_juventude_expansao_slices
Revises: 20260303_033_juventude_risco_evasao
Create Date: 2026-03-03 12:00:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260303_034_juventude_expansao_slices"
down_revision = "20260303_033_juventude_risco_evasao"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_bolsas_estudo (
            id UUID PRIMARY KEY,
            codigo_bolsa VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            valor_mensal NUMERIC(12,2) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativa BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_estagios (
            id UUID PRIMARY KEY,
            codigo_estagio VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            instituicao VARCHAR(200) NOT NULL,
            area_interesse VARCHAR(40) NOT NULL,
            cargo VARCHAR(120) NOT NULL,
            carga_horaria_semanal INTEGER NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            status VARCHAR(30) NOT NULL,
            bolsa_auxilio NUMERIC(12,2),
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_intercambios (
            id UUID PRIMARY KEY,
            codigo_intercambio VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            pais_destino VARCHAR(80) NOT NULL,
            instituicao_destino VARCHAR(200) NOT NULL,
            area_interesse VARCHAR(40) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            status VARCHAR(30) NOT NULL,
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_mentores (
            id UUID PRIMARY KEY,
            codigo_mentor VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo_mentoria VARCHAR(40) NOT NULL,
            area_interesse VARCHAR(40) NOT NULL,
            email VARCHAR(120),
            telefone VARCHAR(30),
            jovem_ids UUID[],
            status VARCHAR(30) NOT NULL,
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_eventos (
            id UUID PRIMARY KEY,
            codigo_evento VARCHAR(50) NOT NULL UNIQUE,
            titulo VARCHAR(200) NOT NULL,
            tipo_evento VARCHAR(30) NOT NULL,
            area_interesse VARCHAR(40) NOT NULL,
            data_evento DATE NOT NULL,
            local VARCHAR(200) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            vagas INTEGER,
            participantes UUID[],
            status VARCHAR(30) NOT NULL,
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_voluntariados (
            id UUID PRIMARY KEY,
            codigo_voluntariado VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            organizacao VARCHAR(200) NOT NULL,
            causa VARCHAR(40) NOT NULL,
            carga_horaria_total INTEGER NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            status VARCHAR(30) NOT NULL,
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_empreendimentos (
            id UUID PRIMARY KEY,
            codigo_empreendimento VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            nome_negocio VARCHAR(200) NOT NULL,
            area_interesse VARCHAR(40) NOT NULL,
            status VARCHAR(30) NOT NULL,
            receita_mensal NUMERIC(14,2),
            valor_credito NUMERIC(14,2),
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_saude_registos (
            id UUID PRIMARY KEY,
            codigo_registo VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            tipo_registo VARCHAR(30) NOT NULL,
            descricao TEXT NOT NULL,
            data_registo DATE NOT NULL,
            status_acompanhamento VARCHAR(30) NOT NULL,
            encaminhamento_necessario BOOLEAN NOT NULL DEFAULT FALSE,
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_acompanhamentos (
            id UUID PRIMARY KEY,
            codigo_acompanhamento VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            responsavel VARCHAR(200) NOT NULL,
            objetivo TEXT NOT NULL,
            data_inicio DATE NOT NULL,
            data_registo DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            proxima_revisao DATE,
            historico JSONB,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_inscricoes_programa (
            id UUID PRIMARY KEY,
            codigo_inscricao VARCHAR(50) NOT NULL UNIQUE,
            programa_id UUID NOT NULL,
            jovem_id UUID NOT NULL,
            data_inscricao DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            prioridade INTEGER NOT NULL DEFAULT 0,
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_politicas (
            id UUID PRIMARY KEY,
            codigo_politica VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            descricao TEXT NOT NULL,
            area_interesse VARCHAR(40) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            status VARCHAR(30) NOT NULL,
            metas JSONB,
            indicadores TEXT[],
            data_cadastro DATE NOT NULL,
            observacoes TEXT,
            ativa BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_bolsa_codigo ON juventude_bolsas_estudo (codigo_bolsa)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_bolsa_jovem ON juventude_bolsas_estudo (jovem_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_estagio_codigo ON juventude_estagios (codigo_estagio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_estagio_jovem ON juventude_estagios (jovem_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_intercambio_codigo ON juventude_intercambios (codigo_intercambio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_intercambio_jovem ON juventude_intercambios (jovem_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_mentor_codigo ON juventude_mentores (codigo_mentor)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_evento_codigo ON juventude_eventos (codigo_evento)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_voluntariado_codigo ON juventude_voluntariados (codigo_voluntariado)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_empreendimento_codigo ON juventude_empreendimentos (codigo_empreendimento)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_saude_codigo ON juventude_saude_registos (codigo_registo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_acomp_codigo ON juventude_acompanhamentos (codigo_acompanhamento)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_inscricao_codigo ON juventude_inscricoes_programa (codigo_inscricao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_inscricao_prog_jovem ON juventude_inscricoes_programa (programa_id, jovem_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juv_politica_codigo ON juventude_politicas (codigo_politica)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_juv_politica_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_inscricao_prog_jovem")
    op.execute("DROP INDEX IF EXISTS ix_juv_inscricao_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_acomp_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_saude_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_empreendimento_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_voluntariado_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_evento_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_mentor_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_intercambio_jovem")
    op.execute("DROP INDEX IF EXISTS ix_juv_intercambio_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_estagio_jovem")
    op.execute("DROP INDEX IF EXISTS ix_juv_estagio_codigo")
    op.execute("DROP INDEX IF EXISTS ix_juv_bolsa_jovem")
    op.execute("DROP INDEX IF EXISTS ix_juv_bolsa_codigo")
    op.execute("DROP TABLE IF EXISTS juventude_politicas")
    op.execute("DROP TABLE IF EXISTS juventude_inscricoes_programa")
    op.execute("DROP TABLE IF EXISTS juventude_acompanhamentos")
    op.execute("DROP TABLE IF EXISTS juventude_saude_registos")
    op.execute("DROP TABLE IF EXISTS juventude_empreendimentos")
    op.execute("DROP TABLE IF EXISTS juventude_voluntariados")
    op.execute("DROP TABLE IF EXISTS juventude_eventos")
    op.execute("DROP TABLE IF EXISTS juventude_mentores")
    op.execute("DROP TABLE IF EXISTS juventude_intercambios")
    op.execute("DROP TABLE IF EXISTS juventude_estagios")
    op.execute("DROP TABLE IF EXISTS juventude_bolsas_estudo")
