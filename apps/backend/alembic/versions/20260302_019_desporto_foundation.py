"""create desporto core tables

Revision ID: 20260302_019_desporto_foundation
Revises: 20260302_018_cultura_slice2_grupos_patrimonio_imaterial
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_019_desporto_foundation"
down_revision = "20260302_018_cultura_slice2_grupos_patrimonio_imaterial"
branch_labels = None
depends_on = None


def _create_atletas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS desporto_atletas (
            id UUID PRIMARY KEY,
            numero_registro VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            data_nascimento DATE NOT NULL,
            naturalidade VARCHAR(100) NOT NULL,
            nacionalidade VARCHAR(50) NOT NULL DEFAULT 'Angolana',
            tipo VARCHAR(30) NOT NULL,
            modalidades TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
            status VARCHAR(30) NOT NULL,
            posicoes TEXT[],
            pe_preferencial VARCHAR(20),
            altura_cm INTEGER,
            peso_kg NUMERIC(6, 2),
            clube_atual_id UUID,
            numero_camisola INTEGER,
            citizen_id UUID,
            ultimo_exame_id UUID,
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
                WHERE conname = 'ck_desporto_atletas_nome_data'
                  AND conrelid = 'desporto_atletas'::regclass
            ) THEN
                ALTER TABLE desporto_atletas
                ADD CONSTRAINT ck_desporto_atletas_nome_data
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
                WHERE conname = 'ck_desporto_atletas_tipo_status'
                  AND conrelid = 'desporto_atletas'::regclass
            ) THEN
                ALTER TABLE desporto_atletas
                ADD CONSTRAINT ck_desporto_atletas_tipo_status
                CHECK (
                    tipo IN ('amador', 'profissional', 'semiprofissional', 'de_base', 'master', 'paralimpico')
                    AND status IN ('ativo', 'lesionado', 'suspenso', 'aposentado', 'transferencia', 'emprestimo')
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
                WHERE conname = 'ck_desporto_atletas_modalidades_fisico'
                  AND conrelid = 'desporto_atletas'::regclass
            ) THEN
                ALTER TABLE desporto_atletas
                ADD CONSTRAINT ck_desporto_atletas_modalidades_fisico
                CHECK (
                    array_length(modalidades, 1) >= 1
                    AND (altura_cm IS NULL OR altura_cm > 0)
                    AND (peso_kg IS NULL OR peso_kg > 0)
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_atletas_numero_registro ON desporto_atletas (numero_registro)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_atletas_nome ON desporto_atletas (nome)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_atletas_tipo ON desporto_atletas (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_atletas_status ON desporto_atletas (status)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_atletas_clube_atual_id ON desporto_atletas (clube_atual_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_atletas_citizen_id ON desporto_atletas (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_atletas_ultimo_exame_id ON desporto_atletas (ultimo_exame_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_desporto_atletas_ativo ON desporto_atletas (ativo)")


def _create_competicoes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS desporto_competicoes (
            id UUID PRIMARY KEY,
            codigo_competicao VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            modalidade VARCHAR(30) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            organizador_id UUID NOT NULL,
            status VARCHAR(30) NOT NULL,
            codigo_obra_instalacao VARCHAR(50),
            atracao_turistica_id UUID,
            instituicao_educacional_id UUID,
            premiacao_total NUMERIC(14, 2),
            inscricoes_abertas BOOLEAN NOT NULL DEFAULT FALSE,
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
                WHERE conname = 'ck_desporto_competicoes_nome_periodo'
                  AND conrelid = 'desporto_competicoes'::regclass
            ) THEN
                ALTER TABLE desporto_competicoes
                ADD CONSTRAINT ck_desporto_competicoes_nome_periodo
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND data_fim >= data_inicio
                    AND (premiacao_total IS NULL OR premiacao_total >= 0)
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
                WHERE conname = 'ck_desporto_competicoes_tipo_modalidade_status'
                  AND conrelid = 'desporto_competicoes'::regclass
            ) THEN
                ALTER TABLE desporto_competicoes
                ADD CONSTRAINT ck_desporto_competicoes_tipo_modalidade_status
                CHECK (
                    tipo IN ('campeonato', 'torneio', 'copa', 'liga', 'prova')
                    AND modalidade IN (
                        'futebol', 'futsal', 'andebol', 'basquetebol', 'voleibol',
                        'atletismo', 'natacao', 'ginastica', 'judo', 'karate',
                        'boxe', 'tenis', 'ciclismo', 'desporto_adaptado'
                    )
                    AND status IN (
                        'planeada', 'inscricoes_abertas', 'em_andamento', 'concluida', 'cancelada'
                    )
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_codigo ON desporto_competicoes (codigo_competicao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_nome ON desporto_competicoes (nome)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_tipo ON desporto_competicoes (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_modalidade ON desporto_competicoes (modalidade)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_data_inicio ON desporto_competicoes (data_inicio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_data_fim ON desporto_competicoes (data_fim)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_municipio ON desporto_competicoes (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_provincia ON desporto_competicoes (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_organizador_id ON desporto_competicoes (organizador_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_status ON desporto_competicoes (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_codigo_obra_instalacao ON desporto_competicoes (codigo_obra_instalacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_atracao_turistica_id ON desporto_competicoes (atracao_turistica_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_instituicao_educacional_id ON desporto_competicoes (instituicao_educacional_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_desporto_competicoes_ativo ON desporto_competicoes (ativo)"
    )


def upgrade() -> None:
    _create_atletas_table()
    _create_competicoes_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_ativo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_instituicao_educacional_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_atracao_turistica_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_codigo_obra_instalacao")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_status")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_organizador_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_provincia")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_municipio")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_data_fim")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_data_inicio")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_modalidade")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_tipo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_nome")
    op.execute("DROP INDEX IF EXISTS ix_desporto_competicoes_codigo")
    op.execute("DROP TABLE IF EXISTS desporto_competicoes")

    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_ativo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_ultimo_exame_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_clube_atual_id")
    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_status")
    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_tipo")
    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_nome")
    op.execute("DROP INDEX IF EXISTS ix_desporto_atletas_numero_registro")
    op.execute("DROP TABLE IF EXISTS desporto_atletas")
