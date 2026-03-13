"""create telecomunicacoes infraestrutura, outorgas e espectro tables

Revision ID: 20260302_024_telecomunicacoes_infra_espectro_outorgas
Revises: 20260302_023_telecomunicacoes_foundation
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260302_024_telecomunicacoes_infra_espectro_outorgas"
down_revision = "20260302_023_telecomunicacoes_foundation"
branch_labels = None
depends_on = None


def _create_infraestruturas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_infraestruturas (
            id UUID PRIMARY KEY,
            codigo_infra VARCHAR(50) NOT NULL UNIQUE,
            operadora_id UUID NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            identificador VARCHAR(120) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            data_implantacao DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            latitude NUMERIC(10, 7),
            longitude NUMERIC(10, 7),
            capacidade VARCHAR(120),
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
                WHERE conname = 'ck_telecom_infraestruturas_tipo_status'
                  AND conrelid = 'telecom_infraestruturas'::regclass
            ) THEN
                ALTER TABLE telecom_infraestruturas
                ADD CONSTRAINT ck_telecom_infraestruturas_tipo_status
                CHECK (
                    tipo IN (
                        'torre',
                        'antena',
                        'erb',
                        'datacenter',
                        'backbone',
                        'fibra_optica',
                        'cabo_submarino',
                        'pop',
                        'estacao_terrena'
                    )
                    AND status IN ('planeada', 'ativa', 'manutencao', 'desativada')
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
                WHERE conname = 'ck_telecom_infraestruturas_campos_basicos'
                  AND conrelid = 'telecom_infraestruturas'::regclass
            ) THEN
                ALTER TABLE telecom_infraestruturas
                ADD CONSTRAINT ck_telecom_infraestruturas_campos_basicos
                CHECK (
                    char_length(trim(codigo_infra)) >= 10
                    AND char_length(trim(identificador)) >= 3
                    AND data_implantacao <= CURRENT_DATE
                    AND (latitude IS NULL OR (latitude BETWEEN -90 AND 90))
                    AND (longitude IS NULL OR (longitude BETWEEN -180 AND 180))
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_codigo_infra ON telecom_infraestruturas (codigo_infra)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_operadora_id ON telecom_infraestruturas (operadora_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_tipo ON telecom_infraestruturas (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_identificador ON telecom_infraestruturas (identificador)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_municipio ON telecom_infraestruturas (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_provincia ON telecom_infraestruturas (provincia)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_status ON telecom_infraestruturas (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_infraestruturas_ativo ON telecom_infraestruturas (ativo)")


def _create_outorgas_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_outorgas_espectro (
            id UUID PRIMARY KEY,
            numero_outorga VARCHAR(50) NOT NULL UNIQUE,
            operadora_id UUID NOT NULL,
            tipo_outorga VARCHAR(30) NOT NULL,
            faixa_inicio_mhz NUMERIC(12, 3) NOT NULL,
            faixa_fim_mhz NUMERIC(12, 3) NOT NULL,
            data_outorga DATE NOT NULL,
            data_validade DATE,
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
                WHERE conname = 'ck_telecom_outorgas_tipo_status'
                  AND conrelid = 'telecom_outorgas_espectro'::regclass
            ) THEN
                ALTER TABLE telecom_outorgas_espectro
                ADD CONSTRAINT ck_telecom_outorgas_tipo_status
                CHECK (
                    tipo_outorga IN ('concessao', 'permissao', 'autorizacao', 'licenca')
                    AND status IN ('requerida', 'em_analise', 'deferida', 'indeferida', 'vencida', 'renovada', 'cancelada')
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
                WHERE conname = 'ck_telecom_outorgas_faixa_periodo'
                  AND conrelid = 'telecom_outorgas_espectro'::regclass
            ) THEN
                ALTER TABLE telecom_outorgas_espectro
                ADD CONSTRAINT ck_telecom_outorgas_faixa_periodo
                CHECK (
                    faixa_inicio_mhz >= 0
                    AND faixa_fim_mhz > faixa_inicio_mhz
                    AND (data_validade IS NULL OR data_validade >= data_outorga)
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_outorgas_numero_outorga ON telecom_outorgas_espectro (numero_outorga)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_outorgas_operadora_id ON telecom_outorgas_espectro (operadora_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_outorgas_tipo_outorga ON telecom_outorgas_espectro (tipo_outorga)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_outorgas_status ON telecom_outorgas_espectro (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_outorgas_ativo ON telecom_outorgas_espectro (ativo)")


def _create_espectro_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_espectro (
            id UUID PRIMARY KEY,
            codigo_espectro VARCHAR(50) NOT NULL UNIQUE,
            tipo VARCHAR(30) NOT NULL,
            frequencia_inicial_mhz NUMERIC(12, 3) NOT NULL,
            frequencia_final_mhz NUMERIC(12, 3) NOT NULL,
            largura_banda_mhz NUMERIC(12, 3) NOT NULL,
            servico_principal VARCHAR(40) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            status VARCHAR(30) NOT NULL,
            outorga_id UUID,
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
                WHERE conname = 'ck_telecom_espectro_tipo_status_servico'
                  AND conrelid = 'telecom_espectro'::regclass
            ) THEN
                ALTER TABLE telecom_espectro
                ADD CONSTRAINT ck_telecom_espectro_tipo_status_servico
                CHECK (
                    tipo IN ('banda_larga', 'banda_estreita', 'radio_difusao', 'tv_difusao', 'satelite')
                    AND status IN ('disponivel', 'outorgado', 'interferido', 'reserva')
                    AND servico_principal IN (
                        'telefonia_fixa',
                        'telefonia_movel',
                        'internet_fixa',
                        'internet_movel',
                        'tv_assinatura',
                        'radio',
                        'comunicacao_dados'
                    )
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
                WHERE conname = 'ck_telecom_espectro_frequencias'
                  AND conrelid = 'telecom_espectro'::regclass
            ) THEN
                ALTER TABLE telecom_espectro
                ADD CONSTRAINT ck_telecom_espectro_frequencias
                CHECK (
                    frequencia_inicial_mhz >= 0
                    AND frequencia_final_mhz > frequencia_inicial_mhz
                    AND largura_banda_mhz = (frequencia_final_mhz - frequencia_inicial_mhz)
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_codigo_espectro ON telecom_espectro (codigo_espectro)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_tipo ON telecom_espectro (tipo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_servico_principal ON telecom_espectro (servico_principal)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_municipio ON telecom_espectro (municipio)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_provincia ON telecom_espectro (provincia)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_status ON telecom_espectro (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_outorga_id ON telecom_espectro (outorga_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_espectro_ativo ON telecom_espectro (ativo)")


def upgrade() -> None:
    _create_infraestruturas_table()
    _create_outorgas_table()
    _create_espectro_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_outorga_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_provincia")
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_municipio")
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_servico_principal")
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_tipo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_espectro_codigo_espectro")
    op.execute("DROP TABLE IF EXISTS telecom_espectro")

    op.execute("DROP INDEX IF EXISTS ix_telecom_outorgas_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_outorgas_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_outorgas_tipo_outorga")
    op.execute("DROP INDEX IF EXISTS ix_telecom_outorgas_operadora_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_outorgas_numero_outorga")
    op.execute("DROP TABLE IF EXISTS telecom_outorgas_espectro")

    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_provincia")
    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_municipio")
    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_identificador")
    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_tipo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_operadora_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_infraestruturas_codigo_infra")
    op.execute("DROP TABLE IF EXISTS telecom_infraestruturas")
