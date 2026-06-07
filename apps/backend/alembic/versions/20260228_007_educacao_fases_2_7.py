"""add educacao tables for fases 2 to 7

Revision ID: 20260228_007_edu_f2_f7
Revises: 20260228_006_saude_status_ck
Create Date: 2026-02-28 07:20:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260228_007_edu_f2_f7"
down_revision = "20260228_006_saude_status_ck"
branch_labels = None
depends_on = None


TABLES: tuple[str, ...] = (
    "educacao_boletins",
    "educacao_certificados",
    "educacao_transferencias",
    "educacao_propinas",
    "educacao_empregos",
    "educacao_concursos",
    "educacao_formacoes",
    "educacao_universidade",
)

STATUS_ALLOWED = (
    "pendente",
    "confirmada",
    "em_analise",
    "aprovada",
    "rejeitada",
    "concluida",
    "cancelada",
)


def _create_workflow_table(table: str) -> None:
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id UUID PRIMARY KEY,
            numero_processo VARCHAR(64) NOT NULL UNIQUE,
            service_type VARCHAR(64) NOT NULL,
            citizen_id UUID NOT NULL,
            instituicao_id UUID NOT NULL,
            data_registo DATE NOT NULL,
            status VARCHAR(24) NOT NULL DEFAULT 'pendente',
            observacoes TEXT,
            metadata_json JSONB NOT NULL DEFAULT '{{}}'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        """
    )
    op.execute(
        f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ
        """
    )
    op.execute(
        f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS metadata_json JSONB NOT NULL DEFAULT '{{}}'::jsonb
        """
    )
    op.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'ck_{table}_status'
                  AND conrelid = '{table}'::regclass
            ) THEN
                ALTER TABLE {table}
                ADD CONSTRAINT ck_{table}_status
                CHECK (status IN {STATUS_ALLOWED});
            END IF;
        END $$;
        """
    )

    op.execute(
        f"CREATE INDEX IF NOT EXISTS ix_{table}_numero_processo ON {table} (numero_processo)"
    )
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table}_service_type ON {table} (service_type)")
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table}_citizen_id ON {table} (citizen_id)")
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table}_instituicao_id ON {table} (instituicao_id)")
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_{table}_status ON {table} (status)")


def upgrade():
    for table in TABLES:
        _create_workflow_table(table)


def downgrade():
    for table in TABLES:
        op.execute(f"DROP INDEX IF EXISTS ix_{table}_status")
        op.execute(f"DROP INDEX IF EXISTS ix_{table}_instituicao_id")
        op.execute(f"DROP INDEX IF EXISTS ix_{table}_citizen_id")
        op.execute(f"DROP INDEX IF EXISTS ix_{table}_service_type")
        op.execute(f"DROP INDEX IF EXISTS ix_{table}_numero_processo")
        op.execute(f"DROP TABLE IF EXISTS {table}")
