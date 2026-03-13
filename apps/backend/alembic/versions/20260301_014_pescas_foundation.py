"""create pescas core tables

Revision ID: 20260301_014_pescas_foundation
Revises: 20260301_013_comex_drawback_modalidades_siscomex_verde_amarelo
Create Date: 2026-03-01 23:59:59.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260301_014_pescas_foundation"
down_revision = "20260301_013_comex_drawback_modalidades_siscomex_verde_amarelo"
branch_labels = None
depends_on = None


def _create_pescadores_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_pescadores (
            id UUID PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            numero_registro VARCHAR(50) NOT NULL UNIQUE,
            tipo VARCHAR(30) NOT NULL,
            citizen_id UUID NOT NULL,
            data_registro DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            telefone VARCHAR(32),
            email VARCHAR(255),
            cooperativa_id UUID,
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
                WHERE conname = 'ck_pescas_pescadores_tipo'
                  AND conrelid = 'pescas_pescadores'::regclass
            ) THEN
                ALTER TABLE pescas_pescadores
                ADD CONSTRAINT ck_pescas_pescadores_tipo
                CHECK (tipo IN ('artesanal', 'industrial', 'desportivo', 'cientifico'));
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_pescadores_numero_registro ON pescas_pescadores (numero_registro)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_pescadores_tipo ON pescas_pescadores (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_pescadores_citizen_id ON pescas_pescadores (citizen_id)")


def _create_armadores_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_armadores (
            id UUID PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            nif VARCHAR(32) NOT NULL UNIQUE,
            data_registro DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            telefone VARCHAR(32),
            email VARCHAR(255),
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_armadores_nif ON pescas_armadores (nif)")


def _create_embarcacoes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_embarcacoes (
            id UUID PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            numero_inscricao VARCHAR(50) NOT NULL UNIQUE,
            tipo VARCHAR(30) NOT NULL,
            modalidades TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
            comprimento NUMERIC(10, 2) NOT NULL,
            arqueacao_bruta NUMERIC(10, 2) NOT NULL,
            potencia_motor NUMERIC(10, 2),
            capacidade_porao NUMERIC(10, 2),
            tripulacao_minima INTEGER NOT NULL DEFAULT 1,
            porto_registro VARCHAR(60) NOT NULL,
            ano_construcao INTEGER NOT NULL,
            material_casco VARCHAR(60) NOT NULL,
            proprietario_id UUID NOT NULL,
            armador_id UUID,
            licenca_id UUID,
            sistema_rastreio VARCHAR(60),
            data_inspecao DATE,
            data_validade_doc DATE,
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
                WHERE conname = 'ck_pescas_embarcacoes_tipo'
                  AND conrelid = 'pescas_embarcacoes'::regclass
            ) THEN
                ALTER TABLE pescas_embarcacoes
                ADD CONSTRAINT ck_pescas_embarcacoes_tipo
                CHECK (tipo IN ('artesanal', 'industrial', 'apoio', 'pesquisa'));
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
                WHERE conname = 'ck_pescas_embarcacoes_tripulacao_minima'
                  AND conrelid = 'pescas_embarcacoes'::regclass
            ) THEN
                ALTER TABLE pescas_embarcacoes
                ADD CONSTRAINT ck_pescas_embarcacoes_tripulacao_minima
                CHECK (tripulacao_minima > 0);
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
                WHERE conname = 'ck_pescas_embarcacoes_dimensoes'
                  AND conrelid = 'pescas_embarcacoes'::regclass
            ) THEN
                ALTER TABLE pescas_embarcacoes
                ADD CONSTRAINT ck_pescas_embarcacoes_dimensoes
                CHECK (comprimento > 0 AND arqueacao_bruta > 0);
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_embarcacoes_numero_inscricao ON pescas_embarcacoes (numero_inscricao)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_embarcacoes_tipo ON pescas_embarcacoes (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_embarcacoes_proprietario_id ON pescas_embarcacoes (proprietario_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_embarcacoes_armador_id ON pescas_embarcacoes (armador_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_embarcacoes_licenca_id ON pescas_embarcacoes (licenca_id)")


def _create_licencas_pesca_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_licencas_pesca (
            id UUID PRIMARY KEY,
            numero_licenca VARCHAR(50) NOT NULL UNIQUE,
            embarcacao_id UUID NOT NULL,
            titular_id UUID NOT NULL,
            data_emissao DATE NOT NULL,
            data_validade DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            modalidade_autorizada VARCHAR(60) NOT NULL,
            zona_pesca_id UUID NOT NULL,
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
                WHERE conname = 'ck_pescas_licencas_status'
                  AND conrelid = 'pescas_licencas_pesca'::regclass
            ) THEN
                ALTER TABLE pescas_licencas_pesca
                ADD CONSTRAINT ck_pescas_licencas_status
                CHECK (status IN ('requerida', 'em_analise', 'deferida', 'indeferida', 'vencida', 'suspensa', 'cancelada'));
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
                WHERE conname = 'ck_pescas_licencas_validade'
                  AND conrelid = 'pescas_licencas_pesca'::regclass
            ) THEN
                ALTER TABLE pescas_licencas_pesca
                ADD CONSTRAINT ck_pescas_licencas_validade
                CHECK (data_validade >= data_emissao);
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_licencas_numero_licenca ON pescas_licencas_pesca (numero_licenca)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_licencas_embarcacao_id ON pescas_licencas_pesca (embarcacao_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_licencas_titular_id ON pescas_licencas_pesca (titular_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_licencas_data_validade ON pescas_licencas_pesca (data_validade)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_licencas_status ON pescas_licencas_pesca (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_licencas_zona_pesca_id ON pescas_licencas_pesca (zona_pesca_id)")


def _create_capturas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_capturas (
            id UUID PRIMARY KEY,
            embarcacao_id UUID NOT NULL,
            licenca_id UUID NOT NULL,
            data_inicio TIMESTAMPTZ NOT NULL,
            data_fim TIMESTAMPTZ NOT NULL,
            zona_pesca_id UUID NOT NULL,
            especie_id UUID NOT NULL,
            quantidade_kg NUMERIC(12, 3) NOT NULL,
            quantidade_unidades INTEGER,
            arte_pesca_id UUID NOT NULL,
            profundidade NUMERIC(8, 2),
            coordenadas_inicio VARCHAR(120),
            coordenadas_fim VARCHAR(120),
            condicoes_mar VARCHAR(120),
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
                WHERE conname = 'ck_pescas_capturas_quantidade_kg'
                  AND conrelid = 'pescas_capturas'::regclass
            ) THEN
                ALTER TABLE pescas_capturas
                ADD CONSTRAINT ck_pescas_capturas_quantidade_kg
                CHECK (quantidade_kg > 0);
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
                WHERE conname = 'ck_pescas_capturas_periodo'
                  AND conrelid = 'pescas_capturas'::regclass
            ) THEN
                ALTER TABLE pescas_capturas
                ADD CONSTRAINT ck_pescas_capturas_periodo
                CHECK (data_fim >= data_inicio);
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_capturas_embarcacao_id ON pescas_capturas (embarcacao_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_capturas_licenca_id ON pescas_capturas (licenca_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_capturas_zona_pesca_id ON pescas_capturas (zona_pesca_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_capturas_especie_id ON pescas_capturas (especie_id)")


def _create_especies_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_especies (
            id UUID PRIMARY KEY,
            nome_comum VARCHAR(120) NOT NULL,
            nome_cientifico VARCHAR(150) NOT NULL,
            codigo_fao VARCHAR(20) NOT NULL UNIQUE,
            ameacada BOOLEAN NOT NULL DEFAULT FALSE,
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_especies_codigo_fao ON pescas_especies (codigo_fao)")


def _create_desembarques_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_desembarques (
            id UUID PRIMARY KEY,
            captura_id UUID NOT NULL,
            porto_desembarque VARCHAR(80) NOT NULL,
            data_desembarque TIMESTAMPTZ NOT NULL,
            quantidade_kg NUMERIC(12, 3) NOT NULL,
            inspecao_aprovada BOOLEAN NOT NULL DEFAULT FALSE,
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
                WHERE conname = 'ck_pescas_desembarques_quantidade_kg'
                  AND conrelid = 'pescas_desembarques'::regclass
            ) THEN
                ALTER TABLE pescas_desembarques
                ADD CONSTRAINT ck_pescas_desembarques_quantidade_kg
                CHECK (quantidade_kg > 0);
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_desembarques_captura_id ON pescas_desembarques (captura_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_pescas_desembarques_porto ON pescas_desembarques (porto_desembarque)")


def upgrade():
    _create_pescadores_table()
    _create_armadores_table()
    _create_embarcacoes_table()
    _create_licencas_pesca_table()
    _create_capturas_table()
    _create_especies_table()
    _create_desembarques_table()


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_pescas_desembarques_porto")
    op.execute("DROP INDEX IF EXISTS ix_pescas_desembarques_captura_id")
    op.execute("DROP TABLE IF EXISTS pescas_desembarques")

    op.execute("DROP INDEX IF EXISTS ix_pescas_especies_codigo_fao")
    op.execute("DROP TABLE IF EXISTS pescas_especies")

    op.execute("DROP INDEX IF EXISTS ix_pescas_capturas_especie_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_capturas_zona_pesca_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_capturas_licenca_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_capturas_embarcacao_id")
    op.execute("DROP TABLE IF EXISTS pescas_capturas")

    op.execute("DROP INDEX IF EXISTS ix_pescas_licencas_zona_pesca_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_licencas_status")
    op.execute("DROP INDEX IF EXISTS ix_pescas_licencas_data_validade")
    op.execute("DROP INDEX IF EXISTS ix_pescas_licencas_titular_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_licencas_embarcacao_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_licencas_numero_licenca")
    op.execute("DROP TABLE IF EXISTS pescas_licencas_pesca")

    op.execute("DROP INDEX IF EXISTS ix_pescas_embarcacoes_licenca_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_embarcacoes_armador_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_embarcacoes_proprietario_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_embarcacoes_tipo")
    op.execute("DROP INDEX IF EXISTS ix_pescas_embarcacoes_numero_inscricao")
    op.execute("DROP TABLE IF EXISTS pescas_embarcacoes")

    op.execute("DROP INDEX IF EXISTS ix_pescas_armadores_nif")
    op.execute("DROP TABLE IF EXISTS pescas_armadores")

    op.execute("DROP INDEX IF EXISTS ix_pescas_pescadores_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_pescadores_tipo")
    op.execute("DROP INDEX IF EXISTS ix_pescas_pescadores_numero_registro")
    op.execute("DROP TABLE IF EXISTS pescas_pescadores")
