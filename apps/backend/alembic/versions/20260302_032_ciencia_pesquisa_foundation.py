"""create ciencia_pesquisa foundation tables

Revision ID: 20260302_032_ciencia_pesquisa_foundation
Revises: 20260302_031_protecao_civil_despachos_atendimentos
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_032_ciencia_pesquisa_foundation"
down_revision = "20260302_031_protecao_civil_despachos_atendimentos"
branch_labels = None
depends_on = None


def _create_instituicoes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS ciencia_instituicoes_pesquisa (
            id UUID PRIMARY KEY,
            sigla VARCHAR(30) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            nif VARCHAR(40) NOT NULL UNIQUE,
            tipo VARCHAR(40) NOT NULL,
            natureza_juridica VARCHAR(40) NOT NULL,
            pais VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            endereco VARCHAR(255) NOT NULL,
            email_institucional VARCHAR(120) NOT NULL,
            telefone VARCHAR(30),
            website VARCHAR(255),
            status_credenciamento VARCHAR(30) NOT NULL DEFAULT 'em_analise',
            data_credenciamento DATE,
            data_validade_credenciamento DATE,
            comite_etica_ativo BOOLEAN NOT NULL DEFAULT FALSE,
            nucleo_inovacao_ativo BOOLEAN NOT NULL DEFAULT FALSE,
            ativa BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_ciencia_instituicoes_campos_basicos'
                  AND conrelid = 'ciencia_instituicoes_pesquisa'::regclass
            ) THEN
                ALTER TABLE ciencia_instituicoes_pesquisa
                ADD CONSTRAINT ck_ciencia_instituicoes_campos_basicos
                CHECK (
                    char_length(trim(sigla)) >= 2
                    AND char_length(trim(nome)) >= 3
                    AND position('@' in email_institucional) > 1
                    AND (
                        data_validade_credenciamento IS NULL
                        OR data_credenciamento IS NULL
                        OR data_validade_credenciamento >= data_credenciamento
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_ciencia_instituicoes_enums'
                  AND conrelid = 'ciencia_instituicoes_pesquisa'::regclass
            ) THEN
                ALTER TABLE ciencia_instituicoes_pesquisa
                ADD CONSTRAINT ck_ciencia_instituicoes_enums
                CHECK (
                    tipo IN (
                        'universidade',
                        'instituto',
                        'centro_pesquisa',
                        'laboratorio',
                        'fundacao',
                        'empresa'
                    )
                    AND natureza_juridica IN (
                        'publica',
                        'privada',
                        'comunitaria',
                        'publico_privada'
                    )
                    AND status_credenciamento IN (
                        'em_analise',
                        'credenciada',
                        'suspensa',
                        'descredenciada'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_sigla ON ciencia_instituicoes_pesquisa (sigla)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_nome ON ciencia_instituicoes_pesquisa (nome)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_nif ON ciencia_instituicoes_pesquisa (nif)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_tipo ON ciencia_instituicoes_pesquisa (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_natureza ON ciencia_instituicoes_pesquisa (natureza_juridica)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_provincia ON ciencia_instituicoes_pesquisa (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_municipio ON ciencia_instituicoes_pesquisa (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_email ON ciencia_instituicoes_pesquisa (email_institucional)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_status ON ciencia_instituicoes_pesquisa (status_credenciamento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_instituicoes_ativa ON ciencia_instituicoes_pesquisa (ativa)"
    )


def _create_pesquisadores_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS ciencia_pesquisadores (
            id UUID PRIMARY KEY,
            nome_completo VARCHAR(255) NOT NULL,
            documento_identificacao VARCHAR(60) NOT NULL UNIQUE,
            email_institucional VARCHAR(120) NOT NULL UNIQUE,
            instituicao_id UUID,
            unidade_pesquisa_id UUID,
            area_conhecimento VARCHAR(50) NOT NULL,
            nivel_formacao VARCHAR(30) NOT NULL,
            tipo_vinculo VARCHAR(30) NOT NULL,
            status_vinculo VARCHAR(30) NOT NULL,
            data_inicio_vinculo DATE NOT NULL,
            data_fim_vinculo DATE,
            telefone VARCHAR(30),
            orcid VARCHAR(40),
            lattes_url VARCHAR(255),
            researcher_id VARCHAR(50),
            scopus_id VARCHAR(50),
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_ciencia_pesquisadores_campos_basicos'
                  AND conrelid = 'ciencia_pesquisadores'::regclass
            ) THEN
                ALTER TABLE ciencia_pesquisadores
                ADD CONSTRAINT ck_ciencia_pesquisadores_campos_basicos
                CHECK (
                    char_length(trim(nome_completo)) >= 3
                    AND position('@' in email_institucional) > 1
                    AND (data_fim_vinculo IS NULL OR data_fim_vinculo >= data_inicio_vinculo)
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_ciencia_pesquisadores_enums'
                  AND conrelid = 'ciencia_pesquisadores'::regclass
            ) THEN
                ALTER TABLE ciencia_pesquisadores
                ADD CONSTRAINT ck_ciencia_pesquisadores_enums
                CHECK (
                    area_conhecimento IN (
                        'ciencias_exatas',
                        'ciencias_biologicas',
                        'ciencias_saude',
                        'ciencias_agrarias',
                        'ciencias_sociais_aplicadas',
                        'engenharias',
                        'linguistica_artes',
                        'humanidades',
                        'multidisciplinar'
                    )
                    AND nivel_formacao IN (
                        'graduado',
                        'especialista',
                        'mestre',
                        'doutor',
                        'pos_doutor'
                    )
                    AND tipo_vinculo IN (
                        'efetivo',
                        'bolsista',
                        'colaborador',
                        'visitante',
                        'voluntario'
                    )
                    AND status_vinculo IN (
                        'ativo',
                        'afastado',
                        'suspenso',
                        'encerrado'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_nome ON ciencia_pesquisadores (nome_completo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_documento ON ciencia_pesquisadores (documento_identificacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_email ON ciencia_pesquisadores (email_institucional)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_instituicao_id ON ciencia_pesquisadores (instituicao_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_unidade_id ON ciencia_pesquisadores (unidade_pesquisa_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_area ON ciencia_pesquisadores (area_conhecimento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_nivel ON ciencia_pesquisadores (nivel_formacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_tipo_vinculo ON ciencia_pesquisadores (tipo_vinculo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_status ON ciencia_pesquisadores (status_vinculo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_ativo ON ciencia_pesquisadores (ativo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_orcid ON ciencia_pesquisadores (orcid)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_researcher_id ON ciencia_pesquisadores (researcher_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_pesquisadores_scopus_id ON ciencia_pesquisadores (scopus_id)"
    )


def _create_projetos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS ciencia_projetos_pesquisa (
            id UUID PRIMARY KEY,
            codigo_projeto VARCHAR(50) NOT NULL UNIQUE,
            titulo VARCHAR(255) NOT NULL,
            resumo TEXT NOT NULL,
            instituicao_id UUID NOT NULL,
            coordenador_id UUID NOT NULL,
            equipe_pesquisadores_ids UUID[] NOT NULL DEFAULT '{}',
            area_conhecimento VARCHAR(50) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim_prevista DATE,
            data_fim_real DATE,
            status VARCHAR(30) NOT NULL DEFAULT 'submetido',
            palavras_chave VARCHAR(80)[],
            orcamento_previsto NUMERIC(14, 2),
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_ciencia_projetos_campos_basicos'
                  AND conrelid = 'ciencia_projetos_pesquisa'::regclass
            ) THEN
                ALTER TABLE ciencia_projetos_pesquisa
                ADD CONSTRAINT ck_ciencia_projetos_campos_basicos
                CHECK (
                    char_length(trim(codigo_projeto)) >= 8
                    AND char_length(trim(titulo)) >= 5
                    AND char_length(trim(resumo)) >= 10
                    AND (data_fim_prevista IS NULL OR data_fim_prevista >= data_inicio)
                    AND (data_fim_real IS NULL OR data_fim_real >= data_inicio)
                    AND (orcamento_previsto IS NULL OR orcamento_previsto >= 0)
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_ciencia_projetos_enums'
                  AND conrelid = 'ciencia_projetos_pesquisa'::regclass
            ) THEN
                ALTER TABLE ciencia_projetos_pesquisa
                ADD CONSTRAINT ck_ciencia_projetos_enums
                CHECK (
                    area_conhecimento IN (
                        'ciencias_exatas',
                        'ciencias_biologicas',
                        'ciencias_saude',
                        'ciencias_agrarias',
                        'ciencias_sociais_aplicadas',
                        'engenharias',
                        'linguistica_artes',
                        'humanidades',
                        'multidisciplinar'
                    )
                    AND status IN (
                        'rascunho',
                        'submetido',
                        'aprovado',
                        'em_execucao',
                        'suspenso',
                        'encerrado',
                        'cancelado'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_codigo ON ciencia_projetos_pesquisa (codigo_projeto)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_titulo ON ciencia_projetos_pesquisa (titulo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_instituicao_id ON ciencia_projetos_pesquisa (instituicao_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_coordenador_id ON ciencia_projetos_pesquisa (coordenador_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_area ON ciencia_projetos_pesquisa (area_conhecimento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_status ON ciencia_projetos_pesquisa (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_data_inicio ON ciencia_projetos_pesquisa (data_inicio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_ativo ON ciencia_projetos_pesquisa (ativo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_ciencia_projetos_equipe_gin ON ciencia_projetos_pesquisa USING GIN (equipe_pesquisadores_ids)"
    )


def upgrade() -> None:
    _create_instituicoes_table()
    _create_pesquisadores_table()
    _create_projetos_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_equipe_gin")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_data_inicio")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_status")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_area")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_coordenador_id")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_instituicao_id")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_titulo")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_projetos_codigo")
    op.execute("DROP TABLE IF EXISTS ciencia_projetos_pesquisa")

    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_scopus_id")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_researcher_id")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_orcid")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_ativo")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_status")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_tipo_vinculo")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_nivel")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_area")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_instituicao_id")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_email")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_documento")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_pesquisadores_nome")
    op.execute("DROP TABLE IF EXISTS ciencia_pesquisadores")

    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_ativa")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_status")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_email")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_municipio")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_provincia")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_natureza")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_tipo")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_nif")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_nome")
    op.execute("DROP INDEX IF EXISTS ix_ciencia_instituicoes_sigla")
    op.execute("DROP TABLE IF EXISTS ciencia_instituicoes_pesquisa")
