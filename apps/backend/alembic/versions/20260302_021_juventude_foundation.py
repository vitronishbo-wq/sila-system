"""create juventude core tables

Revision ID: 20260302_021_juventude_foundation
Revises: 20260302_020_desporto_slice2_clubes_jogos
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260302_021_juventude_foundation"
down_revision = "20260302_020_desporto_slice2_clubes_jogos"
branch_labels = None
depends_on = None


def _create_jovens_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_jovens (
            id UUID PRIMARY KEY,
            numero_registro VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            data_nascimento DATE NOT NULL,
            faixa_etaria VARCHAR(20) NOT NULL,
            genero VARCHAR(20) NOT NULL,
            naturalidade VARCHAR(100) NOT NULL,
            nacionalidade VARCHAR(50) NOT NULL DEFAULT 'Angolana',
            escolaridade VARCHAR(40) NOT NULL,
            situacao_ocupacional VARCHAR(40) NOT NULL,
            endereco VARCHAR(255) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            telefone VARCHAR(20),
            email VARCHAR(120),
            citizen_id UUID,
            vulnerabilidades TEXT[],
            programas UUID[],
            auxilios UUID[],
            formacoes UUID[],
            experiencias JSONB,
            interesses TEXT[],
            habilidades TEXT[],
            encaminhamentos JSONB,
            acompanhamento_psicossocial BOOLEAN NOT NULL DEFAULT FALSE,
            data_cadastro DATE NOT NULL,
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
                WHERE conname = 'ck_juventude_jovens_nome_data'
                  AND conrelid = 'juventude_jovens'::regclass
            ) THEN
                ALTER TABLE juventude_jovens
                ADD CONSTRAINT ck_juventude_jovens_nome_data
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND data_nascimento < CURRENT_DATE
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
                WHERE conname = 'ck_juventude_jovens_enum_values'
                  AND conrelid = 'juventude_jovens'::regclass
            ) THEN
                ALTER TABLE juventude_jovens
                ADD CONSTRAINT ck_juventude_jovens_enum_values
                CHECK (
                    faixa_etaria IN ('15_17', '18_24', '25_29', '30_35')
                    AND escolaridade IN (
                        'sem_escolaridade',
                        'fundamental_incompleto',
                        'fundamental_completo',
                        'medio_incompleto',
                        'medio_completo',
                        'superior_incompleto',
                        'superior_completo',
                        'pos_graduacao'
                    )
                    AND situacao_ocupacional IN (
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

    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_numero_registro ON juventude_jovens (numero_registro)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_nome ON juventude_jovens (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_faixa_etaria ON juventude_jovens (faixa_etaria)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_escolaridade ON juventude_jovens (escolaridade)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_situacao_ocupacional ON juventude_jovens (situacao_ocupacional)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_municipio ON juventude_jovens (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_provincia ON juventude_jovens (provincia)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_citizen_id ON juventude_jovens (citizen_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_jovens_ativo ON juventude_jovens (ativo)")


def _create_auxilios_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS juventude_auxilios (
            id UUID PRIMARY KEY,
            codigo_auxilio VARCHAR(50) NOT NULL UNIQUE,
            jovem_id UUID NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            valor_mensal NUMERIC(12, 2),
            status VARCHAR(30) NOT NULL,
            data_cadastro DATE NOT NULL,
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
                WHERE conname = 'ck_juventude_auxilios_tipo_status'
                  AND conrelid = 'juventude_auxilios'::regclass
            ) THEN
                ALTER TABLE juventude_auxilios
                ADD CONSTRAINT ck_juventude_auxilios_tipo_status
                CHECK (
                    tipo IN (
                        'transporte',
                        'alimentacao',
                        'moradia',
                        'saude',
                        'psicologico',
                        'material_escolar',
                        'uniforme',
                        'tecnologico'
                    )
                    AND status IN ('ativo', 'suspenso', 'cancelado', 'concluido', 'aguardando')
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
                WHERE conname = 'ck_juventude_auxilios_periodo_valor'
                  AND conrelid = 'juventude_auxilios'::regclass
            ) THEN
                ALTER TABLE juventude_auxilios
                ADD CONSTRAINT ck_juventude_auxilios_periodo_valor
                CHECK (
                    (data_fim IS NULL OR data_fim >= data_inicio)
                    AND (valor_mensal IS NULL OR valor_mensal >= 0)
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_auxilios_codigo_auxilio ON juventude_auxilios (codigo_auxilio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_auxilios_jovem_id ON juventude_auxilios (jovem_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_auxilios_tipo ON juventude_auxilios (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_auxilios_status ON juventude_auxilios (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_juventude_auxilios_ativo ON juventude_auxilios (ativo)")


def upgrade() -> None:
    _create_jovens_table()
    _create_auxilios_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_juventude_auxilios_ativo")
    op.execute("DROP INDEX IF EXISTS ix_juventude_auxilios_status")
    op.execute("DROP INDEX IF EXISTS ix_juventude_auxilios_tipo")
    op.execute("DROP INDEX IF EXISTS ix_juventude_auxilios_jovem_id")
    op.execute("DROP INDEX IF EXISTS ix_juventude_auxilios_codigo_auxilio")
    op.execute("DROP TABLE IF EXISTS juventude_auxilios")

    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_ativo")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_provincia")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_municipio")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_situacao_ocupacional")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_escolaridade")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_faixa_etaria")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_nome")
    op.execute("DROP INDEX IF EXISTS ix_juventude_jovens_numero_registro")
    op.execute("DROP TABLE IF EXISTS juventude_jovens")
