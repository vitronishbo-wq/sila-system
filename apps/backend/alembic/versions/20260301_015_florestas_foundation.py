"""create florestas core tables

Revision ID: 20260301_015_florestas_foundation
Revises: 20260301_014_pescas_foundation
Create Date: 2026-03-01 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260301_015_florestas_foundation"
down_revision = "20260301_014_pescas_foundation"
branch_labels = None
depends_on = None


def _create_operadores_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS florestas_operadores_florestais (
            id UUID PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            nif VARCHAR(32) NOT NULL UNIQUE,
            tipo_operador VARCHAR(30) NOT NULL,
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
                WHERE conname = 'ck_florestas_operadores_tipo'
                  AND conrelid = 'florestas_operadores_florestais'::regclass
            ) THEN
                ALTER TABLE florestas_operadores_florestais
                ADD CONSTRAINT ck_florestas_operadores_tipo
                CHECK (tipo_operador IN ('empresa', 'comunidade', 'cooperativa', 'assentamento', 'concessionario'));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_operadores_nif ON florestas_operadores_florestais (nif)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_operadores_tipo ON florestas_operadores_florestais (tipo_operador)"
    )


def _create_unidades_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS florestas_unidades_manejo (
            id UUID PRIMARY KEY,
            codigo_um VARCHAR(60) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            area_total_ha NUMERIC(15, 2) NOT NULL,
            area_manejo_ha NUMERIC(15, 2) NOT NULL,
            area_preservacao_ha NUMERIC(15, 2) NOT NULL,
            tipo_manejo VARCHAR(30) NOT NULL,
            ciclo_corte VARCHAR(20) NOT NULL,
            operador_id UUID NOT NULL,
            imovel_id UUID NOT NULL,
            plano_manejo_id UUID,
            licenca_id UUID,
            data_criacao DATE NOT NULL,
            data_aprovacao DATE,
            data_validade DATE,
            coordenadas_centroide VARCHAR(120),
            arquivo_shp VARCHAR(500),
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
                WHERE conname = 'ck_florestas_unidades_tipo'
                  AND conrelid = 'florestas_unidades_manejo'::regclass
            ) THEN
                ALTER TABLE florestas_unidades_manejo
                ADD CONSTRAINT ck_florestas_unidades_tipo
                CHECK (tipo_manejo IN ('sustentavel', 'convencional', 'comunitario'));
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
                WHERE conname = 'ck_florestas_unidades_area'
                  AND conrelid = 'florestas_unidades_manejo'::regclass
            ) THEN
                ALTER TABLE florestas_unidades_manejo
                ADD CONSTRAINT ck_florestas_unidades_area
                CHECK (area_total_ha > 0 AND area_manejo_ha >= 0 AND area_preservacao_ha >= 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_unidades_codigo ON florestas_unidades_manejo (codigo_um)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_unidades_tipo ON florestas_unidades_manejo (tipo_manejo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_unidades_operador_id ON florestas_unidades_manejo (operador_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_unidades_imovel_id ON florestas_unidades_manejo (imovel_id)"
    )


def _create_planos_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS florestas_planos_manejo (
            id UUID PRIMARY KEY,
            numero_pmfs VARCHAR(80) NOT NULL UNIQUE,
            unidade_manejo_id UUID NOT NULL,
            responsavel_tecnico_id UUID NOT NULL,
            responsavel_tecnico_registro VARCHAR(80) NOT NULL,
            status VARCHAR(30) NOT NULL,
            data_submissao DATE NOT NULL,
            data_aprovacao DATE,
            data_validade DATE,
            analista_responsavel_id UUID,
            volume_anual_estimado_m3 NUMERIC(15, 2) NOT NULL,
            ciclo_corte_anos INTEGER NOT NULL,
            area_anual_ha NUMERIC(15, 2) NOT NULL,
            parecer_tecnico TEXT,
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
                WHERE conname = 'ck_florestas_planos_status'
                  AND conrelid = 'florestas_planos_manejo'::regclass
            ) THEN
                ALTER TABLE florestas_planos_manejo
                ADD CONSTRAINT ck_florestas_planos_status
                CHECK (status IN ('elaboracao', 'submetido', 'em_analise', 'aprovado', 'reprovado', 'em_execucao', 'concluido', 'suspenso', 'cancelado'));
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_planos_numero ON florestas_planos_manejo (numero_pmfs)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_planos_unidade_id ON florestas_planos_manejo (unidade_manejo_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_planos_status ON florestas_planos_manejo (status)"
    )


def _create_inventarios_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS florestas_inventarios (
            id UUID PRIMARY KEY,
            unidade_manejo_id UUID NOT NULL,
            data_inventario DATE NOT NULL,
            volume_estimado_m3 NUMERIC(15, 2) NOT NULL,
            area_inventariada_ha NUMERIC(15, 2) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'aberto',
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
                WHERE conname = 'ck_florestas_inventarios_volume_area'
                  AND conrelid = 'florestas_inventarios'::regclass
            ) THEN
                ALTER TABLE florestas_inventarios
                ADD CONSTRAINT ck_florestas_inventarios_volume_area
                CHECK (volume_estimado_m3 > 0 AND area_inventariada_ha > 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_inventarios_unidade_id ON florestas_inventarios (unidade_manejo_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_florestas_inventarios_data ON florestas_inventarios (data_inventario)"
    )


def upgrade():
    _create_operadores_table()
    _create_unidades_table()
    _create_planos_table()
    _create_inventarios_table()


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_florestas_inventarios_data")
    op.execute("DROP INDEX IF EXISTS ix_florestas_inventarios_unidade_id")
    op.execute("DROP TABLE IF EXISTS florestas_inventarios")

    op.execute("DROP INDEX IF EXISTS ix_florestas_planos_status")
    op.execute("DROP INDEX IF EXISTS ix_florestas_planos_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_florestas_planos_numero")
    op.execute("DROP TABLE IF EXISTS florestas_planos_manejo")

    op.execute("DROP INDEX IF EXISTS ix_florestas_unidades_imovel_id")
    op.execute("DROP INDEX IF EXISTS ix_florestas_unidades_operador_id")
    op.execute("DROP INDEX IF EXISTS ix_florestas_unidades_tipo")
    op.execute("DROP INDEX IF EXISTS ix_florestas_unidades_codigo")
    op.execute("DROP TABLE IF EXISTS florestas_unidades_manejo")

    op.execute("DROP INDEX IF EXISTS ix_florestas_operadores_tipo")
    op.execute("DROP INDEX IF EXISTS ix_florestas_operadores_nif")
    op.execute("DROP TABLE IF EXISTS florestas_operadores_florestais")
