"""create comercio_externo_drawback_externo and drawback_interno tables

Revision ID: 20260301_012_comex_drawback_modalidades_externo_interno
Revises: 20260301_011_comex_drawback_modalidades_complementares
Create Date: 2026-03-01 23:59:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260301_012_comex_drawback_modalidades_externo_interno"
down_revision = "20260301_011_comex_drawback_modalidades_complementares"
branch_labels = None
depends_on = None


def _create_habilitacao_table(*, table_name: str, suffix: str, tipo_operador: str) -> None:
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
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
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
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
                SELECT 1 FROM pg_constraint
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
                SELECT 1 FROM pg_constraint
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

    op.execute(
        f"CREATE INDEX IF NOT EXISTS ix_{table_name}_numero_processo ON {table_name} (numero_processo)"
    )
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table_name}_status ON {table_name} (status)")
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table_name}_cnpj_cpf ON {table_name} (cnpj_cpf)")


def _drop_habilitacao_table(*, table_name: str) -> None:
    op.execute(f"DROP INDEX IF EXISTS ix_{table_name}_cnpj_cpf")
    op.execute(f"DROP INDEX IF EXISTS ix_{table_name}_status")
    op.execute(f"DROP INDEX IF EXISTS ix_{table_name}_numero_processo")
    op.execute(f"DROP TABLE IF EXISTS {table_name}")


def upgrade():
    _create_habilitacao_table(
        table_name="comercio_externo_drawback_externo",
        suffix="comex_drawback_externo",
        tipo_operador="exportador_importador",
    )
    _create_habilitacao_table(
        table_name="comercio_externo_drawback_interno",
        suffix="comex_drawback_interno",
        tipo_operador="exportador_importador",
    )


def downgrade():
    _drop_habilitacao_table(table_name="comercio_externo_drawback_interno")
    _drop_habilitacao_table(table_name="comercio_externo_drawback_externo")
