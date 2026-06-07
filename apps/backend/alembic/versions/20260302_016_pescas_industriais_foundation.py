"""create pescas_industriais core tables

Revision ID: 20260302_016_pescas_industriais_foundation
Revises: 20260301_015_florestas_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_016_pescas_industriais_foundation"
down_revision = "20260301_015_florestas_foundation"
branch_labels = None
depends_on = None


def _create_unidades_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_industriais_unidades (
            id UUID PRIMARY KEY,
            cnpj VARCHAR(18) NOT NULL UNIQUE,
            razao_social VARCHAR(200) NOT NULL,
            nome_fantasia VARCHAR(200),
            inscricao_estadual VARCHAR(20),
            inscricao_municipal VARCHAR(20),
            tipo_processamento TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
            classificacao VARCHAR(30) NOT NULL,
            capacidade_kg_dia NUMERIC(15, 2) NOT NULL,
            area_total_m2 NUMERIC(15, 2) NOT NULL,
            area_producao_m2 NUMERIC(15, 2) NOT NULL,
            area_armazenagem_m2 NUMERIC(15, 2) NOT NULL,
            capacidade_frigorifica_m3 NUMERIC(15, 2),
            temperatura_media NUMERIC(5, 2),
            numero_funcionarios INTEGER NOT NULL,
            responsavel_tecnico_id UUID,
            responsavel_tecnico_registro VARCHAR(50),
            endereco VARCHAR(200) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(50) NOT NULL,
            coordenadas_lat NUMERIC(10, 7),
            coordenadas_long NUMERIC(10, 7),
            armador_id UUID,
            data_inauguracao DATE NOT NULL,
            licenca_operacao_id UUID,
            alvara_sanitario_id UUID,
            certificacoes TEXT[],
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
                WHERE conname = 'ck_pescas_industriais_unidades_classificacao'
                  AND conrelid = 'pescas_industriais_unidades'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_unidades
                ADD CONSTRAINT ck_pescas_industriais_unidades_classificacao
                CHECK (classificacao IN ('tipo_a', 'tipo_b', 'tipo_c'));
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
                WHERE conname = 'ck_pescas_industriais_unidades_areas_capacidade'
                  AND conrelid = 'pescas_industriais_unidades'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_unidades
                ADD CONSTRAINT ck_pescas_industriais_unidades_areas_capacidade
                CHECK (
                    capacidade_kg_dia > 0
                    AND area_total_m2 > 0
                    AND area_producao_m2 > 0
                    AND area_armazenagem_m2 > 0
                    AND numero_funcionarios >= 0
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_unidades_cnpj ON pescas_industriais_unidades (cnpj)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_unidades_classificacao ON pescas_industriais_unidades (classificacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_unidades_municipio ON pescas_industriais_unidades (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_unidades_armador_id ON pescas_industriais_unidades (armador_id)"
    )


def _create_produtos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_industriais_produtos_processados (
            id UUID PRIMARY KEY,
            codigo_produto VARCHAR(50) NOT NULL UNIQUE,
            unidade_processamento_id UUID NOT NULL,
            nome_comercial VARCHAR(200) NOT NULL,
            tipo_produto VARCHAR(30) NOT NULL,
            tipo_processamento VARCHAR(30) NOT NULL,
            peso_liquido_kg NUMERIC(12, 3) NOT NULL,
            rendimento_percentual NUMERIC(5, 2) NOT NULL,
            mercado_destino VARCHAR(20) NOT NULL,
            data_registro DATE NOT NULL,
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
                WHERE conname = 'ck_pescas_industriais_produtos_tipo_produto'
                  AND conrelid = 'pescas_industriais_produtos_processados'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_produtos_processados
                ADD CONSTRAINT ck_pescas_industriais_produtos_tipo_produto
                CHECK (tipo_produto IN ('filete', 'posta', 'conserva', 'enlatado', 'congelado', 'seco', 'salgado', 'defumado', 'farinha', 'oleo', 'subproduto'));
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
                WHERE conname = 'ck_pescas_industriais_produtos_tipo_processamento'
                  AND conrelid = 'pescas_industriais_produtos_processados'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_produtos_processados
                ADD CONSTRAINT ck_pescas_industriais_produtos_tipo_processamento
                CHECK (tipo_processamento IN ('filetagem', 'conserva', 'enlatado', 'congelado', 'seco', 'salgado', 'defumado', 'farinha', 'oleo'));
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
                WHERE conname = 'ck_pescas_industriais_produtos_mercado_destino'
                  AND conrelid = 'pescas_industriais_produtos_processados'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_produtos_processados
                ADD CONSTRAINT ck_pescas_industriais_produtos_mercado_destino
                CHECK (mercado_destino IN ('interno', 'exportacao'));
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
                WHERE conname = 'ck_pescas_industriais_produtos_metricas'
                  AND conrelid = 'pescas_industriais_produtos_processados'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_produtos_processados
                ADD CONSTRAINT ck_pescas_industriais_produtos_metricas
                CHECK (peso_liquido_kg > 0 AND rendimento_percentual > 0 AND rendimento_percentual <= 100);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_produtos_codigo ON pescas_industriais_produtos_processados (codigo_produto)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_produtos_unidade_id ON pescas_industriais_produtos_processados (unidade_processamento_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_produtos_tipo ON pescas_industriais_produtos_processados (tipo_produto)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_produtos_processamento ON pescas_industriais_produtos_processados (tipo_processamento)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_produtos_mercado ON pescas_industriais_produtos_processados (mercado_destino)"
    )


def _create_lotes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_industriais_lotes_producao (
            id UUID PRIMARY KEY,
            codigo_lote VARCHAR(50) NOT NULL UNIQUE,
            unidade_processamento_id UUID NOT NULL,
            produto_processado_id UUID NOT NULL,
            data_producao DATE NOT NULL,
            quantidade_kg NUMERIC(15, 3) NOT NULL,
            status VARCHAR(30) NOT NULL,
            destino_mercado VARCHAR(20) NOT NULL,
            data_validade DATE,
            turno VARCHAR(20),
            temperatura_armazenamento_c NUMERIC(6, 2),
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
                WHERE conname = 'ck_pescas_industriais_lotes_status'
                  AND conrelid = 'pescas_industriais_lotes_producao'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_lotes_producao
                ADD CONSTRAINT ck_pescas_industriais_lotes_status
                CHECK (status IN ('aberto', 'em_processamento', 'concluido', 'bloqueado', 'descartado'));
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
                WHERE conname = 'ck_pescas_industriais_lotes_destino_mercado'
                  AND conrelid = 'pescas_industriais_lotes_producao'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_lotes_producao
                ADD CONSTRAINT ck_pescas_industriais_lotes_destino_mercado
                CHECK (destino_mercado IN ('interno', 'exportacao'));
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
                WHERE conname = 'ck_pescas_industriais_lotes_quantidade_validade'
                  AND conrelid = 'pescas_industriais_lotes_producao'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_lotes_producao
                ADD CONSTRAINT ck_pescas_industriais_lotes_quantidade_validade
                CHECK (quantidade_kg > 0 AND (data_validade IS NULL OR data_validade >= data_producao));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_lotes_codigo ON pescas_industriais_lotes_producao (codigo_lote)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_lotes_unidade_id ON pescas_industriais_lotes_producao (unidade_processamento_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_lotes_produto_id ON pescas_industriais_lotes_producao (produto_processado_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_lotes_data_producao ON pescas_industriais_lotes_producao (data_producao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_lotes_status ON pescas_industriais_lotes_producao (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_lotes_destino_mercado ON pescas_industriais_lotes_producao (destino_mercado)"
    )


def _create_inspecoes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS pescas_industriais_inspecoes (
            id UUID PRIMARY KEY,
            codigo_inspecao VARCHAR(50) NOT NULL UNIQUE,
            unidade_processamento_id UUID NOT NULL,
            data_agendada DATE NOT NULL,
            selo_inspecao VARCHAR(10) NOT NULL,
            status VARCHAR(30) NOT NULL,
            fiscal_id UUID,
            lote_producao_id UUID,
            data_realizacao DATE,
            pontuacao INTEGER,
            inconformidades TEXT[],
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
                WHERE conname = 'ck_pescas_industriais_inspecoes_selo'
                  AND conrelid = 'pescas_industriais_inspecoes'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_inspecoes
                ADD CONSTRAINT ck_pescas_industriais_inspecoes_selo
                CHECK (selo_inspecao IN ('sif', 'sie', 'sim'));
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
                WHERE conname = 'ck_pescas_industriais_inspecoes_status'
                  AND conrelid = 'pescas_industriais_inspecoes'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_inspecoes
                ADD CONSTRAINT ck_pescas_industriais_inspecoes_status
                CHECK (status IN ('agendada', 'em_andamento', 'aprovada', 'reprovada', 'pendencia', 'interditada'));
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
                WHERE conname = 'ck_pescas_industriais_inspecoes_pontuacao'
                  AND conrelid = 'pescas_industriais_inspecoes'::regclass
            ) THEN
                ALTER TABLE pescas_industriais_inspecoes
                ADD CONSTRAINT ck_pescas_industriais_inspecoes_pontuacao
                CHECK (pontuacao IS NULL OR (pontuacao >= 0 AND pontuacao <= 100));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_inspecoes_codigo ON pescas_industriais_inspecoes (codigo_inspecao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_inspecoes_unidade_id ON pescas_industriais_inspecoes (unidade_processamento_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_inspecoes_data_agendada ON pescas_industriais_inspecoes (data_agendada)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_inspecoes_selo ON pescas_industriais_inspecoes (selo_inspecao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_inspecoes_status ON pescas_industriais_inspecoes (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pescas_industriais_inspecoes_lote_id ON pescas_industriais_inspecoes (lote_producao_id)"
    )


def upgrade() -> None:
    _create_unidades_table()
    _create_produtos_table()
    _create_lotes_table()
    _create_inspecoes_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_inspecoes_lote_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_inspecoes_status")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_inspecoes_selo")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_inspecoes_data_agendada")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_inspecoes_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_inspecoes_codigo")
    op.execute("DROP TABLE IF EXISTS pescas_industriais_inspecoes")

    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_lotes_destino_mercado")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_lotes_status")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_lotes_data_producao")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_lotes_produto_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_lotes_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_lotes_codigo")
    op.execute("DROP TABLE IF EXISTS pescas_industriais_lotes_producao")

    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_produtos_mercado")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_produtos_processamento")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_produtos_tipo")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_produtos_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_produtos_codigo")
    op.execute("DROP TABLE IF EXISTS pescas_industriais_produtos_processados")

    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_unidades_armador_id")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_unidades_municipio")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_unidades_classificacao")
    op.execute("DROP INDEX IF EXISTS ix_pescas_industriais_unidades_cnpj")
    op.execute("DROP TABLE IF EXISTS pescas_industriais_unidades")
