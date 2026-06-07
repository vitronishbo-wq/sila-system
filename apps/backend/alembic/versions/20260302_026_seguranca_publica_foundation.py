"""create seguranca_publica foundation tables

Revision ID: 20260302_026_seguranca_publica_foundation
Revises: 20260302_025_telecomunicacoes_qualidade_sla_indicadores
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_026_seguranca_publica_foundation"
down_revision = "20260302_025_telecomunicacoes_qualidade_sla_indicadores"
branch_labels = None
depends_on = None


def _create_unidades_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_unidades_policiais (
            id UUID PRIMARY KEY,
            codigo_unidade VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            endereco VARCHAR(255) NOT NULL,
            comandante VARCHAR(120) NOT NULL,
            data_ativacao DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            telefone VARCHAR(30),
            email VARCHAR(120),
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
                WHERE conname = 'ck_seguranca_unidades_campos_basicos'
                  AND conrelid = 'seguranca_unidades_policiais'::regclass
            ) THEN
                ALTER TABLE seguranca_unidades_policiais
                ADD CONSTRAINT ck_seguranca_unidades_campos_basicos
                CHECK (
                    char_length(trim(codigo_unidade)) >= 10
                    AND char_length(trim(nome)) >= 3
                    AND char_length(trim(comandante)) >= 3
                    AND data_ativacao <= CURRENT_DATE
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
                WHERE conname = 'ck_seguranca_unidades_tipo_status'
                  AND conrelid = 'seguranca_unidades_policiais'::regclass
            ) THEN
                ALTER TABLE seguranca_unidades_policiais
                ADD CONSTRAINT ck_seguranca_unidades_tipo_status
                CHECK (
                    tipo IN (
                        'delegacia',
                        'posto_policial',
                        'batalhao',
                        'companhia',
                        'pelotao',
                        'comando',
                        'base_operacional'
                    )
                    AND status IN ('ativa', 'manutencao', 'interditada', 'desativada')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_unidades_codigo ON seguranca_unidades_policiais (codigo_unidade)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_unidades_nome ON seguranca_unidades_policiais (nome)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_unidades_tipo ON seguranca_unidades_policiais (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_unidades_municipio ON seguranca_unidades_policiais (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_unidades_provincia ON seguranca_unidades_policiais (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_unidades_status ON seguranca_unidades_policiais (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_unidades_ativo ON seguranca_unidades_policiais (ativo)"
    )


def _create_policiais_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_policiais (
            id UUID PRIMARY KEY,
            matricula VARCHAR(50) NOT NULL UNIQUE,
            unidade_id UUID NOT NULL,
            nome VARCHAR(200) NOT NULL,
            data_nascimento DATE NOT NULL,
            cpf VARCHAR(14) NOT NULL UNIQUE,
            rg VARCHAR(30) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            vinculo VARCHAR(30) NOT NULL,
            cargo VARCHAR(40),
            patente VARCHAR(40),
            data_ingresso DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
            porte_arma BOOLEAN NOT NULL DEFAULT FALSE,
            numero_porte VARCHAR(40),
            data_validade_porte DATE,
            telefone VARCHAR(30),
            email VARCHAR(120),
            endereco VARCHAR(255),
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
                WHERE conname = 'ck_seguranca_policiais_campos_basicos'
                  AND conrelid = 'seguranca_policiais'::regclass
            ) THEN
                ALTER TABLE seguranca_policiais
                ADD CONSTRAINT ck_seguranca_policiais_campos_basicos
                CHECK (
                    char_length(trim(matricula)) >= 10
                    AND char_length(trim(nome)) >= 3
                    AND char_length(trim(cpf)) = 14
                    AND data_nascimento < CURRENT_DATE
                    AND data_ingresso <= CURRENT_DATE
                    AND (
                        porte_arma = FALSE
                        OR (numero_porte IS NOT NULL AND data_validade_porte IS NOT NULL)
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
                WHERE conname = 'ck_seguranca_policiais_enum_values'
                  AND conrelid = 'seguranca_policiais'::regclass
            ) THEN
                ALTER TABLE seguranca_policiais
                ADD CONSTRAINT ck_seguranca_policiais_enum_values
                CHECK (
                    tipo IN (
                        'policial',
                        'militar',
                        'bombeiro',
                        'guarda',
                        'inspetor',
                        'perito',
                        'delegado',
                        'escrivao',
                        'investigador'
                    )
                    AND vinculo IN ('efetivo', 'comissionado', 'temporario', 'estagiario', 'reservista')
                    AND status IN (
                        'ativo',
                        'afastado',
                        'licenca',
                        'ferias',
                        'treinamento',
                        'suspenso',
                        'aposentado',
                        'exonerado'
                    )
                    AND (cargo IS NULL OR cargo IN (
                        'delegado',
                        'agente',
                        'escrivao',
                        'investigador',
                        'perito',
                        'papiloscopista',
                        'auxiliar'
                    ))
                    AND (patente IS NULL OR patente IN (
                        'soldado',
                        'cabo',
                        'sargento',
                        'subtenente',
                        'tenente',
                        'capitao',
                        'major',
                        'tenente_coronel',
                        'coronel',
                        'delegado_geral'
                    ))
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_matricula ON seguranca_policiais (matricula)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_unidade_id ON seguranca_policiais (unidade_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_nome ON seguranca_policiais (nome)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_cpf ON seguranca_policiais (cpf)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_tipo ON seguranca_policiais (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_vinculo ON seguranca_policiais (vinculo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_status ON seguranca_policiais (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_policiais_ativo ON seguranca_policiais (ativo)"
    )


def _create_ocorrencias_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS seguranca_ocorrencias (
            id UUID PRIMARY KEY,
            codigo_ocorrencia VARCHAR(50) NOT NULL UNIQUE,
            unidade_id UUID NOT NULL,
            policial_responsavel_id UUID,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            prioridade VARCHAR(20) NOT NULL,
            data_ocorrencia TIMESTAMP NOT NULL,
            descricao TEXT NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            endereco VARCHAR(255),
            vitimas INTEGER NOT NULL DEFAULT 0,
            suspeitos INTEGER NOT NULL DEFAULT 0,
            preso_em_flagrante BOOLEAN NOT NULL DEFAULT FALSE,
            data_registro DATE NOT NULL,
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
                WHERE conname = 'ck_seguranca_ocorrencias_campos_basicos'
                  AND conrelid = 'seguranca_ocorrencias'::regclass
            ) THEN
                ALTER TABLE seguranca_ocorrencias
                ADD CONSTRAINT ck_seguranca_ocorrencias_campos_basicos
                CHECK (
                    char_length(trim(codigo_ocorrencia)) >= 10
                    AND char_length(trim(descricao)) >= 5
                    AND vitimas >= 0
                    AND suspeitos >= 0
                    AND data_registro <= CURRENT_DATE
                    AND data_ocorrencia <= CURRENT_TIMESTAMP
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
                WHERE conname = 'ck_seguranca_ocorrencias_enum_values'
                  AND conrelid = 'seguranca_ocorrencias'::regclass
            ) THEN
                ALTER TABLE seguranca_ocorrencias
                ADD CONSTRAINT ck_seguranca_ocorrencias_enum_values
                CHECK (
                    tipo IN (
                        'roubo',
                        'furto',
                        'homicidio',
                        'latrocinio',
                        'lesao_corporal',
                        'violencia_domestica',
                        'trafico',
                        'posse_arma',
                        'direcao_perigosa',
                        'embriaguez',
                        'desaparecimento',
                        'ameaca',
                        'dano',
                        'estelionato',
                        'falsidade',
                        'corrupcao'
                    )
                    AND status IN (
                        'registrada',
                        'em_andamento',
                        'concluida',
                        'arquivada',
                        'remetida_justica'
                    )
                    AND prioridade IN ('baixa', 'media', 'alta', 'critica')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_codigo ON seguranca_ocorrencias (codigo_ocorrencia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_unidade_id ON seguranca_ocorrencias (unidade_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_policial_responsavel ON seguranca_ocorrencias (policial_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_tipo ON seguranca_ocorrencias (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_status ON seguranca_ocorrencias (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_prioridade ON seguranca_ocorrencias (prioridade)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_data_ocorrencia ON seguranca_ocorrencias (data_ocorrencia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_data_registro ON seguranca_ocorrencias (data_registro)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_municipio ON seguranca_ocorrencias (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_provincia ON seguranca_ocorrencias (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_seguranca_ocorrencias_ativo ON seguranca_ocorrencias (ativo)"
    )


def upgrade() -> None:
    _create_unidades_table()
    _create_policiais_table()
    _create_ocorrencias_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_provincia")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_municipio")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_data_registro")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_data_ocorrencia")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_prioridade")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_policial_responsavel")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_ocorrencias_codigo")
    op.execute("DROP TABLE IF EXISTS seguranca_ocorrencias")

    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_vinculo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_cpf")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_nome")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_unidade_id")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_policiais_matricula")
    op.execute("DROP TABLE IF EXISTS seguranca_policiais")

    op.execute("DROP INDEX IF EXISTS ix_seguranca_unidades_ativo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_unidades_status")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_unidades_provincia")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_unidades_municipio")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_unidades_tipo")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_unidades_nome")
    op.execute("DROP INDEX IF EXISTS ix_seguranca_unidades_codigo")
    op.execute("DROP TABLE IF EXISTS seguranca_unidades_policiais")
