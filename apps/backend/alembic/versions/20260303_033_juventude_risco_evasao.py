"""create juventude riscos evasao table

Revision ID: 20260303_033_juventude_risco_evasao
Revises: 20260302_032_ciencia_pesquisa_foundation
Create Date: 2026-03-03 10:30:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260303_033_juventude_risco_evasao"
down_revision = "20260302_032_ciencia_pesquisa_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_riscos_evasao (
            id UUID PRIMARY KEY,
            codigo_risco VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            citizen_id UUID,
            matricula_ativa BOOLEAN NOT NULL DEFAULT FALSE,
            situacao_ocupacional VARCHAR(40) NOT NULL,
            vulnerabilidades TEXT[],
            pontuacao INTEGER NOT NULL,
            nivel_risco VARCHAR(20) NOT NULL,
            data_avaliacao DATE NOT NULL,
            fatores JSONB NOT NULL DEFAULT '[]'::jsonb,
            recomendacoes JSONB NOT NULL DEFAULT '[]'::jsonb,
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
                WHERE conname = 'ck_juventude_riscos_evasao_nivel_pontuacao'
                  AND conrelid = 'juventude_riscos_evasao'::regclass
            ) THEN
                ALTER TABLE juventude_riscos_evasao
                ADD CONSTRAINT ck_juventude_riscos_evasao_nivel_pontuacao
                CHECK (
                    pontuacao >= 0 AND pontuacao <= 100
                    AND nivel_risco IN ('baixo', 'medio', 'alto', 'critico')
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
                WHERE conname = 'ck_juventude_riscos_evasao_situacao'
                  AND conrelid = 'juventude_riscos_evasao'::regclass
            ) THEN
                ALTER TABLE juventude_riscos_evasao
                ADD CONSTRAINT ck_juventude_riscos_evasao_situacao
                CHECK (
                    situacao_ocupacional IN (
                        'estuda',
                        'trabalha',
                        'estuda_trabalha',
                        'desempregado',
                        'procura_emprego',
                        'nao_estuda_nao_trabalha'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_juventude_riscos_evasao_codigo_risco ON juventude_riscos_evasao (codigo_risco)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_juventude_riscos_evasao_jovem_id ON juventude_riscos_evasao (jovem_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_juventude_riscos_evasao_citizen_id ON juventude_riscos_evasao (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_juventude_riscos_evasao_nivel_risco ON juventude_riscos_evasao (nivel_risco)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_juventude_riscos_evasao_data_avaliacao ON juventude_riscos_evasao (data_avaliacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_juventude_riscos_evasao_ativo ON juventude_riscos_evasao (ativo)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_juventude_riscos_evasao_ativo")
    op.execute("DROP INDEX IF EXISTS ix_juventude_riscos_evasao_data_avaliacao")
    op.execute("DROP INDEX IF EXISTS ix_juventude_riscos_evasao_nivel_risco")
    op.execute("DROP INDEX IF EXISTS ix_juventude_riscos_evasao_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_juventude_riscos_evasao_jovem_id")
    op.execute("DROP INDEX IF EXISTS ix_juventude_riscos_evasao_codigo_risco")
    op.execute("DROP TABLE IF EXISTS juventude_riscos_evasao")
