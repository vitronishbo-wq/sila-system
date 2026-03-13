"""create cultura slice2 tables for grupos e patrimonio imaterial

Revision ID: 20260302_018_cultura_slice2_grupos_patrimonio_imaterial
Revises: 20260302_017_cultura_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260302_018_cultura_slice2_grupos_patrimonio_imaterial"
down_revision = "20260302_017_cultura_foundation"
branch_labels = None
depends_on = None


def _create_grupos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_grupos_artisticos (
            id UUID PRIMARY KEY,
            codigo_grupo VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            lider_artista_id UUID NOT NULL,
            descricao TEXT,
            data_fundacao DATE,
            municipio VARCHAR(100),
            provincia VARCHAR(100),
            instituicao_educacional_id UUID,
            membros_ids TEXT[],
            data_cadastro DATE NOT NULL,
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
                WHERE conname = 'ck_cultura_grupos_tipo'
                  AND conrelid = 'cultura_grupos_artisticos'::regclass
            ) THEN
                ALTER TABLE cultura_grupos_artisticos
                ADD CONSTRAINT ck_cultura_grupos_tipo
                CHECK (tipo IN ('banda', 'companhia', 'coletivo', 'coral', 'orquestra'));
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
                WHERE conname = 'ck_cultura_grupos_nome_fundacao'
                  AND conrelid = 'cultura_grupos_artisticos'::regclass
            ) THEN
                ALTER TABLE cultura_grupos_artisticos
                ADD CONSTRAINT ck_cultura_grupos_nome_fundacao
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND (data_fundacao IS NULL OR data_fundacao <= CURRENT_DATE)
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_grupos_codigo ON cultura_grupos_artisticos (codigo_grupo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_grupos_nome ON cultura_grupos_artisticos (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_grupos_tipo ON cultura_grupos_artisticos (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_grupos_lider_artista_id ON cultura_grupos_artisticos (lider_artista_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_grupos_municipio ON cultura_grupos_artisticos (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_grupos_provincia ON cultura_grupos_artisticos (provincia)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_grupos_instituicao_educacional_id ON cultura_grupos_artisticos (instituicao_educacional_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_grupos_ativo ON cultura_grupos_artisticos (ativo)")


def _create_patrimonios_imateriais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_patrimonios_imateriais (
            id UUID PRIMARY KEY,
            registro_pni VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            categoria VARCHAR(40) NOT NULL,
            descricao TEXT NOT NULL,
            comunidade VARCHAR(200) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            status VARCHAR(30) NOT NULL,
            atracao_turistica_id UUID,
            instituicao_educacional_id UUID,
            plano_salvaguarda TEXT,
            data_registro DATE NOT NULL,
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
                WHERE conname = 'ck_cultura_pim_categoria'
                  AND conrelid = 'cultura_patrimonios_imateriais'::regclass
            ) THEN
                ALTER TABLE cultura_patrimonios_imateriais
                ADD CONSTRAINT ck_cultura_pim_categoria
                CHECK (
                    categoria IN (
                        'festa_popular',
                        'ritual',
                        'tradicao',
                        'saber_tradicional',
                        'expressao_oral',
                        'musica_tradicional',
                        'danca_tradicional'
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
                WHERE conname = 'ck_cultura_pim_status'
                  AND conrelid = 'cultura_patrimonios_imateriais'::regclass
            ) THEN
                ALTER TABLE cultura_patrimonios_imateriais
                ADD CONSTRAINT ck_cultura_pim_status
                CHECK (status IN ('proposto', 'em_analise', 'registrado', 'suspenso'));
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
                WHERE conname = 'ck_cultura_pim_nome_descricao'
                  AND conrelid = 'cultura_patrimonios_imateriais'::regclass
            ) THEN
                ALTER TABLE cultura_patrimonios_imateriais
                ADD CONSTRAINT ck_cultura_pim_nome_descricao
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND char_length(trim(descricao)) >= 10
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_pim_registro ON cultura_patrimonios_imateriais (registro_pni)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_pim_nome ON cultura_patrimonios_imateriais (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_pim_categoria ON cultura_patrimonios_imateriais (categoria)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_pim_status ON cultura_patrimonios_imateriais (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_pim_municipio ON cultura_patrimonios_imateriais (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_pim_provincia ON cultura_patrimonios_imateriais (provincia)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_pim_atracao_turistica_id ON cultura_patrimonios_imateriais (atracao_turistica_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_pim_instituicao_educacional_id ON cultura_patrimonios_imateriais (instituicao_educacional_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_pim_ativo ON cultura_patrimonios_imateriais (ativo)")


def upgrade() -> None:
    _create_grupos_table()
    _create_patrimonios_imateriais_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_instituicao_educacional_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_atracao_turistica_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_provincia")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_municipio")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_status")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_categoria")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_nome")
    op.execute("DROP INDEX IF EXISTS ix_cultura_pim_registro")
    op.execute("DROP TABLE IF EXISTS cultura_patrimonios_imateriais")

    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_instituicao_educacional_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_provincia")
    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_municipio")
    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_lider_artista_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_tipo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_nome")
    op.execute("DROP INDEX IF EXISTS ix_cultura_grupos_codigo")
    op.execute("DROP TABLE IF EXISTS cultura_grupos_artisticos")
