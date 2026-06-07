"""create comercio_externo_transportadores_internacionais table

Revision ID: 20260301_004_comex_transportadores_internacionais
Revises: 20260301_003_comex_operadores_logisticos
Create Date: 2026-03-01 17:10:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260301_004_comex_transportadores_internacionais"
down_revision = "20260301_003_comex_operadores_logisticos"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS comercio_externo_transportadores_internacionais (
            id UUID PRIMARY KEY,
            cadastro_radar VARCHAR(64) NOT NULL DEFAULT '',
            tipo_operador VARCHAR(32) NOT NULL,
            tipo_pessoa VARCHAR(16) NOT NULL,
            status VARCHAR(24) NOT NULL,
            razao_social VARCHAR(255) NOT NULL,
            nome_fantasia VARCHAR(255),
            cnpj_cpf VARCHAR(32) NOT NULL UNIQUE,
            endereco TEXT NOT NULL,
            numero VARCHAR(32) NOT NULL,
            complemento VARCHAR(128),
            bairro VARCHAR(128) NOT NULL,
            municipio VARCHAR(128) NOT NULL,
            provincia VARCHAR(128) NOT NULL,
            cep VARCHAR(16) NOT NULL,
            pais VARCHAR(2) NOT NULL DEFAULT 'AO',
            telefone VARCHAR(32),
            email VARCHAR(255),
            site VARCHAR(255),
            numero_licenca VARCHAR(64),
            orgao_anuente VARCHAR(255),
            data_habilitacao DATE,
            data_validade DATE,
            data_suspensao DATE,
            data_cancelamento DATE,
            motivo_cancelamento TEXT,
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
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'ck_comex_transportadores_internacionais_status'
                  AND conrelid = 'comercio_externo_transportadores_internacionais'::regclass
            ) THEN
                ALTER TABLE comercio_externo_transportadores_internacionais
                ADD CONSTRAINT ck_comex_transportadores_internacionais_status
                CHECK (status IN ('pendente', 'habilitado', 'suspenso', 'cancelado', 'bloqueado'));
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'ck_comex_transportadores_internacionais_tipo_pessoa'
                  AND conrelid = 'comercio_externo_transportadores_internacionais'::regclass
            ) THEN
                ALTER TABLE comercio_externo_transportadores_internacionais
                ADD CONSTRAINT ck_comex_transportadores_internacionais_tipo_pessoa
                CHECK (tipo_pessoa IN ('fisica', 'juridica'));
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'ck_comex_transportadores_internacionais_tipo_operador'
                  AND conrelid = 'comercio_externo_transportadores_internacionais'::regclass
            ) THEN
                ALTER TABLE comercio_externo_transportadores_internacionais
                ADD CONSTRAINT ck_comex_transportadores_internacionais_tipo_operador
                CHECK (tipo_operador = 'transportador');
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_comercio_externo_transportadores_internacionais_cnpj_cpf
        ON comercio_externo_transportadores_internacionais (cnpj_cpf)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_comercio_externo_transportadores_internacionais_status
        ON comercio_externo_transportadores_internacionais (status)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_comercio_externo_transportadores_internacionais_municipio
        ON comercio_externo_transportadores_internacionais (municipio)
        """
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_transportadores_internacionais_municipio")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_transportadores_internacionais_status")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_transportadores_internacionais_cnpj_cpf")
    op.execute("DROP TABLE IF EXISTS comercio_externo_transportadores_internacionais")
