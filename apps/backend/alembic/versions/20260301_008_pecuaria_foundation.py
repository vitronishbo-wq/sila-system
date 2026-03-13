"""create pecuaria core tables

Revision ID: 20260301_008_pecuaria_foundation
Revises: 20260301_007_comex_processos_radar
Create Date: 2026-03-01 22:10:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260301_008_pecuaria_foundation"
down_revision = "20260301_007_comex_processos_radar"
branch_labels = None
depends_on = None


def _create_pecuaristas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pecuaria_pecuaristas (
            id UUID PRIMARY KEY,
            cadastro_pecuarista VARCHAR(32) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            documento VARCHAR(50) NOT NULL UNIQUE,
            documento_tipo VARCHAR(30) NOT NULL,
            data_cadastro DATE NOT NULL DEFAULT current_date,
            status VARCHAR(24) NOT NULL,
            telefone VARCHAR(30),
            email VARCHAR(120),
            endereco TEXT,
            citizen_id UUID,
            empresa_id UUID,
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
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_pecuaria_pecuaristas_status'
                  AND conrelid = 'pecuaria_pecuaristas'::regclass
            ) THEN
                ALTER TABLE pecuaria_pecuaristas
                ADD CONSTRAINT ck_pecuaria_pecuaristas_status
                CHECK (status IN ('pendente', 'ativo', 'suspenso', 'inativo'));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_pecuaristas_cadastro_pecuarista ON pecuaria_pecuaristas (cadastro_pecuarista)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_pecuaristas_documento ON pecuaria_pecuaristas (documento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_pecuaristas_status ON pecuaria_pecuaristas (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_pecuaristas_citizen_id ON pecuaria_pecuaristas (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_pecuaristas_empresa_id ON pecuaria_pecuaristas (empresa_id)"
    )


def _create_propriedades_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pecuaria_propriedades (
            id UUID PRIMARY KEY,
            codigo_propriedade VARCHAR(32) NOT NULL UNIQUE,
            pecuarista_id UUID NOT NULL,
            nome VARCHAR(200) NOT NULL,
            area_total_ha DOUBLE PRECISION NOT NULL,
            municipio VARCHAR(120) NOT NULL,
            provincia VARCHAR(120) NOT NULL,
            data_cadastro DATE NOT NULL DEFAULT current_date,
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
                WHERE conname = 'ck_pecuaria_propriedades_area_total_ha'
                  AND conrelid = 'pecuaria_propriedades'::regclass
            ) THEN
                ALTER TABLE pecuaria_propriedades
                ADD CONSTRAINT ck_pecuaria_propriedades_area_total_ha
                CHECK (area_total_ha > 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_propriedades_codigo_propriedade ON pecuaria_propriedades (codigo_propriedade)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_propriedades_pecuarista_id ON pecuaria_propriedades (pecuarista_id)"
    )


def _create_rebanhos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pecuaria_rebanhos (
            id UUID PRIMARY KEY,
            codigo_rebanho VARCHAR(32) NOT NULL UNIQUE,
            propriedade_id UUID NOT NULL,
            tipo_animal VARCHAR(32) NOT NULL,
            descricao TEXT NOT NULL,
            quantidade_animais INTEGER NOT NULL DEFAULT 0,
            data_cadastro DATE NOT NULL DEFAULT current_date,
            status VARCHAR(24) NOT NULL,
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
                WHERE conname = 'ck_pecuaria_rebanhos_status'
                  AND conrelid = 'pecuaria_rebanhos'::regclass
            ) THEN
                ALTER TABLE pecuaria_rebanhos
                ADD CONSTRAINT ck_pecuaria_rebanhos_status
                CHECK (status IN ('ativo', 'encerrado'));
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
                WHERE conname = 'ck_pecuaria_rebanhos_tipo_animal'
                  AND conrelid = 'pecuaria_rebanhos'::regclass
            ) THEN
                ALTER TABLE pecuaria_rebanhos
                ADD CONSTRAINT ck_pecuaria_rebanhos_tipo_animal
                CHECK (tipo_animal IN ('bovino', 'caprino', 'ovino', 'suino', 'equino', 'bufalino', 'aves'));
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
                WHERE conname = 'ck_pecuaria_rebanhos_quantidade_animais'
                  AND conrelid = 'pecuaria_rebanhos'::regclass
            ) THEN
                ALTER TABLE pecuaria_rebanhos
                ADD CONSTRAINT ck_pecuaria_rebanhos_quantidade_animais
                CHECK (quantidade_animais >= 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_rebanhos_codigo_rebanho ON pecuaria_rebanhos (codigo_rebanho)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_rebanhos_propriedade_id ON pecuaria_rebanhos (propriedade_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_rebanhos_tipo_animal ON pecuaria_rebanhos (tipo_animal)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_rebanhos_status ON pecuaria_rebanhos (status)"
    )


def _create_animais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pecuaria_animais (
            id UUID PRIMARY KEY,
            brinco VARCHAR(20) NOT NULL UNIQUE,
            nome VARCHAR(100),
            tipo VARCHAR(32) NOT NULL,
            raca_id UUID NOT NULL,
            sexo VARCHAR(16) NOT NULL,
            data_nascimento DATE NOT NULL,
            peso_nascimento NUMERIC(10, 2),
            peso_atual NUMERIC(10, 2),
            status VARCHAR(24) NOT NULL,
            proprietario_id UUID NOT NULL,
            propriedade_id UUID NOT NULL,
            rebanho_id UUID,
            mae_id UUID,
            pai_id UUID,
            data_entrada DATE NOT NULL,
            data_saida DATE,
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
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_pecuaria_animais_tipo'
                  AND conrelid = 'pecuaria_animais'::regclass
            ) THEN
                ALTER TABLE pecuaria_animais
                ADD CONSTRAINT ck_pecuaria_animais_tipo
                CHECK (tipo IN ('bovino', 'caprino', 'ovino', 'suino', 'equino', 'bufalino', 'aves'));
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
                WHERE conname = 'ck_pecuaria_animais_sexo'
                  AND conrelid = 'pecuaria_animais'::regclass
            ) THEN
                ALTER TABLE pecuaria_animais
                ADD CONSTRAINT ck_pecuaria_animais_sexo
                CHECK (sexo IN ('macho', 'femea'));
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
                WHERE conname = 'ck_pecuaria_animais_status'
                  AND conrelid = 'pecuaria_animais'::regclass
            ) THEN
                ALTER TABLE pecuaria_animais
                ADD CONSTRAINT ck_pecuaria_animais_status
                CHECK (status IN ('ativo', 'vendido', 'morto', 'abatido', 'descartado'));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_animais_brinco ON pecuaria_animais (brinco)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_animais_tipo ON pecuaria_animais (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_animais_status ON pecuaria_animais (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_animais_proprietario_id ON pecuaria_animais (proprietario_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_animais_propriedade_id ON pecuaria_animais (propriedade_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_animais_rebanho_id ON pecuaria_animais (rebanho_id)"
    )


def _create_producao_leite_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pecuaria_producao_leite (
            id UUID PRIMARY KEY,
            propriedade_id UUID NOT NULL,
            litros DOUBLE PRECISION NOT NULL,
            data_producao DATE NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'ck_pecuaria_producao_leite_litros'
                  AND conrelid = 'pecuaria_producao_leite'::regclass
            ) THEN
                ALTER TABLE pecuaria_producao_leite
                ADD CONSTRAINT ck_pecuaria_producao_leite_litros
                CHECK (litros > 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_producao_leite_propriedade_id ON pecuaria_producao_leite (propriedade_id)"
    )


def _create_vacinas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pecuaria_vacinas (
            id UUID PRIMARY KEY,
            animal_id UUID NOT NULL,
            nome VARCHAR(160) NOT NULL,
            data_aplicacao DATE NOT NULL,
            proxima_dose DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pecuaria_vacinas_animal_id ON pecuaria_vacinas (animal_id)"
    )


def upgrade():
    _create_pecuaristas_table()
    _create_propriedades_table()
    _create_rebanhos_table()
    _create_animais_table()
    _create_producao_leite_table()
    _create_vacinas_table()


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_vacinas_animal_id")
    op.execute("DROP TABLE IF EXISTS pecuaria_vacinas")

    op.execute("DROP INDEX IF EXISTS ix_pecuaria_producao_leite_propriedade_id")
    op.execute("DROP TABLE IF EXISTS pecuaria_producao_leite")

    op.execute("DROP INDEX IF EXISTS ix_pecuaria_animais_rebanho_id")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_animais_propriedade_id")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_animais_proprietario_id")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_animais_status")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_animais_tipo")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_animais_brinco")
    op.execute("DROP TABLE IF EXISTS pecuaria_animais")

    op.execute("DROP INDEX IF EXISTS ix_pecuaria_rebanhos_status")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_rebanhos_tipo_animal")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_rebanhos_propriedade_id")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_rebanhos_codigo_rebanho")
    op.execute("DROP TABLE IF EXISTS pecuaria_rebanhos")

    op.execute("DROP INDEX IF EXISTS ix_pecuaria_propriedades_pecuarista_id")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_propriedades_codigo_propriedade")
    op.execute("DROP TABLE IF EXISTS pecuaria_propriedades")

    op.execute("DROP INDEX IF EXISTS ix_pecuaria_pecuaristas_empresa_id")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_pecuaristas_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_pecuaristas_status")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_pecuaristas_documento")
    op.execute("DROP INDEX IF EXISTS ix_pecuaria_pecuaristas_cadastro_pecuarista")
    op.execute("DROP TABLE IF EXISTS pecuaria_pecuaristas")
