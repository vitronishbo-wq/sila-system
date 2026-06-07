"""create telecomunicacoes qualidade, sla e indicadores tables

Revision ID: 20260302_025_telecomunicacoes_qualidade_sla_indicadores
Revises: 20260302_024_telecomunicacoes_infra_espectro_outorgas
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_025_telecomunicacoes_qualidade_sla_indicadores"
down_revision = "20260302_024_telecomunicacoes_infra_espectro_outorgas"
branch_labels = None
depends_on = None


def _create_slas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_slas (
            id UUID PRIMARY KEY,
            codigo_sla VARCHAR(50) NOT NULL UNIQUE,
            operadora_id UUID NOT NULL,
            nome VARCHAR(200) NOT NULL,
            servico VARCHAR(40) NOT NULL,
            disponibilidade_min_percentual NUMERIC(5, 2) NOT NULL,
            latencia_max_ms NUMERIC(10, 2) NOT NULL,
            jitter_max_ms NUMERIC(10, 2) NOT NULL,
            perda_pacotes_max_percentual NUMERIC(5, 2) NOT NULL,
            velocidade_download_min_mbps NUMERIC(10, 2) NOT NULL,
            velocidade_upload_min_mbps NUMERIC(10, 2) NOT NULL,
            data_inicio DATE NOT NULL,
            data_fim DATE,
            status VARCHAR(30) NOT NULL,
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
                WHERE conname = 'ck_telecom_slas_servico_status'
                  AND conrelid = 'telecom_slas'::regclass
            ) THEN
                ALTER TABLE telecom_slas
                ADD CONSTRAINT ck_telecom_slas_servico_status
                CHECK (
                    servico IN (
                        'telefonia_fixa',
                        'telefonia_movel',
                        'internet_fixa',
                        'internet_movel',
                        'tv_assinatura',
                        'radio',
                        'comunicacao_dados'
                    )
                    AND status IN ('ativo', 'suspenso', 'encerrado')
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
                WHERE conname = 'ck_telecom_slas_parametros'
                  AND conrelid = 'telecom_slas'::regclass
            ) THEN
                ALTER TABLE telecom_slas
                ADD CONSTRAINT ck_telecom_slas_parametros
                CHECK (
                    char_length(trim(nome)) >= 3
                    AND disponibilidade_min_percentual BETWEEN 0 AND 100
                    AND latencia_max_ms > 0
                    AND jitter_max_ms >= 0
                    AND perda_pacotes_max_percentual BETWEEN 0 AND 100
                    AND velocidade_download_min_mbps >= 0
                    AND velocidade_upload_min_mbps >= 0
                    AND (data_fim IS NULL OR data_fim >= data_inicio)
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_slas_codigo_sla ON telecom_slas (codigo_sla)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_slas_operadora_id ON telecom_slas (operadora_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_slas_servico ON telecom_slas (servico)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_slas_status ON telecom_slas (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_slas_ativo ON telecom_slas (ativo)")


def _create_qualidade_servico_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_qualidade_servico (
            id UUID PRIMARY KEY,
            codigo_medicao VARCHAR(50) NOT NULL UNIQUE,
            operadora_id UUID NOT NULL,
            assinante_id UUID,
            sla_id UUID,
            servico VARCHAR(40) NOT NULL,
            data_medicao DATE NOT NULL,
            disponibilidade_percentual NUMERIC(5, 2) NOT NULL,
            latencia_ms NUMERIC(10, 2) NOT NULL,
            jitter_ms NUMERIC(10, 2) NOT NULL,
            perda_pacotes_percentual NUMERIC(5, 2) NOT NULL,
            velocidade_download_mbps NUMERIC(10, 2) NOT NULL,
            velocidade_upload_mbps NUMERIC(10, 2) NOT NULL,
            status VARCHAR(30) NOT NULL,
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
                WHERE conname = 'ck_telecom_qualidade_servico_enum'
                  AND conrelid = 'telecom_qualidade_servico'::regclass
            ) THEN
                ALTER TABLE telecom_qualidade_servico
                ADD CONSTRAINT ck_telecom_qualidade_servico_enum
                CHECK (
                    servico IN (
                        'telefonia_fixa',
                        'telefonia_movel',
                        'internet_fixa',
                        'internet_movel',
                        'tv_assinatura',
                        'radio',
                        'comunicacao_dados'
                    )
                    AND status IN ('conforme', 'alerta', 'critico')
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
                WHERE conname = 'ck_telecom_qualidade_servico_metricas'
                  AND conrelid = 'telecom_qualidade_servico'::regclass
            ) THEN
                ALTER TABLE telecom_qualidade_servico
                ADD CONSTRAINT ck_telecom_qualidade_servico_metricas
                CHECK (
                    disponibilidade_percentual BETWEEN 0 AND 100
                    AND latencia_ms >= 0
                    AND jitter_ms >= 0
                    AND perda_pacotes_percentual BETWEEN 0 AND 100
                    AND velocidade_download_mbps >= 0
                    AND velocidade_upload_mbps >= 0
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_codigo_medicao ON telecom_qualidade_servico (codigo_medicao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_operadora_id ON telecom_qualidade_servico (operadora_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_assinante_id ON telecom_qualidade_servico (assinante_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_sla_id ON telecom_qualidade_servico (sla_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_servico ON telecom_qualidade_servico (servico)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_data_medicao ON telecom_qualidade_servico (data_medicao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_status ON telecom_qualidade_servico (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_qualidade_servico_ativo ON telecom_qualidade_servico (ativo)"
    )


def _create_indicadores_qualidade_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_indicadores_qualidade (
            id UUID PRIMARY KEY,
            codigo_indicador VARCHAR(50) NOT NULL UNIQUE,
            operadora_id UUID NOT NULL,
            referencia_ano INTEGER NOT NULL,
            referencia_mes INTEGER NOT NULL,
            total_medicoes INTEGER NOT NULL,
            disponibilidade_media_percentual NUMERIC(5, 2) NOT NULL,
            latencia_media_ms NUMERIC(10, 2) NOT NULL,
            jitter_medio_ms NUMERIC(10, 2) NOT NULL,
            perda_pacotes_media_percentual NUMERIC(5, 2) NOT NULL,
            conformidade_percentual NUMERIC(5, 2) NOT NULL,
            data_calculo DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
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
                WHERE conname = 'ck_telecom_indicadores_qualidade_status'
                  AND conrelid = 'telecom_indicadores_qualidade'::regclass
            ) THEN
                ALTER TABLE telecom_indicadores_qualidade
                ADD CONSTRAINT ck_telecom_indicadores_qualidade_status
                CHECK (status IN ('bom', 'regular', 'critico'));
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
                WHERE conname = 'ck_telecom_indicadores_qualidade_campos'
                  AND conrelid = 'telecom_indicadores_qualidade'::regclass
            ) THEN
                ALTER TABLE telecom_indicadores_qualidade
                ADD CONSTRAINT ck_telecom_indicadores_qualidade_campos
                CHECK (
                    referencia_ano >= 2000
                    AND referencia_mes BETWEEN 1 AND 12
                    AND total_medicoes > 0
                    AND disponibilidade_media_percentual BETWEEN 0 AND 100
                    AND perda_pacotes_media_percentual BETWEEN 0 AND 100
                    AND conformidade_percentual BETWEEN 0 AND 100
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_indicadores_qualidade_codigo_indicador ON telecom_indicadores_qualidade (codigo_indicador)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_indicadores_qualidade_operadora_id ON telecom_indicadores_qualidade (operadora_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_indicadores_qualidade_referencia_ano ON telecom_indicadores_qualidade (referencia_ano)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_indicadores_qualidade_referencia_mes ON telecom_indicadores_qualidade (referencia_mes)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_indicadores_qualidade_status ON telecom_indicadores_qualidade (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_indicadores_qualidade_ativo ON telecom_indicadores_qualidade (ativo)"
    )
    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS uq_telecom_indicadores_operadora_periodo
        ON telecom_indicadores_qualidade (operadora_id, referencia_ano, referencia_mes)
        """
    )


def upgrade() -> None:
    _create_slas_table()
    _create_qualidade_servico_table()
    _create_indicadores_qualidade_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_telecom_indicadores_operadora_periodo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_indicadores_qualidade_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_indicadores_qualidade_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_indicadores_qualidade_referencia_mes")
    op.execute("DROP INDEX IF EXISTS ix_telecom_indicadores_qualidade_referencia_ano")
    op.execute("DROP INDEX IF EXISTS ix_telecom_indicadores_qualidade_operadora_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_indicadores_qualidade_codigo_indicador")
    op.execute("DROP TABLE IF EXISTS telecom_indicadores_qualidade")

    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_data_medicao")
    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_servico")
    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_sla_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_assinante_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_operadora_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_qualidade_servico_codigo_medicao")
    op.execute("DROP TABLE IF EXISTS telecom_qualidade_servico")

    op.execute("DROP INDEX IF EXISTS ix_telecom_slas_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_slas_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_slas_servico")
    op.execute("DROP INDEX IF EXISTS ix_telecom_slas_operadora_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_slas_codigo_sla")
    op.execute("DROP TABLE IF EXISTS telecom_slas")
