"""create comercio_externo_despachantes and comercio_externo_agentes_carga tables

Revision ID: 20260301_003_comex_operadores_logisticos
Revises: 20260301_002_comex_importadores
Create Date: 2026-03-01 16:20:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260301_003_comex_operadores_logisticos"
down_revision = "20260301_002_comex_importadores"
branch_labels = None
depends_on = None


def _create_operador_logistico_table(*, table_name: str, tipo_operador: str, suffix: str) -> None:
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
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
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'ck_{suffix}_status'
                  AND conrelid = '{table_name}'::regclass
            ) THEN
                ALTER TABLE {table_name}
                ADD CONSTRAINT ck_{suffix}_status
                CHECK (status IN ('pendente', 'habilitado', 'suspenso', 'cancelado', 'bloqueado'));
            END IF;
        END $$;
        """
    )

    op.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'ck_{suffix}_tipo_pessoa'
                  AND conrelid = '{table_name}'::regclass
            ) THEN
                ALTER TABLE {table_name}
                ADD CONSTRAINT ck_{suffix}_tipo_pessoa
                CHECK (tipo_pessoa IN ('fisica', 'juridica'));
            END IF;
        END $$;
        """
    )

    op.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'ck_{suffix}_tipo_operador'
                  AND conrelid = '{table_name}'::regclass
            ) THEN
                ALTER TABLE {table_name}
                ADD CONSTRAINT ck_{suffix}_tipo_operador
                CHECK (tipo_operador = '{tipo_operador}');
            END IF;
        END $$;
        """
    )

    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table_name}_cnpj_cpf ON {table_name} (cnpj_cpf)")
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table_name}_status ON {table_name} (status)")
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table_name}_municipio ON {table_name} (municipio)")


def _drop_operador_logistico_table(*, table_name: str) -> None:
    op.execute(f"DROP INDEX IF EXISTS ix_{table_name}_municipio")
    op.execute(f"DROP INDEX IF EXISTS ix_{table_name}_status")
    op.execute(f"DROP INDEX IF EXISTS ix_{table_name}_cnpj_cpf")
    op.execute(f"DROP TABLE IF EXISTS {table_name}")


def upgrade():
    _create_operador_logistico_table(
        table_name="comercio_externo_despachantes",
        tipo_operador="despachante",
        suffix="comex_despachantes",
    )
    _create_operador_logistico_table(
        table_name="comercio_externo_agentes_carga",
        tipo_operador="agente_carga",
        suffix="comex_agentes_carga",
    )


def downgrade():
    _drop_operador_logistico_table(table_name="comercio_externo_agentes_carga")
    _drop_operador_logistico_table(table_name="comercio_externo_despachantes")
