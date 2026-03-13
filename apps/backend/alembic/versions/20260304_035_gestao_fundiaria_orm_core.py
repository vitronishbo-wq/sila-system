"""create gestao_fundiaria orm core tables

Revision ID: 20260304_035_gestao_fundiaria_orm_core
Revises: 3261f0e24605
Create Date: 2026-03-04 12:30:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260304_035_gestao_fundiaria_orm_core"
down_revision = "3261f0e24605"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gestao_fundiaria_imoveis (
            id UUID PRIMARY KEY,
            inscricao_imobiliaria VARCHAR(50) NOT NULL UNIQUE,
            tipo VARCHAR(32) NOT NULL,
            natureza VARCHAR(32) NOT NULL,
            regime VARCHAR(32) NOT NULL,
            situacao VARCHAR(32) NOT NULL,
            area_total NUMERIC(18,2) NOT NULL,
            endereco VARCHAR(255) NOT NULL,
            bairro VARCHAR(100) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            data_cadastro DATE NOT NULL,
            area_privativa NUMERIC(18,2),
            area_construida NUMERIC(18,2),
            area_terreno NUMERIC(18,2),
            cep VARCHAR(20),
            coordenadas_lat NUMERIC(12,8),
            coordenadas_long NUMERIC(12,8),
            matricula_id UUID,
            proprietario_atual_id UUID,
            data_atualizacao DATE,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gestao_fundiaria_proprietarios (
            id UUID PRIMARY KEY,
            numero_cadastro VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            documento VARCHAR(64) NOT NULL UNIQUE,
            tipo_pessoa VARCHAR(24) NOT NULL,
            tipo_titularidade VARCHAR(32) NOT NULL,
            data_cadastro DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            percentual_titularidade NUMERIC(5,2),
            email VARCHAR(255),
            telefone VARCHAR(32),
            endereco VARCHAR(255),
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gestao_fundiaria_oneracoes (
            id UUID PRIMARY KEY,
            numero_oneracao VARCHAR(50) NOT NULL UNIQUE,
            imovel_inscricao VARCHAR(50) NOT NULL,
            tipo VARCHAR(32) NOT NULL,
            credor_nome VARCHAR(255) NOT NULL,
            valor NUMERIC(18,2) NOT NULL,
            data_registro DATE NOT NULL,
            status VARCHAR(24) NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            documento_credor VARCHAR(64),
            moeda VARCHAR(3) NOT NULL DEFAULT 'AOA',
            data_vencimento DATE,
            descricao TEXT,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gestao_fundiaria_desapropriacoes (
            id UUID PRIMARY KEY,
            numero_processo VARCHAR(50) NOT NULL UNIQUE,
            imovel_inscricao VARCHAR(50) NOT NULL,
            tipo VARCHAR(32) NOT NULL,
            ente_publico VARCHAR(255) NOT NULL,
            finalidade TEXT NOT NULL,
            valor_indenizacao NUMERIC(18,2) NOT NULL,
            data_inicio DATE NOT NULL,
            status VARCHAR(24) NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            data_decreto DATE,
            data_pagamento DATE,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gestao_fundiaria_matriculas_imovel (
            id UUID PRIMARY KEY,
            numero_matricula VARCHAR(60) NOT NULL UNIQUE,
            imovel_inscricao VARCHAR(50) NOT NULL,
            tipo_registro VARCHAR(24) NOT NULL,
            cartorio_nome VARCHAR(255) NOT NULL,
            livro VARCHAR(32) NOT NULL,
            folha VARCHAR(32) NOT NULL,
            comarca VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            data_registro DATE NOT NULL,
            status VARCHAR(24) NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            proprietario_documento VARCHAR(64),
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gestao_fundiaria_georreferenciamentos (
            id UUID PRIMARY KEY,
            codigo_geo VARCHAR(60) NOT NULL UNIQUE,
            imovel_inscricao VARCHAR(50) NOT NULL,
            latitude NUMERIC(12,8) NOT NULL,
            longitude NUMERIC(12,8) NOT NULL,
            sistema_referencia VARCHAR(24) NOT NULL,
            data_registro DATE NOT NULL,
            precisao_metros NUMERIC(10,2),
            area_calculada NUMERIC(18,2),
            validado BOOLEAN NOT NULL DEFAULT TRUE,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            data_atualizacao DATE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_imovel_inscricao ON gestao_fundiaria_imoveis (inscricao_imobiliaria)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_tipo ON gestao_fundiaria_imoveis (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_natureza ON gestao_fundiaria_imoveis (natureza)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_regime ON gestao_fundiaria_imoveis (regime)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_situacao ON gestao_fundiaria_imoveis (situacao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_bairro ON gestao_fundiaria_imoveis (bairro)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_municipio ON gestao_fundiaria_imoveis (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_provincia ON gestao_fundiaria_imoveis (provincia)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_imovel_matricula_id ON gestao_fundiaria_imoveis (matricula_id)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_imovel_proprietario_id ON gestao_fundiaria_imoveis (proprietario_atual_id)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_proprietario_numero ON gestao_fundiaria_proprietarios (numero_cadastro)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_proprietario_documento ON gestao_fundiaria_proprietarios (documento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_proprietario_tipo_pessoa ON gestao_fundiaria_proprietarios (tipo_pessoa)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_proprietario_titularidade ON gestao_fundiaria_proprietarios (tipo_titularidade)"
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_oneracao_numero ON gestao_fundiaria_oneracoes (numero_oneracao)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_oneracao_imovel_inscricao ON gestao_fundiaria_oneracoes (imovel_inscricao)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_oneracao_tipo ON gestao_fundiaria_oneracoes (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gf_oneracao_status ON gestao_fundiaria_oneracoes (status)")

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_desapropriacao_numero ON gestao_fundiaria_desapropriacoes (numero_processo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_desapropriacao_imovel_inscricao ON gestao_fundiaria_desapropriacoes (imovel_inscricao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_desapropriacao_tipo ON gestao_fundiaria_desapropriacoes (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_desapropriacao_status ON gestao_fundiaria_desapropriacoes (status)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_matricula_numero ON gestao_fundiaria_matriculas_imovel (numero_matricula)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_matricula_imovel_inscricao ON gestao_fundiaria_matriculas_imovel (imovel_inscricao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_matricula_tipo_registro ON gestao_fundiaria_matriculas_imovel (tipo_registro)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_matricula_comarca ON gestao_fundiaria_matriculas_imovel (comarca)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_matricula_provincia ON gestao_fundiaria_matriculas_imovel (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_matricula_status ON gestao_fundiaria_matriculas_imovel (status)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_geo_codigo ON gestao_fundiaria_georreferenciamentos (codigo_geo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_geo_imovel_inscricao ON gestao_fundiaria_georreferenciamentos (imovel_inscricao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_gf_geo_sistema_referencia ON gestao_fundiaria_georreferenciamentos (sistema_referencia)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_gf_geo_sistema_referencia")
    op.execute("DROP INDEX IF EXISTS ix_gf_geo_imovel_inscricao")
    op.execute("DROP INDEX IF EXISTS ix_gf_geo_codigo")
    op.execute("DROP INDEX IF EXISTS ix_gf_matricula_status")
    op.execute("DROP INDEX IF EXISTS ix_gf_matricula_provincia")
    op.execute("DROP INDEX IF EXISTS ix_gf_matricula_comarca")
    op.execute("DROP INDEX IF EXISTS ix_gf_matricula_tipo_registro")
    op.execute("DROP INDEX IF EXISTS ix_gf_matricula_imovel_inscricao")
    op.execute("DROP INDEX IF EXISTS ix_gf_matricula_numero")
    op.execute("DROP INDEX IF EXISTS ix_gf_desapropriacao_status")
    op.execute("DROP INDEX IF EXISTS ix_gf_desapropriacao_tipo")
    op.execute("DROP INDEX IF EXISTS ix_gf_desapropriacao_imovel_inscricao")
    op.execute("DROP INDEX IF EXISTS ix_gf_desapropriacao_numero")
    op.execute("DROP INDEX IF EXISTS ix_gf_oneracao_status")
    op.execute("DROP INDEX IF EXISTS ix_gf_oneracao_tipo")
    op.execute("DROP INDEX IF EXISTS ix_gf_oneracao_imovel_inscricao")
    op.execute("DROP INDEX IF EXISTS ix_gf_oneracao_numero")
    op.execute("DROP INDEX IF EXISTS ix_gf_proprietario_titularidade")
    op.execute("DROP INDEX IF EXISTS ix_gf_proprietario_tipo_pessoa")
    op.execute("DROP INDEX IF EXISTS ix_gf_proprietario_documento")
    op.execute("DROP INDEX IF EXISTS ix_gf_proprietario_numero")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_proprietario_id")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_matricula_id")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_provincia")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_municipio")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_bairro")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_situacao")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_regime")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_natureza")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_tipo")
    op.execute("DROP INDEX IF EXISTS ix_gf_imovel_inscricao")

    op.execute("DROP TABLE IF EXISTS gestao_fundiaria_georreferenciamentos")
    op.execute("DROP TABLE IF EXISTS gestao_fundiaria_matriculas_imovel")
    op.execute("DROP TABLE IF EXISTS gestao_fundiaria_desapropriacoes")
    op.execute("DROP TABLE IF EXISTS gestao_fundiaria_oneracoes")
    op.execute("DROP TABLE IF EXISTS gestao_fundiaria_proprietarios")
    op.execute("DROP TABLE IF EXISTS gestao_fundiaria_imoveis")
