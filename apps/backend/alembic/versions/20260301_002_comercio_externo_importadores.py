"""create comercio_externo_importadores table

Revision ID: 20260301_002_comex_importadores
Revises: 20260301_001_comex_exportadores
Create Date: 2026-03-01 14:15:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260301_002_comex_importadores"
down_revision = "20260301_001_comex_exportadores"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS comercio_externo_importadores (
            id UUID PRIMARY KEY,
            cadastro_radar VARCHAR(64) NOT NULL DEFAULT '',
            tipo_operador VARCHAR(32) NOT NULL,
            tipo_pessoa VARCHAR(16) NOT NULL,
            status VARCHAR(24) NOT NULL,
            razao_social VARCHAR(255) NOT NULL,
            nome_fantasia VARCHAR(255),
            cnpj_cpf VARCHAR(32) NOT NULL UNIQUE,
            inscricao_estadual VARCHAR(32),
            inscricao_municipal VARCHAR(32),
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
            representante_nome VARCHAR(255),
            representante_cpf VARCHAR(32),
            representante_cargo VARCHAR(128),
            responsavel_nome VARCHAR(255),
            responsavel_cpf VARCHAR(32),
            responsavel_registro VARCHAR(64),
            data_habilitacao DATE,
            data_validade DATE,
            data_suspensao DATE,
            data_cancelamento DATE,
            motivo_cancelamento TEXT,
            regimes_autorizados JSONB NOT NULL DEFAULT '[]'::jsonb,
            produtos_principais JSONB,
            paises_origem JSONB,
            banco_principal VARCHAR(255),
            conta_corrente VARCHAR(64),
            swift_code VARCHAR(32),
            limite_credito NUMERIC(18, 2),
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
                WHERE conname = 'ck_comex_importadores_status'
                  AND conrelid = 'comercio_externo_importadores'::regclass
            ) THEN
                ALTER TABLE comercio_externo_importadores
                ADD CONSTRAINT ck_comex_importadores_status
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
                WHERE conname = 'ck_comex_importadores_tipo_pessoa'
                  AND conrelid = 'comercio_externo_importadores'::regclass
            ) THEN
                ALTER TABLE comercio_externo_importadores
                ADD CONSTRAINT ck_comex_importadores_tipo_pessoa
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
                WHERE conname = 'ck_comex_importadores_tipo_operador'
                  AND conrelid = 'comercio_externo_importadores'::regclass
            ) THEN
                ALTER TABLE comercio_externo_importadores
                ADD CONSTRAINT ck_comex_importadores_tipo_operador
                CHECK (
                    tipo_operador IN (
                        'exportador',
                        'importador',
                        'exportador_importador',
                        'despachante',
                        'agente_carga',
                        'transportador'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_comercio_externo_importadores_cnpj_cpf ON comercio_externo_importadores (cnpj_cpf)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_comercio_externo_importadores_status ON comercio_externo_importadores (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_comercio_externo_importadores_municipio ON comercio_externo_importadores (municipio)"
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_importadores_municipio")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_importadores_status")
    op.execute("DROP INDEX IF EXISTS ix_comercio_externo_importadores_cnpj_cpf")
    op.execute("DROP TABLE IF EXISTS comercio_externo_importadores")
