"""create cultura slice3 tables for espacos, projetos e editais

Revision ID: 20260305_046_cultura_slice3_espacos_projetos_editais
Revises: 20260305_045_obras_publicas_event_sourcing_governance
Create Date: 2026-03-05 06:10:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260305_046_cultura_slice3_espacos_projetos_editais"
down_revision = "20260305_045_obras_publicas_event_sourcing_governance"
branch_labels = None
depends_on = None


def _create_espacos_culturais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_espacos_culturais (
            id UUID PRIMARY KEY,
            codigo_espaco VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            municipio VARCHAR(120) NOT NULL,
            provincia VARCHAR(120) NOT NULL,
            endereco VARCHAR(255) NOT NULL,
            capacidade INTEGER NOT NULL,
            area_m2 DOUBLE PRECISION NOT NULL,
            administracao VARCHAR(40) NOT NULL,
            responsavel_cpf VARCHAR(32) NOT NULL,
            data_registro DATE NOT NULL,
            orgao_gestor VARCHAR(200),
            ano_inauguracao INTEGER,
            acessibilidade BOOLEAN NOT NULL DEFAULT FALSE,
            visitas_anuais INTEGER NOT NULL DEFAULT 0,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            observacoes TEXT,
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
                WHERE conname = 'ck_cultura_espacos_tipo'
                  AND conrelid = 'cultura_espacos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_espacos_culturais
                ADD CONSTRAINT ck_cultura_espacos_tipo
                CHECK (
                    tipo IN (
                        'teatro',
                        'museu',
                        'centro_cultural',
                        'biblioteca',
                        'galeria',
                        'cinema',
                        'auditorio',
                        'sala_exposicao'
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
                WHERE conname = 'ck_cultura_espacos_integridade'
                  AND conrelid = 'cultura_espacos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_espacos_culturais
                ADD CONSTRAINT ck_cultura_espacos_integridade
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND capacidade > 0
                    AND area_m2 > 0
                    AND visitas_anuais >= 0
                    AND administracao IN ('PUBLICA', 'PRIVADA', 'MISTA')
                    AND (
                        ano_inauguracao IS NULL
                        OR (ano_inauguracao >= 1800 AND ano_inauguracao <= EXTRACT(YEAR FROM CURRENT_DATE))
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_codigo ON cultura_espacos_culturais (codigo_espaco)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_nome ON cultura_espacos_culturais (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_tipo ON cultura_espacos_culturais (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_municipio ON cultura_espacos_culturais (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_provincia ON cultura_espacos_culturais (provincia)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_administracao ON cultura_espacos_culturais (administracao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_responsavel_cpf ON cultura_espacos_culturais (responsavel_cpf)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_espacos_ativo ON cultura_espacos_culturais (ativo)")


def _create_projetos_culturais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_projetos_culturais (
            id UUID PRIMARY KEY,
            codigo_projeto VARCHAR(60) NOT NULL UNIQUE,
            titulo VARCHAR(255) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            natureza VARCHAR(40) NOT NULL,
            proponente_cpf_cnpj VARCHAR(32) NOT NULL,
            proponente_nome VARCHAR(200) NOT NULL,
            resumo TEXT NOT NULL,
            valor_solicitado NUMERIC(14, 2) NOT NULL,
            valor_aprovado NUMERIC(14, 2),
            data_submissao DATE NOT NULL,
            data_inicio DATE,
            data_fim DATE,
            status VARCHAR(40) NOT NULL,
            edital_id UUID,
            justificativa TEXT,
            objetivos JSONB NOT NULL DEFAULT '[]'::jsonb,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            observacoes TEXT,
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
                WHERE conname = 'ck_cultura_projetos_tipo'
                  AND conrelid = 'cultura_projetos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_projetos_culturais
                ADD CONSTRAINT ck_cultura_projetos_tipo
                CHECK (
                    tipo IN (
                        'producao',
                        'circulacao',
                        'formacao',
                        'preservacao',
                        'pesquisa',
                        'difusao',
                        'fomento'
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
                WHERE conname = 'ck_cultura_projetos_natureza'
                  AND conrelid = 'cultura_projetos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_projetos_culturais
                ADD CONSTRAINT ck_cultura_projetos_natureza
                CHECK (natureza IN ('artistica', 'cultural', 'educativa', 'social', 'tecnica'));
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
                WHERE conname = 'ck_cultura_projetos_status'
                  AND conrelid = 'cultura_projetos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_projetos_culturais
                ADD CONSTRAINT ck_cultura_projetos_status
                CHECK (
                    status IN (
                        'rascunho',
                        'submetido',
                        'em_analise',
                        'aprovado',
                        'reprovado',
                        'contratado',
                        'em_execucao',
                        'concluido',
                        'prestacao_contas',
                        'arquivado'
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
                WHERE conname = 'ck_cultura_projetos_integridade'
                  AND conrelid = 'cultura_projetos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_projetos_culturais
                ADD CONSTRAINT ck_cultura_projetos_integridade
                CHECK (
                    char_length(trim(titulo)) >= 5
                    AND char_length(trim(resumo)) >= 10
                    AND valor_solicitado > 0
                    AND (valor_aprovado IS NULL OR valor_aprovado > 0)
                    AND (
                        data_inicio IS NULL
                        OR data_fim IS NULL
                        OR data_fim >= data_inicio
                    )
                    AND jsonb_typeof(objetivos) = 'array'
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_codigo ON cultura_projetos_culturais (codigo_projeto)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_titulo ON cultura_projetos_culturais (titulo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_tipo ON cultura_projetos_culturais (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_natureza ON cultura_projetos_culturais (natureza)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_status ON cultura_projetos_culturais (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_proponente_cpf_cnpj ON cultura_projetos_culturais (proponente_cpf_cnpj)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_edital_id ON cultura_projetos_culturais (edital_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_data_submissao ON cultura_projetos_culturais (data_submissao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_projetos_ativo ON cultura_projetos_culturais (ativo)")


def _create_editais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_editais (
            id UUID PRIMARY KEY,
            numero VARCHAR(60) NOT NULL UNIQUE,
            titulo VARCHAR(255) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            orgao_responsavel_id UUID NOT NULL,
            valor_total NUMERIC(14, 2) NOT NULL,
            valor_disponivel NUMERIC(14, 2) NOT NULL,
            data_publicacao TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            data_inicio_inscricoes TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            data_fim_inscricoes TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            vagas INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            fase VARCHAR(40) NOT NULL,
            criterios JSONB NOT NULL DEFAULT '[]'::jsonb,
            documentos_necessarios JSONB NOT NULL DEFAULT '[]'::jsonb,
            inscricoes JSONB NOT NULL DEFAULT '[]'::jsonb,
            projetos_selecionados JSONB NOT NULL DEFAULT '[]'::jsonb,
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
                WHERE conname = 'ck_cultura_editais_tipo'
                  AND conrelid = 'cultura_editais'::regclass
            ) THEN
                ALTER TABLE cultura_editais
                ADD CONSTRAINT ck_cultura_editais_tipo
                CHECK (
                    tipo IN (
                        'fomento',
                        'premio',
                        'residencia',
                        'circulacao',
                        'producao',
                        'pesquisa',
                        'formacao'
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
                WHERE conname = 'ck_cultura_editais_fase'
                  AND conrelid = 'cultura_editais'::regclass
            ) THEN
                ALTER TABLE cultura_editais
                ADD CONSTRAINT ck_cultura_editais_fase
                CHECK (
                    fase IN (
                        'publicado',
                        'inscricoes_abertas',
                        'inscricoes_encerradas',
                        'em_analise',
                        'resultado_preliminar',
                        'prazo_recursos',
                        'resultado_final',
                        'contratacao',
                        'concluido'
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
                WHERE conname = 'ck_cultura_editais_integridade'
                  AND conrelid = 'cultura_editais'::regclass
            ) THEN
                ALTER TABLE cultura_editais
                ADD CONSTRAINT ck_cultura_editais_integridade
                CHECK (
                    char_length(trim(numero)) >= 3
                    AND char_length(trim(titulo)) >= 5
                    AND char_length(trim(descricao)) >= 10
                    AND valor_total > 0
                    AND valor_disponivel >= 0
                    AND valor_disponivel <= valor_total
                    AND vagas > 0
                    AND data_fim_inscricoes > data_inicio_inscricoes
                    AND jsonb_typeof(criterios) = 'array'
                    AND jsonb_typeof(documentos_necessarios) = 'array'
                    AND jsonb_typeof(inscricoes) = 'array'
                    AND jsonb_typeof(projetos_selecionados) = 'array'
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_editais_numero ON cultura_editais (numero)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_editais_titulo ON cultura_editais (titulo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_editais_tipo ON cultura_editais (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_editais_orgao_responsavel_id ON cultura_editais (orgao_responsavel_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_editais_fase ON cultura_editais (fase)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_editais_data_publicacao ON cultura_editais (data_publicacao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_editais_ativo ON cultura_editais (ativo)")


def upgrade() -> None:
    _create_espacos_culturais_table()
    _create_projetos_culturais_table()
    _create_editais_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_cultura_editais_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_editais_data_publicacao")
    op.execute("DROP INDEX IF EXISTS ix_cultura_editais_fase")
    op.execute("DROP INDEX IF EXISTS ix_cultura_editais_orgao_responsavel_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_editais_tipo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_editais_titulo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_editais_numero")
    op.execute("DROP TABLE IF EXISTS cultura_editais")

    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_data_submissao")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_edital_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_proponente_cpf_cnpj")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_status")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_natureza")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_tipo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_titulo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_projetos_codigo")
    op.execute("DROP TABLE IF EXISTS cultura_projetos_culturais")

    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_responsavel_cpf")
    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_administracao")
    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_provincia")
    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_municipio")
    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_tipo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_nome")
    op.execute("DROP INDEX IF EXISTS ix_cultura_espacos_codigo")
    op.execute("DROP TABLE IF EXISTS cultura_espacos_culturais")
