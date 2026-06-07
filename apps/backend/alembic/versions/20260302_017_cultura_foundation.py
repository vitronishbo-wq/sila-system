"""create cultura core tables

Revision ID: 20260302_017_cultura_foundation
Revises: 20260302_016_pescas_industriais_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_017_cultura_foundation"
down_revision = "20260302_016_pescas_industriais_foundation"
branch_labels = None
depends_on = None


def _create_artistas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_artistas (
            id UUID PRIMARY KEY,
            registro_cultural VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            nome_artistico VARCHAR(200),
            tipo TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
            data_nascimento DATE,
            naturalidade VARCHAR(100),
            nacionalidade VARCHAR(50) NOT NULL DEFAULT 'Angolana',
            biografia TEXT,
            citizen_id UUID,
            municipio VARCHAR(100),
            provincia VARCHAR(100),
            data_cadastro DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
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
                WHERE conname = 'ck_cultura_artistas_nome'
                  AND conrelid = 'cultura_artistas'::regclass
            ) THEN
                ALTER TABLE cultura_artistas
                ADD CONSTRAINT ck_cultura_artistas_nome
                CHECK (char_length(trim(nome)) >= 3);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_artistas_registro ON cultura_artistas (registro_cultural)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_artistas_nome ON cultura_artistas (nome)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_artistas_citizen_id ON cultura_artistas (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_artistas_municipio ON cultura_artistas (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_artistas_provincia ON cultura_artistas (provincia)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_artistas_ativo ON cultura_artistas (ativo)")


def _create_bens_culturais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_bens_culturais (
            id UUID PRIMARY KEY,
            registro_ipat VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            descricao TEXT NOT NULL,
            localizacao VARCHAR(255) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            coordenadas_lat NUMERIC(10, 7),
            coordenadas_long NUMERIC(10, 7),
            status_tombamento VARCHAR(30) NOT NULL,
            tombamento_id UUID,
            data_cadastro DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
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
                WHERE conname = 'ck_cultura_bens_tipo'
                  AND conrelid = 'cultura_bens_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_bens_culturais
                ADD CONSTRAINT ck_cultura_bens_tipo
                CHECK (tipo IN ('material', 'imaterial', 'arqueologico', 'historico', 'artistico', 'paisagistico'));
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
                WHERE conname = 'ck_cultura_bens_status_tombamento'
                  AND conrelid = 'cultura_bens_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_bens_culturais
                ADD CONSTRAINT ck_cultura_bens_status_tombamento
                CHECK (status_tombamento IN ('proposto', 'em_analise', 'tombado', 'cancelado', 'revogado'));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_bens_registro ON cultura_bens_culturais (registro_ipat)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_bens_nome ON cultura_bens_culturais (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_bens_tipo ON cultura_bens_culturais (tipo)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_bens_municipio ON cultura_bens_culturais (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_bens_provincia ON cultura_bens_culturais (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_bens_status_tombamento ON cultura_bens_culturais (status_tombamento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_bens_tombamento_id ON cultura_bens_culturais (tombamento_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_cultura_bens_ativo ON cultura_bens_culturais (ativo)")


def _create_eventos_culturais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS cultura_eventos_culturais (
            id UUID PRIMARY KEY,
            codigo_evento VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            descricao TEXT NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE NOT NULL,
            local VARCHAR(200) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            realizador_id UUID NOT NULL,
            atracao_turistica_id UUID,
            instituicao_educacional_id UUID,
            entrada_gratuita BOOLEAN NOT NULL DEFAULT TRUE,
            valor_ingresso NUMERIC(10, 2),
            publico_estimado INTEGER,
            status VARCHAR(30) NOT NULL,
            data_cadastro DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
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
                WHERE conname = 'ck_cultura_eventos_tipo'
                  AND conrelid = 'cultura_eventos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_eventos_culturais
                ADD CONSTRAINT ck_cultura_eventos_tipo
                CHECK (tipo IN ('festival', 'mostra', 'exposicao', 'feira', 'espetaculo', 'oficina'));
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
                WHERE conname = 'ck_cultura_eventos_status'
                  AND conrelid = 'cultura_eventos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_eventos_culturais
                ADD CONSTRAINT ck_cultura_eventos_status
                CHECK (status IN ('rascunho', 'publicado', 'em_andamento', 'concluido', 'cancelado'));
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
                WHERE conname = 'ck_cultura_eventos_periodo_ingresso'
                  AND conrelid = 'cultura_eventos_culturais'::regclass
            ) THEN
                ALTER TABLE cultura_eventos_culturais
                ADD CONSTRAINT ck_cultura_eventos_periodo_ingresso
                CHECK (
                    data_fim >= data_inicio
                    AND (valor_ingresso IS NULL OR valor_ingresso >= 0)
                    AND (publico_estimado IS NULL OR publico_estimado >= 0)
                    AND (entrada_gratuita = TRUE OR valor_ingresso IS NOT NULL)
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_codigo ON cultura_eventos_culturais (codigo_evento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_nome ON cultura_eventos_culturais (nome)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_tipo ON cultura_eventos_culturais (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_municipio ON cultura_eventos_culturais (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_provincia ON cultura_eventos_culturais (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_data_inicio ON cultura_eventos_culturais (data_inicio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_data_fim ON cultura_eventos_culturais (data_fim)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_status ON cultura_eventos_culturais (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_realizador_id ON cultura_eventos_culturais (realizador_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_atracao_turistica_id ON cultura_eventos_culturais (atracao_turistica_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_instituicao_educacional_id ON cultura_eventos_culturais (instituicao_educacional_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_cultura_eventos_ativo ON cultura_eventos_culturais (ativo)"
    )


def upgrade() -> None:
    _create_artistas_table()
    _create_bens_culturais_table()
    _create_eventos_culturais_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_instituicao_educacional_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_atracao_turistica_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_realizador_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_status")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_data_fim")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_data_inicio")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_provincia")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_municipio")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_tipo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_nome")
    op.execute("DROP INDEX IF EXISTS ix_cultura_eventos_codigo")
    op.execute("DROP TABLE IF EXISTS cultura_eventos_culturais")

    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_tombamento_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_status_tombamento")
    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_provincia")
    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_municipio")
    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_tipo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_nome")
    op.execute("DROP INDEX IF EXISTS ix_cultura_bens_registro")
    op.execute("DROP TABLE IF EXISTS cultura_bens_culturais")

    op.execute("DROP INDEX IF EXISTS ix_cultura_artistas_ativo")
    op.execute("DROP INDEX IF EXISTS ix_cultura_artistas_provincia")
    op.execute("DROP INDEX IF EXISTS ix_cultura_artistas_municipio")
    op.execute("DROP INDEX IF EXISTS ix_cultura_artistas_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_cultura_artistas_nome")
    op.execute("DROP INDEX IF EXISTS ix_cultura_artistas_registro")
    op.execute("DROP TABLE IF EXISTS cultura_artistas")
