"""create desporto slice2 tables for clubes e jogos

Revision ID: 20260302_020_desporto_slice2_clubes_jogos
Revises: 20260302_019_desporto_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_020_desporto_slice2_clubes_jogos"
down_revision = "20260302_019_desporto_foundation"
branch_labels = None
depends_on = None


def _create_clubes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS desporto_clubes (
            id UUID PRIMARY KEY,
            codigo_clube VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            sigla VARCHAR(10) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            modalidade_principal VARCHAR(30) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            data_cadastro DATE NOT NULL,
            data_fundacao DATE,
            codigo_obra_instalacao VARCHAR(50),
            instituicao_educacional_id UUID,
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
                WHERE conname = 'ck_desporto_clubes_nome_sigla'
                  AND conrelid = 'desporto_clubes'::regclass
            ) THEN
                ALTER TABLE desporto_clubes
                ADD CONSTRAINT ck_desporto_clubes_nome_sigla
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND char_length(trim(sigla)) BETWEEN 2 AND 10
                    AND (data_fundacao IS NULL OR data_fundacao <= CURRENT_DATE)
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
                WHERE conname = 'ck_desporto_clubes_tipo_modalidade'
                  AND conrelid = 'desporto_clubes'::regclass
            ) THEN
                ALTER TABLE desporto_clubes
                ADD CONSTRAINT ck_desporto_clubes_tipo_modalidade
                CHECK (
                    tipo IN ('profissional', 'escolar', 'universitario', 'comunitario', 'federado')
                    AND modalidade_principal IN (
                        'futebol', 'futsal', 'andebol', 'basquetebol', 'voleibol',
                        'atletismo', 'natacao', 'ginastica', 'judo', 'karate',
                        'boxe', 'tenis', 'ciclismo', 'desporto_adaptado'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_clubes_codigo ON desporto_clubes (codigo_clube)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_clubes_nome ON desporto_clubes (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_clubes_sigla ON desporto_clubes (sigla)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_clubes_tipo ON desporto_clubes (tipo)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_clubes_modalidade_principal ON desporto_clubes (modalidade_principal)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_clubes_municipio ON desporto_clubes (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_clubes_provincia ON desporto_clubes (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_clubes_codigo_obra_instalacao ON desporto_clubes (codigo_obra_instalacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_clubes_instituicao_educacional_id ON desporto_clubes (instituicao_educacional_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_clubes_ativo ON desporto_clubes (ativo)")


def _create_jogos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS desporto_jogos (
            id UUID PRIMARY KEY,
            codigo_jogo VARCHAR(50) NOT NULL UNIQUE,
            competicao_id UUID NOT NULL,
            clube_casa_id UUID NOT NULL,
            clube_fora_id UUID NOT NULL,
            data_jogo DATE NOT NULL,
            local VARCHAR(200) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            data_cadastro DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            placar_casa INTEGER,
            placar_fora INTEGER,
            codigo_obra_instalacao VARCHAR(50),
            atracao_turistica_id UUID,
            publico_estimado INTEGER,
            publico_presente INTEGER,
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
                WHERE conname = 'ck_desporto_jogos_clubes_placar_publico'
                  AND conrelid = 'desporto_jogos'::regclass
            ) THEN
                ALTER TABLE desporto_jogos
                ADD CONSTRAINT ck_desporto_jogos_clubes_placar_publico
                CHECK (
                    clube_casa_id <> clube_fora_id
                    AND char_length(trim(local)) >= 3
                    AND (placar_casa IS NULL OR placar_casa >= 0)
                    AND (placar_fora IS NULL OR placar_fora >= 0)
                    AND (publico_estimado IS NULL OR publico_estimado >= 0)
                    AND (publico_presente IS NULL OR publico_presente >= 0)
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
                WHERE conname = 'ck_desporto_jogos_status'
                  AND conrelid = 'desporto_jogos'::regclass
            ) THEN
                ALTER TABLE desporto_jogos
                ADD CONSTRAINT ck_desporto_jogos_status
                CHECK (status IN ('agendado', 'em_andamento', 'encerrado', 'cancelado'));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_codigo ON desporto_jogos (codigo_jogo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_competicao_id ON desporto_jogos (competicao_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_clube_casa_id ON desporto_jogos (clube_casa_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_clube_fora_id ON desporto_jogos (clube_fora_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_data_jogo ON desporto_jogos (data_jogo)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_jogos_status ON desporto_jogos (status)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_municipio ON desporto_jogos (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_provincia ON desporto_jogos (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_codigo_obra_instalacao ON desporto_jogos (codigo_obra_instalacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_jogos_atracao_turistica_id ON desporto_jogos (atracao_turistica_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_jogos_ativo ON desporto_jogos (ativo)")


def upgrade() -> None:
    _create_clubes_table()
    _create_jogos_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_ativo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_atracao_turistica_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_codigo_obra_instalacao")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_provincia")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_municipio")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_status")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_data_jogo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_clube_fora_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_clube_casa_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_competicao_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_jogos_codigo")
    op.execute("DROP TABLE IF EXISTS desporto_jogos")

    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_ativo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_instituicao_educacional_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_codigo_obra_instalacao")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_provincia")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_municipio")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_modalidade_principal")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_tipo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_sigla")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_nome")
    op.execute("DROP INDEX IF EXISTS ix_desporto_clubes_codigo")
    op.execute("DROP TABLE IF EXISTS desporto_clubes")
