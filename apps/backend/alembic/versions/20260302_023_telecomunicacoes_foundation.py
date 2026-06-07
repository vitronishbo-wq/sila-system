"""create telecomunicacoes core tables

Revision ID: 20260302_023_telecomunicacoes_foundation
Revises: 20260302_022_juventude_programas_formacoes
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_023_telecomunicacoes_foundation"
down_revision = "20260302_022_juventude_programas_formacoes"
branch_labels = None
depends_on = None


def _create_operadoras_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_operadoras (
            id UUID PRIMARY KEY,
            cnpj VARCHAR(18) NOT NULL UNIQUE,
            razao_social VARCHAR(200) NOT NULL,
            nome_fantasia VARCHAR(200),
            tipo VARCHAR(30) NOT NULL,
            servicos_autorizados TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
            endereco VARCHAR(255) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            telefone VARCHAR(30) NOT NULL,
            email VARCHAR(120) NOT NULL,
            representante_legal VARCHAR(120) NOT NULL,
            representante_documento VARCHAR(40) NOT NULL,
            representante_cargo VARCHAR(80) NOT NULL,
            outorga_id UUID,
            data_autorizacao DATE,
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
                WHERE conname = 'ck_telecom_operadoras_campos_basicos'
                  AND conrelid = 'telecom_operadoras'::regclass
            ) THEN
                ALTER TABLE telecom_operadoras
                ADD CONSTRAINT ck_telecom_operadoras_campos_basicos
                CHECK (
                    char_length(trim(razao_social)) >= 3
                    AND char_length(trim(cnpj)) = 18
                    AND array_length(servicos_autorizados, 1) >= 1
                    AND (data_validade IS NULL OR data_autorizacao IS NULL OR data_validade >= data_autorizacao)
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
                WHERE conname = 'ck_telecom_operadoras_tipo_status'
                  AND conrelid = 'telecom_operadoras'::regclass
            ) THEN
                ALTER TABLE telecom_operadoras
                ADD CONSTRAINT ck_telecom_operadoras_tipo_status
                CHECK (
                    tipo IN ('concessionaria', 'permissionaria', 'autorizataria', 'provedor', 'satelital')
                    AND status IN ('requerida', 'em_analise', 'deferida', 'indeferida', 'vencida', 'renovada', 'cancelada')
                );
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_operadoras_cnpj ON telecom_operadoras (cnpj)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_operadoras_razao_social ON telecom_operadoras (razao_social)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_telecom_operadoras_tipo ON telecom_operadoras (tipo)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_operadoras_municipio ON telecom_operadoras (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_operadoras_provincia ON telecom_operadoras (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_operadoras_status ON telecom_operadoras (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_operadoras_ativo ON telecom_operadoras (ativo)"
    )


def _create_assinantes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS telecom_assinantes (
            id UUID PRIMARY KEY,
            codigo_assinante VARCHAR(50) NOT NULL UNIQUE,
            operadora_id UUID NOT NULL,
            tipo_plano VARCHAR(30) NOT NULL,
            servico_principal VARCHAR(40) NOT NULL,
            data_adesao DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            nome VARCHAR(200),
            citizen_id UUID,
            telefone_contato VARCHAR(30),
            email_contato VARCHAR(120),
            contrato_numero VARCHAR(60),
            valor_mensal NUMERIC(12, 2),
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
                WHERE conname = 'ck_telecom_assinantes_enum_values'
                  AND conrelid = 'telecom_assinantes'::regclass
            ) THEN
                ALTER TABLE telecom_assinantes
                ADD CONSTRAINT ck_telecom_assinantes_enum_values
                CHECK (
                    tipo_plano IN ('pre_pago', 'pos_pago', 'controle', 'corporativo', 'empresarial', 'governamental')
                    AND servico_principal IN (
                        'telefonia_fixa',
                        'telefonia_movel',
                        'internet_fixa',
                        'internet_movel',
                        'tv_assinatura',
                        'radio',
                        'comunicacao_dados'
                    )
                    AND status IN ('ativo', 'suspenso', 'cancelado', 'inadimplente')
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
                WHERE conname = 'ck_telecom_assinantes_campos_basicos'
                  AND conrelid = 'telecom_assinantes'::regclass
            ) THEN
                ALTER TABLE telecom_assinantes
                ADD CONSTRAINT ck_telecom_assinantes_campos_basicos
                CHECK (
                    char_length(trim(codigo_assinante)) >= 10
                    AND data_adesao <= CURRENT_DATE
                    AND (valor_mensal IS NULL OR valor_mensal >= 0)
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_codigo_assinante ON telecom_assinantes (codigo_assinante)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_operadora_id ON telecom_assinantes (operadora_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_tipo_plano ON telecom_assinantes (tipo_plano)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_servico_principal ON telecom_assinantes (servico_principal)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_status ON telecom_assinantes (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_municipio ON telecom_assinantes (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_provincia ON telecom_assinantes (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_citizen_id ON telecom_assinantes (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_telecom_assinantes_ativo ON telecom_assinantes (ativo)"
    )


def upgrade() -> None:
    _create_operadoras_table()
    _create_assinantes_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_provincia")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_municipio")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_servico_principal")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_tipo_plano")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_operadora_id")
    op.execute("DROP INDEX IF EXISTS ix_telecom_assinantes_codigo_assinante")
    op.execute("DROP TABLE IF EXISTS telecom_assinantes")

    op.execute("DROP INDEX IF EXISTS ix_telecom_operadoras_ativo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_operadoras_status")
    op.execute("DROP INDEX IF EXISTS ix_telecom_operadoras_provincia")
    op.execute("DROP INDEX IF EXISTS ix_telecom_operadoras_municipio")
    op.execute("DROP INDEX IF EXISTS ix_telecom_operadoras_tipo")
    op.execute("DROP INDEX IF EXISTS ix_telecom_operadoras_razao_social")
    op.execute("DROP INDEX IF EXISTS ix_telecom_operadoras_cnpj")
    op.execute("DROP TABLE IF EXISTS telecom_operadoras")
