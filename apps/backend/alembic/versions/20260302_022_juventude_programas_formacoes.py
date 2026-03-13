"""create juventude programas e formacoes tables

Revision ID: 20260302_022_juventude_programas_formacoes
Revises: 20260302_021_juventude_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260302_022_juventude_programas_formacoes"
down_revision = "20260302_021_juventude_foundation"
branch_labels = None
depends_on = None


def _create_programas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_programas (
            id UUID PRIMARY KEY,
            codigo_programa VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            vagas INTEGER,
            municipio VARCHAR(100),
            provincia VARCHAR(100),
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
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_juventude_programas_nome_periodo_vagas'
                  AND conrelid = 'juventude_programas'::regclass
            ) THEN
                ALTER TABLE juventude_programas
                ADD CONSTRAINT ck_juventude_programas_nome_periodo_vagas
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND (data_fim IS NULL OR data_fim >= data_inicio)
                    AND (vagas IS NULL OR vagas > 0)
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
                WHERE conname = 'ck_juventude_programas_tipo_status'
                  AND conrelid = 'juventude_programas'::regclass
            ) THEN
                ALTER TABLE juventude_programas
                ADD CONSTRAINT ck_juventude_programas_tipo_status
                CHECK (
                    tipo IN (
                        'aprendizagem',
                        'estagio',
                        'primeiro_emprego',
                        'empreendedorismo',
                        'intercambio',
                        'voluntariado',
                        'capacitacao',
                        'lideranca'
                    )
                    AND status IN (
                        'planeado',
                        'inscricoes_abertas',
                        'ativo',
                        'concluido',
                        'cancelado'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_programas_codigo_programa ON juventude_programas (codigo_programa)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_programas_nome ON juventude_programas (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_programas_tipo ON juventude_programas (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_programas_status ON juventude_programas (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_programas_municipio ON juventude_programas (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_programas_provincia ON juventude_programas (provincia)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_programas_ativo ON juventude_programas (ativo)")


def _create_formacoes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_formacoes (
            id UUID PRIMARY KEY,
            codigo_formacao VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            programa_id UUID,
            nome_curso VARCHAR(200) NOT NULL,
            instituicao VARCHAR(200) NOT NULL,
            carga_horaria INTEGER NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            certificado_emitido BOOLEAN NOT NULL DEFAULT FALSE,
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
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_juventude_formacoes_curso_duracao'
                  AND conrelid = 'juventude_formacoes'::regclass
            ) THEN
                ALTER TABLE juventude_formacoes
                ADD CONSTRAINT ck_juventude_formacoes_curso_duracao
                CHECK (
                    char_length(trim(nome_curso)) >= 3
                    AND char_length(trim(instituicao)) >= 3
                    AND carga_horaria > 0
                    AND (data_fim IS NULL OR data_fim >= data_inicio)
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
                WHERE conname = 'ck_juventude_formacoes_status'
                  AND conrelid = 'juventude_formacoes'::regclass
            ) THEN
                ALTER TABLE juventude_formacoes
                ADD CONSTRAINT ck_juventude_formacoes_status
                CHECK (
                    status IN (
                        'inscrito',
                        'em_andamento',
                        'concluida',
                        'reprovada',
                        'cancelada'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_formacoes_codigo_formacao ON juventude_formacoes (codigo_formacao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_formacoes_jovem_id ON juventude_formacoes (jovem_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_formacoes_programa_id ON juventude_formacoes (programa_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_formacoes_nome_curso ON juventude_formacoes (nome_curso)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_formacoes_status ON juventude_formacoes (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_formacoes_ativo ON juventude_formacoes (ativo)")


def upgrade() -> None:
    _create_programas_table()
    _create_formacoes_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_juventude_formacoes_ativo")
    op.execute("DROP INDEX IF EXISTS ix_juventude_formacoes_status")
    op.execute("DROP INDEX IF EXISTS ix_juventude_formacoes_nome_curso")
    op.execute("DROP INDEX IF EXISTS ix_juventude_formacoes_programa_id")
    op.execute("DROP INDEX IF EXISTS ix_juventude_formacoes_jovem_id")
    op.execute("DROP INDEX IF EXISTS ix_juventude_formacoes_codigo_formacao")
    op.execute("DROP TABLE IF EXISTS juventude_formacoes")

    op.execute("DROP INDEX IF EXISTS ix_juventude_programas_ativo")
    op.execute("DROP INDEX IF EXISTS ix_juventude_programas_provincia")
    op.execute("DROP INDEX IF EXISTS ix_juventude_programas_municipio")
    op.execute("DROP INDEX IF EXISTS ix_juventude_programas_status")
    op.execute("DROP INDEX IF EXISTS ix_juventude_programas_tipo")
    op.execute("DROP INDEX IF EXISTS ix_juventude_programas_nome")
    op.execute("DROP INDEX IF EXISTS ix_juventude_programas_codigo_programa")
    op.execute("DROP TABLE IF EXISTS juventude_programas")
