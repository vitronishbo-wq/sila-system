"""add seguranca_publica cadeia custodia and laudos periciais

Revision ID: 20260302_028_seguranca_publica_cadeia_custodia_laudos
Revises: 20260302_027_seguranca_publica_mandados_investigacoes_provas
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_028_seguranca_publica_cadeia_custodia_laudos"
down_revision = "20260302_027_seguranca_publica_mandados_investigacoes_provas"
branch_labels = None
depends_on = None


def _create_cadeia_custodia_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_cadeias_custodia (
            id UUID PRIMARY KEY,
            codigo_cadeia VARCHAR(50) NOT NULL UNIQUE,
            prova_id UUID NOT NULL UNIQUE,
            ocorrencia_id UUID NOT NULL,
            status VARCHAR(30) NOT NULL,
            local_atual VARCHAR(255) NOT NULL,
            responsavel_id UUID NOT NULL,
            data_inicio TIMESTAMP NOT NULL,
            data_ultima_movimentacao TIMESTAMP NOT NULL,
            historico_movimentacoes JSONB NOT NULL DEFAULT '[]'::jsonb,
            integridade_verificada BOOLEAN NOT NULL DEFAULT TRUE,
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
                WHERE conname = 'ck_seguranca_cadeias_campos_basicos'
                  AND conrelid = 'seguranca_cadeias_custodia'::regclass
            ) THEN
                ALTER TABLE seguranca_cadeias_custodia
                ADD CONSTRAINT ck_seguranca_cadeias_campos_basicos
                CHECK (
                    char_length(trim(codigo_cadeia)) >= 8
                    AND char_length(trim(local_atual)) >= 3
                    AND data_ultima_movimentacao >= data_inicio
                    AND jsonb_typeof(historico_movimentacoes::jsonb) = 'array'
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
                WHERE conname = 'ck_seguranca_cadeias_status'
                  AND conrelid = 'seguranca_cadeias_custodia'::regclass
            ) THEN
                ALTER TABLE seguranca_cadeias_custodia
                ADD CONSTRAINT ck_seguranca_cadeias_status
                CHECK (
                    status IN ('iniciada', 'em_transito', 'armazenada', 'encerrada', 'rompida')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_codigo ON seguranca_cadeias_custodia (codigo_cadeia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_prova_id ON seguranca_cadeias_custodia (prova_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_ocorrencia_id ON seguranca_cadeias_custodia (ocorrencia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_status ON seguranca_cadeias_custodia (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_local_atual ON seguranca_cadeias_custodia (local_atual)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_responsavel_id ON seguranca_cadeias_custodia (responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_data_inicio ON seguranca_cadeias_custodia (data_inicio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_data_ultima_mov ON seguranca_cadeias_custodia (data_ultima_movimentacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_cadeias_ativo ON seguranca_cadeias_custodia (ativo)"
    )


def _create_laudos_periciais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_laudos_periciais (
            id UUID PRIMARY KEY,
            numero_laudo VARCHAR(50) NOT NULL UNIQUE,
            prova_id UUID NOT NULL,
            tipo_laudo VARCHAR(30) NOT NULL,
            perito_id UUID NOT NULL,
            data_emissao DATE NOT NULL,
            conclusao TEXT NOT NULL,
            status VARCHAR(30) NOT NULL,
            resumo TEXT,
            arquivo_url VARCHAR(500),
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
                WHERE conname = 'ck_seguranca_laudos_campos_basicos'
                  AND conrelid = 'seguranca_laudos_periciais'::regclass
            ) THEN
                ALTER TABLE seguranca_laudos_periciais
                ADD CONSTRAINT ck_seguranca_laudos_campos_basicos
                CHECK (
                    char_length(trim(numero_laudo)) >= 8
                    AND char_length(trim(conclusao)) >= 10
                    AND data_emissao <= CURRENT_DATE
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
                WHERE conname = 'ck_seguranca_laudos_tipo_status'
                  AND conrelid = 'seguranca_laudos_periciais'::regclass
            ) THEN
                ALTER TABLE seguranca_laudos_periciais
                ADD CONSTRAINT ck_seguranca_laudos_tipo_status
                CHECK (
                    tipo_laudo IN (
                        'criminalistico',
                        'balistico',
                        'toxicologico',
                        'dna',
                        'papiloscopico',
                        'documentoscopico',
                        'informatica',
                        'medico_legal'
                    )
                    AND status IN ('em_elaboracao', 'emitido', 'retificado', 'cancelado')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_laudos_numero ON seguranca_laudos_periciais (numero_laudo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_laudos_prova_id ON seguranca_laudos_periciais (prova_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_laudos_tipo ON seguranca_laudos_periciais (tipo_laudo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_laudos_perito_id ON seguranca_laudos_periciais (perito_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_laudos_data_emissao ON seguranca_laudos_periciais (data_emissao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_laudos_status ON seguranca_laudos_periciais (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_laudos_ativo ON seguranca_laudos_periciais (ativo)"
    )


def upgrade() -> None:
    _create_cadeia_custodia_table()
    _create_laudos_periciais_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_seguranca_laudos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_laudos_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_laudos_data_emissao")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_laudos_perito_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_laudos_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_laudos_prova_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_laudos_numero")
    op.execute("DROP TABLE IF EXISTS seguranca_laudos_periciais")

    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_data_ultima_mov")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_data_inicio")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_responsavel_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_local_atual")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_ocorrencia_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_prova_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_cadeias_codigo")
    op.execute("DROP TABLE IF EXISTS seguranca_cadeias_custodia")
