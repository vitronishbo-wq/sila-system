"""add seguranca_publica vestigios e evidencias

Revision ID: 20260302_029_seguranca_publica_vestigios_evidencias
Revises: 20260302_028_seguranca_publica_cadeia_custodia_laudos
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_029_seguranca_publica_vestigios_evidencias"
down_revision = "20260302_028_seguranca_publica_cadeia_custodia_laudos"
branch_labels = None
depends_on = None


def _create_vestigios_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_vestigios (
            id UUID PRIMARY KEY,
            codigo_vestigio VARCHAR(50) NOT NULL UNIQUE,
            cadeia_custodia_id UUID NOT NULL,
            ocorrencia_id UUID NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            descricao TEXT NOT NULL,
            localizacao VARCHAR(255) NOT NULL,
            data_coleta TIMESTAMP NOT NULL,
            status VARCHAR(30) NOT NULL,
            coletado_por_id UUID,
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
                WHERE conname = 'ck_seguranca_vestigios_campos_basicos'
                  AND conrelid = 'seguranca_vestigios'::regclass
            ) THEN
                ALTER TABLE seguranca_vestigios
                ADD CONSTRAINT ck_seguranca_vestigios_campos_basicos
                CHECK (
                    char_length(trim(codigo_vestigio)) >= 8
                    AND char_length(trim(descricao)) >= 5
                    AND char_length(trim(localizacao)) >= 3
                    AND data_coleta <= CURRENT_TIMESTAMP
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
                WHERE conname = 'ck_seguranca_vestigios_tipo_status'
                  AND conrelid = 'seguranca_vestigios'::regclass
            ) THEN
                ALTER TABLE seguranca_vestigios
                ADD CONSTRAINT ck_seguranca_vestigios_tipo_status
                CHECK (
                    tipo IN (
                        'material_biologico',
                        'impressao_digital',
                        'residuo_balistico',
                        'documento',
                        'midia_digital',
                        'objeto',
                        'outro'
                    )
                    AND status IN ('coletado', 'em_analise', 'preservado', 'descartado')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_codigo ON seguranca_vestigios (codigo_vestigio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_cadeia_id ON seguranca_vestigios (cadeia_custodia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_ocorrencia_id ON seguranca_vestigios (ocorrencia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_tipo ON seguranca_vestigios (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_status ON seguranca_vestigios (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_data_coleta ON seguranca_vestigios (data_coleta)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_localizacao ON seguranca_vestigios (localizacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_coletado_por ON seguranca_vestigios (coletado_por_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_vestigios_ativo ON seguranca_vestigios (ativo)"
    )


def _create_evidencias_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_evidencias (
            id UUID PRIMARY KEY,
            codigo_evidencia VARCHAR(50) NOT NULL UNIQUE,
            vestigio_id UUID NOT NULL,
            cadeia_custodia_id UUID NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            descricao TEXT NOT NULL,
            fonte VARCHAR(255) NOT NULL,
            confiabilidade INTEGER NOT NULL DEFAULT 3,
            status VARCHAR(30) NOT NULL,
            data_registro DATE NOT NULL,
            analisado_por_id UUID,
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
                WHERE conname = 'ck_seguranca_evidencias_campos_basicos'
                  AND conrelid = 'seguranca_evidencias'::regclass
            ) THEN
                ALTER TABLE seguranca_evidencias
                ADD CONSTRAINT ck_seguranca_evidencias_campos_basicos
                CHECK (
                    char_length(trim(codigo_evidencia)) >= 8
                    AND char_length(trim(descricao)) >= 5
                    AND char_length(trim(fonte)) >= 3
                    AND confiabilidade BETWEEN 1 AND 5
                    AND data_registro <= CURRENT_DATE
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
                WHERE conname = 'ck_seguranca_evidencias_tipo_status'
                  AND conrelid = 'seguranca_evidencias'::regclass
            ) THEN
                ALTER TABLE seguranca_evidencias
                ADD CONSTRAINT ck_seguranca_evidencias_tipo_status
                CHECK (
                    tipo IN ('fisica', 'documental', 'digital', 'testemunhal', 'pericial')
                    AND status IN ('registrada', 'em_validacao', 'validada', 'inutilizada')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_codigo ON seguranca_evidencias (codigo_evidencia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_vestigio_id ON seguranca_evidencias (vestigio_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_cadeia_id ON seguranca_evidencias (cadeia_custodia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_tipo ON seguranca_evidencias (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_status ON seguranca_evidencias (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_data_registro ON seguranca_evidencias (data_registro)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_fonte ON seguranca_evidencias (fonte)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_analisado_por ON seguranca_evidencias (analisado_por_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_evidencias_ativo ON seguranca_evidencias (ativo)"
    )


def upgrade() -> None:
    _create_vestigios_table()
    _create_evidencias_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_analisado_por")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_fonte")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_data_registro")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_cadeia_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_vestigio_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_evidencias_codigo")
    op.execute("DROP TABLE IF EXISTS seguranca_evidencias")

    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_coletado_por")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_localizacao")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_data_coleta")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_ocorrencia_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_cadeia_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_vestigios_codigo")
    op.execute("DROP TABLE IF EXISTS seguranca_vestigios")
