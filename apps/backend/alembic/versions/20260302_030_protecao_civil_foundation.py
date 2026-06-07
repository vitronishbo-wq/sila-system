"""create protecao_civil foundation tables

Revision ID: 20260302_030_protecao_civil_foundation
Revises: 20260302_029_seguranca_publica_vestigios_evidencias
Create Date: 2026-03-02 23:59:59.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260302_030_protecao_civil_foundation"
down_revision = "20260302_029_seguranca_publica_vestigios_evidencias"
branch_labels = None
depends_on = None


def _create_corporacoes_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS protecao_civil_corporacoes (
            id UUID PRIMARY KEY,
            codigo_corporacao VARCHAR(50) NOT NULL UNIQUE,
            nome VARCHAR(200) NOT NULL,
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
                WHERE conname = 'ck_protecao_corporacoes_campos_basicos'
                  AND conrelid = 'protecao_civil_corporacoes'::regclass
            ) THEN
                ALTER TABLE protecao_civil_corporacoes
                ADD CONSTRAINT ck_protecao_corporacoes_campos_basicos
                CHECK (
                    char_length(trim(codigo_corporacao)) >= 10
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
                WHERE conname = 'ck_protecao_corporacoes_status'
                  AND conrelid = 'protecao_civil_corporacoes'::regclass
            ) THEN
                ALTER TABLE protecao_civil_corporacoes
                ADD CONSTRAINT ck_protecao_corporacoes_status
                CHECK (
                    status IN ('ativa', 'em_reestruturacao', 'interditada', 'desativada')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_corporacoes_codigo ON protecao_civil_corporacoes (codigo_corporacao)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_corporacoes_nome ON protecao_civil_corporacoes (nome)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_corporacoes_municipio ON protecao_civil_corporacoes (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_corporacoes_provincia ON protecao_civil_corporacoes (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_corporacoes_status ON protecao_civil_corporacoes (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_corporacoes_ativo ON protecao_civil_corporacoes (ativo)"
    )


def _create_bombeiros_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS protecao_civil_bombeiros (
            id UUID PRIMARY KEY,
            matricula VARCHAR(50) NOT NULL UNIQUE,
            corporacao_id UUID NOT NULL,
            nome VARCHAR(200) NOT NULL,
            data_nascimento DATE NOT NULL,
            cpf VARCHAR(14) NOT NULL UNIQUE,
            rg VARCHAR(30) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            cargo VARCHAR(40),
            data_ingresso DATE NOT NULL,
            status VARCHAR(30) NOT NULL,
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
                WHERE conname = 'ck_protecao_bombeiros_campos_basicos'
                  AND conrelid = 'protecao_civil_bombeiros'::regclass
            ) THEN
                ALTER TABLE protecao_civil_bombeiros
                ADD CONSTRAINT ck_protecao_bombeiros_campos_basicos
                CHECK (
                    char_length(trim(matricula)) >= 10
                    AND char_length(trim(nome)) >= 3
                    AND char_length(trim(cpf)) = 14
                    AND data_nascimento < CURRENT_DATE
                    AND data_ingresso <= CURRENT_DATE
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
                WHERE conname = 'ck_protecao_bombeiros_enum_values'
                  AND conrelid = 'protecao_civil_bombeiros'::regclass
            ) THEN
                ALTER TABLE protecao_civil_bombeiros
                ADD CONSTRAINT ck_protecao_bombeiros_enum_values
                CHECK (
                    tipo IN (
                        'bombeiro',
                        'socorrista',
                        'voluntario',
                        'coordenador',
                        'agente_defesa_civil'
                    )
                    AND status IN ('ativo', 'afastado', 'licenca', 'aposentado', 'desligado')
                    AND (cargo IS NULL OR cargo IN (
                        'soldado',
                        'cabo',
                        'sargento',
                        'tenente',
                        'capitao',
                        'major',
                        'tenente_coronel',
                        'coronel',
                        'comandante'
                    ))
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_bombeiros_matricula ON protecao_civil_bombeiros (matricula)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_bombeiros_corporacao_id ON protecao_civil_bombeiros (corporacao_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_bombeiros_nome ON protecao_civil_bombeiros (nome)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_bombeiros_cpf ON protecao_civil_bombeiros (cpf)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_bombeiros_tipo ON protecao_civil_bombeiros (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_bombeiros_status ON protecao_civil_bombeiros (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_bombeiros_ativo ON protecao_civil_bombeiros (ativo)"
    )


def _create_ocorrencias_table() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS protecao_civil_ocorrencias_emergenciais (
            id UUID PRIMARY KEY,
            codigo_ocorrencia VARCHAR(50) NOT NULL UNIQUE,
            corporacao_id UUID NOT NULL,
            bombeiro_responsavel_id UUID,
            tipo VARCHAR(40) NOT NULL,
            status VARCHAR(40) NOT NULL,
            prioridade VARCHAR(20) NOT NULL,
            data_ocorrencia TIMESTAMP NOT NULL,
            descricao TEXT NOT NULL,
            municipio VARCHAR(100) NOT NULL,
            provincia VARCHAR(100) NOT NULL,
            endereco VARCHAR(255),
            vitimas INTEGER NOT NULL DEFAULT 0,
            desalojados INTEGER NOT NULL DEFAULT 0,
            obitos INTEGER NOT NULL DEFAULT 0,
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
                WHERE conname = 'ck_protecao_ocorrencias_campos_basicos'
                  AND conrelid = 'protecao_civil_ocorrencias_emergenciais'::regclass
            ) THEN
                ALTER TABLE protecao_civil_ocorrencias_emergenciais
                ADD CONSTRAINT ck_protecao_ocorrencias_campos_basicos
                CHECK (
                    char_length(trim(codigo_ocorrencia)) >= 10
                    AND char_length(trim(descricao)) >= 5
                    AND vitimas >= 0
                    AND desalojados >= 0
                    AND obitos >= 0
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
                WHERE conname = 'ck_protecao_ocorrencias_enum_values'
                  AND conrelid = 'protecao_civil_ocorrencias_emergenciais'::regclass
            ) THEN
                ALTER TABLE protecao_civil_ocorrencias_emergenciais
                ADD CONSTRAINT ck_protecao_ocorrencias_enum_values
                CHECK (
                    tipo IN (
                        'incendio_urbano',
                        'incendio_florestal',
                        'desabamento',
                        'deslizamento',
                        'inundacao',
                        'enchente',
                        'alagamento',
                        'seca',
                        'tempestade',
                        'acidente_transporte',
                        'acidente_quimico',
                        'explosao',
                        'rompimento_barragem',
                        'resgate',
                        'salvamento',
                        'atendimento_pre_hospitalar'
                    )
                    AND status IN (
                        'recebida',
                        'em_atendimento',
                        'concluida',
                        'cancelada',
                        'falso_alarme'
                    )
                    AND prioridade IN ('baixa', 'media', 'alta', 'critica')
                );
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_codigo ON protecao_civil_ocorrencias_emergenciais (codigo_ocorrencia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_corporacao_id ON protecao_civil_ocorrencias_emergenciais (corporacao_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_bombeiro_responsavel ON protecao_civil_ocorrencias_emergenciais (bombeiro_responsavel_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_tipo ON protecao_civil_ocorrencias_emergenciais (tipo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_status ON protecao_civil_ocorrencias_emergenciais (status)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_prioridade ON protecao_civil_ocorrencias_emergenciais (prioridade)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_data_ocorrencia ON protecao_civil_ocorrencias_emergenciais (data_ocorrencia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_data_registro ON protecao_civil_ocorrencias_emergenciais (data_registro)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_municipio ON protecao_civil_ocorrencias_emergenciais (municipio)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_provincia ON protecao_civil_ocorrencias_emergenciais (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_protecao_ocorrencias_ativo ON protecao_civil_ocorrencias_emergenciais (ativo)"
    )


def upgrade() -> None:
    _create_corporacoes_table()
    _create_bombeiros_table()
    _create_ocorrencias_table()


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_ativo")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_provincia")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_municipio")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_data_registro")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_data_ocorrencia")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_prioridade")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_status")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_tipo")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_bombeiro_responsavel")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_corporacao_id")
    op.execute("DROP INDEX IF EXISTS ix_protecao_ocorrencias_codigo")
    op.execute("DROP TABLE IF EXISTS protecao_civil_ocorrencias_emergenciais")

    op.execute("DROP INDEX IF EXISTS ix_protecao_bombeiros_ativo")
    op.execute("DROP INDEX IF EXISTS ix_protecao_bombeiros_status")
    op.execute("DROP INDEX IF EXISTS ix_protecao_bombeiros_tipo")
    op.execute("DROP INDEX IF EXISTS ix_protecao_bombeiros_cpf")
    op.execute("DROP INDEX IF EXISTS ix_protecao_bombeiros_nome")
    op.execute("DROP INDEX IF EXISTS ix_protecao_bombeiros_corporacao_id")
    op.execute("DROP INDEX IF EXISTS ix_protecao_bombeiros_matricula")
    op.execute("DROP TABLE IF EXISTS protecao_civil_bombeiros")

    op.execute("DROP INDEX IF EXISTS ix_protecao_corporacoes_ativo")
    op.execute("DROP INDEX IF EXISTS ix_protecao_corporacoes_status")
    op.execute("DROP INDEX IF EXISTS ix_protecao_corporacoes_provincia")
    op.execute("DROP INDEX IF EXISTS ix_protecao_corporacoes_municipio")
    op.execute("DROP INDEX IF EXISTS ix_protecao_corporacoes_nome")
    op.execute("DROP INDEX IF EXISTS ix_protecao_corporacoes_codigo")
    op.execute("DROP TABLE IF EXISTS protecao_civil_corporacoes")
