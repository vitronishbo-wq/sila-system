"""add protecao_civil despachos and atendimentos

Revision ID: 20260302_031_protecao_civil_despachos_atendimentos
Revises: 20260302_030_protecao_civil_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_031_protecao_civil_despachos_atendimentos"
down_revision = "20260302_030_protecao_civil_foundation"
branch_labels = None
depends_on = None


def _create_despachos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS protecao_civil_despachos (
            id UUID PRIMARY KEY,
            codigo_despacho VARCHAR(50) NOT NULL UNIQUE,
            ocorrencia_id UUID NOT NULL,
            corporacao_id UUID NOT NULL,
            bombeiro_responsavel_id UUID,
            status VARCHAR(30) NOT NULL,
            data_despacho TIMESTAMP NOT NULL,
            data_ultima_atualizacao TIMESTAMP NOT NULL,
            meio_deslocamento VARCHAR(100),
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
                WHERE conname = 'ck_protecao_despachos_campos_basicos'
                  AND conrelid = 'protecao_civil_despachos'::regclass
            ) THEN
                ALTER TABLE protecao_civil_despachos
                ADD CONSTRAINT ck_protecao_despachos_campos_basicos
                CHECK (
                    char_length(trim(codigo_despacho)) >= 8
                    AND data_ultima_atualizacao >= data_despacho
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
                WHERE conname = 'ck_protecao_despachos_status'
                  AND conrelid = 'protecao_civil_despachos'::regclass
            ) THEN
                ALTER TABLE protecao_civil_despachos
                ADD CONSTRAINT ck_protecao_despachos_status
                CHECK (
                    status IN ('gerado', 'em_deslocamento', 'concluido', 'cancelado')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_codigo ON protecao_civil_despachos (codigo_despacho)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_ocorrencia_id ON protecao_civil_despachos (ocorrencia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_corporacao_id ON protecao_civil_despachos (corporacao_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_bombeiro_responsavel ON protecao_civil_despachos (bombeiro_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_status ON protecao_civil_despachos (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_data_despacho ON protecao_civil_despachos (data_despacho)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_data_ultima ON protecao_civil_despachos (data_ultima_atualizacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_despachos_ativo ON protecao_civil_despachos (ativo)"
    )


def _create_atendimentos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS protecao_civil_atendimentos (
            id UUID PRIMARY KEY,
            codigo_atendimento VARCHAR(50) NOT NULL UNIQUE,
            despacho_id UUID NOT NULL,
            ocorrencia_id UUID NOT NULL,
            status VARCHAR(30) NOT NULL,
            inicio_atendimento TIMESTAMP NOT NULL,
            fim_atendimento TIMESTAMP,
            local_atendimento VARCHAR(255) NOT NULL,
            resumo TEXT,
            vitimas_atendidas INTEGER NOT NULL DEFAULT 0,
            desalojados_atendidos INTEGER NOT NULL DEFAULT 0,
            obitos_confirmados INTEGER NOT NULL DEFAULT 0,
            equipe_responsavel_id UUID,
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
                WHERE conname = 'ck_protecao_atendimentos_campos_basicos'
                  AND conrelid = 'protecao_civil_atendimentos'::regclass
            ) THEN
                ALTER TABLE protecao_civil_atendimentos
                ADD CONSTRAINT ck_protecao_atendimentos_campos_basicos
                CHECK (
                    char_length(trim(codigo_atendimento)) >= 8
                    AND char_length(trim(local_atendimento)) >= 3
                    AND vitimas_atendidas >= 0
                    AND desalojados_atendidos >= 0
                    AND obitos_confirmados >= 0
                    AND (fim_atendimento IS NULL OR fim_atendimento >= inicio_atendimento)
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
                WHERE conname = 'ck_protecao_atendimentos_status'
                  AND conrelid = 'protecao_civil_atendimentos'::regclass
            ) THEN
                ALTER TABLE protecao_civil_atendimentos
                ADD CONSTRAINT ck_protecao_atendimentos_status
                CHECK (
                    status IN ('iniciado', 'em_andamento', 'finalizado', 'cancelado')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_codigo ON protecao_civil_atendimentos (codigo_atendimento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_despacho_id ON protecao_civil_atendimentos (despacho_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_ocorrencia_id ON protecao_civil_atendimentos (ocorrencia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_status ON protecao_civil_atendimentos (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_inicio ON protecao_civil_atendimentos (inicio_atendimento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_fim ON protecao_civil_atendimentos (fim_atendimento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_equipe ON protecao_civil_atendimentos (equipe_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_atendimentos_ativo ON protecao_civil_atendimentos (ativo)"
    )


def upgrade() -> None:
    _create_despachos_table()
    _create_atendimentos_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_equipe")
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_fim")
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_inicio")
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_status")
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_ocorrencia_id")
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_despacho_id")
    op.execute("DROP INDEX IF EXISTS ix_protecao_atendimentos_codigo")
    op.execute("DROP TABLE IF EXISTS protecao_civil_atendimentos")

    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_data_ultima")
    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_data_despacho")
    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_status")
    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_bombeiro_responsavel")
    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_corporacao_id")
    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_ocorrencia_id")
    op.execute("DROP INDEX IF EXISTS ix_protecao_despachos_codigo")
    op.execute("DROP TABLE IF EXISTS protecao_civil_despachos")
