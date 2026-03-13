"""add materia_processual to justica_processos

Revision ID: 20260305_048_justica_add_materia_processual
Revises: 20260305_047_estatistica_enterprise_foundation, 20260305_047_familia_foundation
Create Date: 2026-03-05 12:10:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260305_048_justica_add_materia_processual"
down_revision = ("20260305_047_estatistica_enterprise_foundation", "20260305_047_familia_foundation")
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF to_regclass('public.justica_processos') IS NOT NULL THEN
                ALTER TABLE justica_processos
                ADD COLUMN IF NOT EXISTS materia_processual VARCHAR(32);

                UPDATE justica_processos
                SET materia_processual = CASE
                    WHEN tipo = 'familia' THEN 'familia'
                    WHEN tipo = 'penal' THEN 'criminal'
                    ELSE 'civel'
                END
                WHERE materia_processual IS NULL;

                ALTER TABLE justica_processos
                ALTER COLUMN materia_processual SET DEFAULT 'civel';

                ALTER TABLE justica_processos
                ALTER COLUMN materia_processual SET NOT NULL;

                EXECUTE 'CREATE INDEX IF NOT EXISTS ix_justica_processos_materia_processual ON justica_processos (materia_processual)';
            END IF;
        END
        $$;
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_justica_processos_materia_processual")
    op.execute(
        """
        ALTER TABLE IF EXISTS justica_processos
        DROP COLUMN IF EXISTS materia_processual
        """
    )
