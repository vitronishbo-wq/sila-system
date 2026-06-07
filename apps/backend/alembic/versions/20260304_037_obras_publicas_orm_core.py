"""create obras_publicas orm core tables

Revision ID: 20260304_037_obras_publicas_orm_core
Revises: 20260304_036_urbanismo_habitacao_orm_core
Create Date: 2026-03-04 18:30:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260304_037_obras_publicas_orm_core"
down_revision = "20260304_036_urbanismo_habitacao_orm_core"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS obras_publicas_projetos (
            id UUID PRIMARY KEY,
            codigo_projeto VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            orgao_responsavel_id UUID NOT NULL,
            responsavel_tecnico_id UUID NOT NULL,
            valor_estimado NUMERIC(18,2) NOT NULL,
            data_inicio_prevista DATE NOT NULL,
            data_fim_prevista DATE NOT NULL,
            data_cadastro DATE NOT NULL,
            obra_id UUID,
            descricao TEXT,
            data_inicio_real DATE,
            data_fim_real DATE,
            versao INTEGER NOT NULL DEFAULT 1,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS obras_publicas_obras (
            id UUID PRIMARY KEY,
            codigo_obra VARCHAR(40) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            natureza VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            orgao_responsavel_id UUID NOT NULL,
            orgao_responsavel_tipo VARCHAR(80) NOT NULL,
            valor_orcado NUMERIC(18,2) NOT NULL,
            data_inicio_prevista DATE NOT NULL,
            data_fim_prevista DATE NOT NULL,
            endereco VARCHAR(255) NOT NULL,
            bairro VARCHAR(100) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            prazo_original_dias INTEGER NOT NULL,
            data_cadastro DATE NOT NULL,
            descricao TEXT,
            gestor_responsavel_id UUID,
            fiscal_responsavel_id UUID,
            empreiteira_id UUID,
            contrato_id UUID,
            projeto_id UUID,
            valor_contratado NUMERIC(18,2),
            valor_executado NUMERIC(18,2),
            valor_pago NUMERIC(18,2),
            data_inicio_real DATE,
            data_fim_real DATE,
            data_entrega DATE,
            coordenadas_lat NUMERIC(12,8),
            coordenadas_long NUMERIC(12,8),
            imovel_id UUID,
            percentual_executado NUMERIC(5,2) NOT NULL DEFAULT 0,
            prazo_adicionado_dias INTEGER NOT NULL DEFAULT 0,
            dias_corridos INTEGER NOT NULL DEFAULT 0,
            dias_atraso INTEGER NOT NULL DEFAULT 0,
            data_atualizacao DATE,
            observacoes TEXT,
            medicoes JSONB NOT NULL DEFAULT '[]'::jsonb,
            aditivos JSONB NOT NULL DEFAULT '[]'::jsonb,
            fiscalizacoes JSONB NOT NULL DEFAULT '[]'::jsonb,
            termos_recebimento JSONB NOT NULL DEFAULT '[]'::jsonb,
            trilha_auditoria JSONB NOT NULL DEFAULT '[]'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS obras_publicas_licitacoes (
            id UUID PRIMARY KEY,
            numero_licitacao VARCHAR(40) NOT NULL UNIQUE,
            objeto TEXT NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            obra_id UUID NOT NULL,
            orgao_responsavel_id UUID NOT NULL,
            valor_estimado NUMERIC(18,2) NOT NULL,
            data_publicacao_edital DATE NOT NULL,
            data_entrega_propostas DATE NOT NULL,
            data_cadastro DATE NOT NULL,
            data_abertura DATE,
            vencedor_id UUID,
            valor_adjudicado NUMERIC(18,2),
            data_homologacao DATE,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS obras_publicas_editais (
            id UUID PRIMARY KEY,
            numero_edital VARCHAR(40) NOT NULL UNIQUE,
            titulo VARCHAR(255) NOT NULL,
            objeto TEXT NOT NULL,
            licitacao_id UUID NOT NULL,
            status VARCHAR(40) NOT NULL,
            data_publicacao DATE NOT NULL,
            data_abertura DATE NOT NULL,
            data_encerramento DATE NOT NULL,
            data_cadastro DATE NOT NULL,
            versao INTEGER NOT NULL DEFAULT 1,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_prj_codigo ON obras_publicas_projetos (codigo_projeto)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_prj_tipo ON obras_publicas_projetos (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_prj_status ON obras_publicas_projetos (status)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_prj_orgao ON obras_publicas_projetos (orgao_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_prj_responsavel ON obras_publicas_projetos (responsavel_tecnico_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_prj_obra_id ON obras_publicas_projetos (obra_id)")

    op.execute("CREATE INDEX IF NOT EXISTS ix_op_obra_codigo ON obras_publicas_obras (codigo_obra)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_obra_tipo ON obras_publicas_obras (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_obra_natureza ON obras_publicas_obras (natureza)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_obra_status ON obras_publicas_obras (status)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_orgao_id ON obras_publicas_obras (orgao_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_orgao_tipo ON obras_publicas_obras (orgao_responsavel_tipo)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_obra_bairro ON obras_publicas_obras (bairro)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_municipio ON obras_publicas_obras (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_provincia ON obras_publicas_obras (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_gestor ON obras_publicas_obras (gestor_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_fiscal ON obras_publicas_obras (fiscal_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_empreiteira ON obras_publicas_obras (empreiteira_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_obra_contrato ON obras_publicas_obras (contrato_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_obra_projeto ON obras_publicas_obras (projeto_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_obra_imovel ON obras_publicas_obras (imovel_id)")

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_lic_numero ON obras_publicas_licitacoes (numero_licitacao)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_lic_tipo ON obras_publicas_licitacoes (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_lic_status ON obras_publicas_licitacoes (status)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_lic_obra_id ON obras_publicas_licitacoes (obra_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_lic_orgao ON obras_publicas_licitacoes (orgao_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_lic_vencedor ON obras_publicas_licitacoes (vencedor_id)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_edt_numero ON obras_publicas_editais (numero_edital)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_edt_licitacao ON obras_publicas_editais (licitacao_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_edt_status ON obras_publicas_editais (status)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_op_edt_status")
    op.execute("DROP INDEX IF EXISTS ix_op_edt_licitacao")
    op.execute("DROP INDEX IF EXISTS ix_op_edt_numero")
    op.execute("DROP INDEX IF EXISTS ix_op_lic_vencedor")
    op.execute("DROP INDEX IF EXISTS ix_op_lic_orgao")
    op.execute("DROP INDEX IF EXISTS ix_op_lic_obra_id")
    op.execute("DROP INDEX IF EXISTS ix_op_lic_status")
    op.execute("DROP INDEX IF EXISTS ix_op_lic_tipo")
    op.execute("DROP INDEX IF EXISTS ix_op_lic_numero")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_imovel")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_projeto")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_contrato")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_empreiteira")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_fiscal")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_gestor")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_provincia")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_municipio")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_bairro")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_orgao_tipo")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_orgao_id")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_status")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_natureza")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_tipo")
    op.execute("DROP INDEX IF EXISTS ix_op_obra_codigo")
    op.execute("DROP INDEX IF EXISTS ix_op_prj_obra_id")
    op.execute("DROP INDEX IF EXISTS ix_op_prj_responsavel")
    op.execute("DROP INDEX IF EXISTS ix_op_prj_orgao")
    op.execute("DROP INDEX IF EXISTS ix_op_prj_status")
    op.execute("DROP INDEX IF EXISTS ix_op_prj_tipo")
    op.execute("DROP INDEX IF EXISTS ix_op_prj_codigo")

    op.execute("DROP TABLE IF EXISTS obras_publicas_editais")
    op.execute("DROP TABLE IF EXISTS obras_publicas_licitacoes")
    op.execute("DROP TABLE IF EXISTS obras_publicas_obras")
    op.execute("DROP TABLE IF EXISTS obras_publicas_projetos")
