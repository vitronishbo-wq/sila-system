"""create comercio_externo_radar and comercio_externo_habilitacoes_radar tables

Revision ID: 20260301_006_comex_radar
Revises: 20260301_005_comex_habilitacoes
Create Date: 2026-03-01 19:00:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260301_006_comex_radar"
down_revision = "20260301_005_comex_habilitacoes"
branch_labels = None
depends_on = None


def _create_radar_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS comercio_externo_radar (
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
                WHERE conname = 'ck_comex_radar_status'
                  AND conrelid = 'comercio_externo_radar'::regclass
            ) THEN
                ALTER TABLE comercio_externo_radar
                ADD CONSTRAINT ck_comex_radar_status
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
                WHERE conname = 'ck_comex_radar_tipo_pessoa'
                  AND conrelid = 'comercio_externo_radar'::regclass
            ) THEN
                ALTER TABLE comercio_externo_radar
                ADD CONSTRAINT ck_comex_radar_tipo_pessoa
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
                WHERE conname = 'ck_comex_radar_tipo_operador'
                  AND conrelid = 'comercio_externo_radar'::regclass
            ) THEN
                ALTER TABLE comercio_externo_radar
                ADD CONSTRAINT ck_comex_radar_tipo_operador
                CHECK (tipo_operador = 'exportador_importador');
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_comercio_externo_radar_cnpj_cpf ON comercio_externo_radar (cnpj_cpf)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_comercio_externo_radar_status ON comercio_externo_radar (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_comercio_externo_radar_municipio ON comercio_externo_radar (municipio)"
    )


def _create_habilitacao_radar_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS comercio_externo_habilitacoes_radar (
            id UUID PRIMARY KEY,
            tipo_operador VARCHAR(32) NOT NULL,
            tipo_pessoa VARCHAR(16) NOT NULL,
            status VARCHAR(24) NOT NULL,
            razao_social VARCHAR(255) NOT NULL,
            cnpj_cpf VARCHAR(32) NOT NULL,
            numero_processo VARCHAR(64) NOT NULL UNIQUE,
            data_solicitacao DATE NOT NULL,
            data_analise DATE,
            data_validade DATE,
            numero_radar VARCHAR(64),
            motivo TEXT,
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
                WHERE conname = 'ck_comex_habilitacoes_radar_status'
                  AND conrelid = 'comercio_externo_habilitacoes_radar'::regclass
            ) THEN
                ALTER TABLE comercio_externo_habilitacoes_radar
                ADD CONSTRAINT ck_comex_habilitacoes_radar_status
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
                WHERE conname = 'ck_comex_habilitacoes_radar_tipo_pessoa'
                  AND conrelid = 'comercio_externo_habilitacoes_radar'::regclass
            ) THEN
                ALTER TABLE comercio_externo_habilitacoes_radar
                ADD CONSTRAINT ck_comex_habilitacoes_radar_tipo_pessoa
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
                WHERE conname = 'ck_comex_habilitacoes_radar_tipo_operador'
                  AND conrelid = 'comercio_externo_habilitacoes_radar'::regclass
            ) THEN
                ALTER TABLE comercio_externo_habilitacoes_radar
                ADD CONSTRAINT ck_comex_habilitacoes_radar_tipo_operador
                CHECK (tipo_operador = 'exportador_importador');
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_comercio_externo_habilitacoes_radar_numero_processo
        ON comercio_externo_habilitacoes_radar (numero_processo)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_comercio_externo_habilitacoes_radar_status
        ON comercio_externo_habilitacoes_radar (status)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_comercio_externo_habilitacoes_radar_cnpj_cpf
        ON comercio_externo_habilitacoes_radar (cnpj_cpf)
        """
    )


def upgrade():
    _create_radar_table()
    _create_habilitacao_radar_table()


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_habilitacoes_radar_cnpj_cpf")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_habilitacoes_radar_status")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_habilitacoes_radar_numero_processo")
    op.execute("DROP TABLE IF EXISTS comercio_externo_habilitacoes_radar")

    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_radar_municipio")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_radar_status")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_radar_cnpj_cpf")
    op.execute("DROP TABLE IF EXISTS comercio_externo_radar")
