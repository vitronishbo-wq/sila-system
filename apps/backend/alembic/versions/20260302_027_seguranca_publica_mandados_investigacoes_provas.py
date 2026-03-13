"""add seguranca_publica mandados investigacoes provas periciais

Revision ID: 20260302_027_seguranca_publica_mandados_investigacoes_provas
Revises: 20260302_026_seguranca_publica_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260302_027_seguranca_publica_mandados_investigacoes_provas"
down_revision = "20260302_026_seguranca_publica_foundation"
branch_labels = None
depends_on = None


def _create_mandados_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_mandados (
            id UUID PRIMARY KEY,
            numero_mandado VARCHAR(50) NOT NULL UNIQUE,
            ocorrencia_id UUID NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            autoridade_judicial VARCHAR(150) NOT NULL,
            data_expedicao DATE NOT NULL,
            data_validade DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            unidade_id UUID,
            policial_responsavel_id UUID,
            observacoes TEXT,
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
                WHERE conname = 'ck_seguranca_mandados_campos_basicos'
                  AND conrelid = 'seguranca_mandados'::regclass
            ) THEN
                ALTER TABLE seguranca_mandados
                ADD CONSTRAINT ck_seguranca_mandados_campos_basicos
                CHECK (
                    char_length(trim(numero_mandado)) >= 8
                    AND char_length(trim(autoridade_judicial)) >= 3
                    AND data_validade >= data_expedicao
                    AND data_expedicao <= CURRENT_DATE
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
                WHERE conname = 'ck_seguranca_mandados_enum_values'
                  AND conrelid = 'seguranca_mandados'::regclass
            ) THEN
                ALTER TABLE seguranca_mandados
                ADD CONSTRAINT ck_seguranca_mandados_enum_values
                CHECK (
                    tipo IN (
                        'prisao',
                        'busca_apreensao',
                        'apreensao',
                        'conducao_coercitiva',
                        'internacao'
                    )
                    AND status IN ('expedido', 'cumprido', 'pendente', 'cancelado', 'vencido')
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_numero ON seguranca_mandados (numero_mandado)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_ocorrencia_id ON seguranca_mandados (ocorrencia_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_tipo ON seguranca_mandados (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_status ON seguranca_mandados (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_data_expedicao ON seguranca_mandados (data_expedicao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_data_validade ON seguranca_mandados (data_validade)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_unidade_id ON seguranca_mandados (unidade_id)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_policial_responsavel ON seguranca_mandados (policial_responsavel_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_mandados_ativo ON seguranca_mandados (ativo)")


def _create_investigacoes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_investigacoes (
            id UUID PRIMARY KEY,
            codigo_investigacao VARCHAR(50) NOT NULL UNIQUE,
            ocorrencia_id UUID NOT NULL,
            unidade_id UUID NOT NULL,
            data_abertura DATE NOT NULL,
            status VARCHAR(40) NOT NULL,
            delegado_responsavel_id UUID,
            data_conclusao DATE,
            resumo TEXT,
            observacoes TEXT,
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
                WHERE conname = 'ck_seguranca_investigacoes_campos_basicos'
                  AND conrelid = 'seguranca_investigacoes'::regclass
            ) THEN
                ALTER TABLE seguranca_investigacoes
                ADD CONSTRAINT ck_seguranca_investigacoes_campos_basicos
                CHECK (
                    char_length(trim(codigo_investigacao)) >= 8
                    AND data_abertura <= CURRENT_DATE
                    AND (data_conclusao IS NULL OR data_conclusao >= data_abertura)
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
                WHERE conname = 'ck_seguranca_investigacoes_status'
                  AND conrelid = 'seguranca_investigacoes'::regclass
            ) THEN
                ALTER TABLE seguranca_investigacoes
                ADD CONSTRAINT ck_seguranca_investigacoes_status
                CHECK (
                    status IN (
                        'aberta',
                        'em_andamento',
                        'concluida',
                        'arquivada',
                        'remetida_justica'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_codigo ON seguranca_investigacoes (codigo_investigacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_ocorrencia_id ON seguranca_investigacoes (ocorrencia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_unidade_id ON seguranca_investigacoes (unidade_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_status ON seguranca_investigacoes (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_data_abertura ON seguranca_investigacoes (data_abertura)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_data_conclusao ON seguranca_investigacoes (data_conclusao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_delegado_id ON seguranca_investigacoes (delegado_responsavel_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_investigacoes_ativo ON seguranca_investigacoes (ativo)")


def _create_provas_periciais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_provas_periciais (
            id UUID PRIMARY KEY,
            codigo_prova VARCHAR(50) NOT NULL UNIQUE,
            ocorrencia_id UUID NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            descricao TEXT NOT NULL,
            data_coleta DATE NOT NULL,
            local_coleta VARCHAR(255) NOT NULL,
            status VARCHAR(30) NOT NULL,
            coletado_por_id UUID,
            cadeia_custodia_id UUID,
            observacoes TEXT,
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
                WHERE conname = 'ck_seguranca_provas_periciais_campos_basicos'
                  AND conrelid = 'seguranca_provas_periciais'::regclass
            ) THEN
                ALTER TABLE seguranca_provas_periciais
                ADD CONSTRAINT ck_seguranca_provas_periciais_campos_basicos
                CHECK (
                    char_length(trim(codigo_prova)) >= 8
                    AND char_length(trim(descricao)) >= 5
                    AND char_length(trim(local_coleta)) >= 3
                    AND data_coleta <= CURRENT_DATE
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
                WHERE conname = 'ck_seguranca_provas_periciais_enum_values'
                  AND conrelid = 'seguranca_provas_periciais'::regclass
            ) THEN
                ALTER TABLE seguranca_provas_periciais
                ADD CONSTRAINT ck_seguranca_provas_periciais_enum_values
                CHECK (
                    tipo IN (
                        'documental',
                        'testemunhal',
                        'material',
                        'digital',
                        'audiovisual',
                        'biologica',
                        'balistica'
                    )
                    AND status IN ('coletada', 'em_analise', 'validada', 'descartada')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_codigo ON seguranca_provas_periciais (codigo_prova)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_ocorrencia_id ON seguranca_provas_periciais (ocorrencia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_tipo ON seguranca_provas_periciais (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_status ON seguranca_provas_periciais (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_data_coleta ON seguranca_provas_periciais (data_coleta)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_local_coleta ON seguranca_provas_periciais (local_coleta)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_coletado_por ON seguranca_provas_periciais (coletado_por_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_cadeia_custodia ON seguranca_provas_periciais (cadeia_custodia_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_provas_periciais_ativo ON seguranca_provas_periciais (ativo)")


def upgrade() -> None:
    _create_mandados_table()
    _create_investigacoes_table()
    _create_provas_periciais_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_cadeia_custodia")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_coletado_por")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_local_coleta")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_data_coleta")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_ocorrencia_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_provas_periciais_codigo")
    op.execute("DROP TABLE IF EXISTS seguranca_provas_periciais")

    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_delegado_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_data_conclusao")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_data_abertura")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_ocorrencia_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_investigacoes_codigo")
    op.execute("DROP TABLE IF EXISTS seguranca_investigacoes")

    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_policial_responsavel")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_data_validade")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_data_expedicao")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_ocorrencia_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_mandados_numero")
    op.execute("DROP TABLE IF EXISTS seguranca_mandados")
