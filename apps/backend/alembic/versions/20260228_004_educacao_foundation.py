"""create educacao tables and institutional seed

Revision ID: 20260228_004_educacao_foundation
Revises: 20260228_003_operational_flow
Create Date: 2026-02-28 04:00:00.000000
"""

from alembic import op

revision = "20260228_004_educacao_foundation"
down_revision = "20260228_003_operational_flow"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_anos_letivos (
            id UUID PRIMARY KEY,
            ano INTEGER NOT NULL UNIQUE,
            data_inicio DATE NOT NULL,
            data_fim DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        ALTER TABLE educacao_anos_letivos
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        """
    )
    op.execute(
        """
        ALTER TABLE educacao_anos_letivos
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_escolas (
            id UUID PRIMARY KEY,
            codigo_med VARCHAR(32) NOT NULL UNIQUE,
            nome VARCHAR(255) NOT NULL,
            tipo VARCHAR(32) NOT NULL,
            ciclos JSONB NOT NULL DEFAULT '[]'::jsonb,
            provincia VARCHAR(128) NOT NULL,
            municipio VARCHAR(128) NOT NULL,
            comuna VARCHAR(128) NOT NULL,
            bairro VARCHAR(128) NOT NULL,
            endereco TEXT NOT NULL,
            contacto VARCHAR(64),
            email VARCHAR(255),
            ativa BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        ALTER TABLE educacao_escolas
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        """
    )
    op.execute(
        """
        ALTER TABLE educacao_escolas
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_turmas (
            id UUID PRIMARY KEY,
            escola_id UUID NOT NULL REFERENCES educacao_escolas(id) ON DELETE CASCADE,
            ano_letivo_id UUID NOT NULL REFERENCES educacao_anos_letivos(id) ON DELETE RESTRICT,
            codigo VARCHAR(32) NOT NULL,
            classe VARCHAR(32) NOT NULL,
            turno VARCHAR(16) NOT NULL,
            capacidade INTEGER NOT NULL DEFAULT 40,
            ativa BOOLEAN NOT NULL DEFAULT TRUE
        )
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'uq_educacao_turmas_escola_ano_codigo'
            ) THEN
                ALTER TABLE educacao_turmas
                ADD CONSTRAINT uq_educacao_turmas_escola_ano_codigo
                UNIQUE (escola_id, ano_letivo_id, codigo);
            END IF;
        END $$;
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_matriculas (
            id UUID PRIMARY KEY,
            numero_processo VARCHAR(50) NOT NULL UNIQUE,
            citizen_id UUID NOT NULL,
            escola_id UUID NOT NULL REFERENCES educacao_escolas(id) ON DELETE RESTRICT,
            turma_id UUID NOT NULL REFERENCES educacao_turmas(id) ON DELETE RESTRICT,
            ano_letivo_id UUID NOT NULL REFERENCES educacao_anos_letivos(id) ON DELETE RESTRICT,
            data_matricula DATE NOT NULL,
            status VARCHAR(24) NOT NULL DEFAULT 'pendente',
            observacoes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        ALTER TABLE educacao_matriculas
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        """
    )
    op.execute(
        """
        ALTER TABLE educacao_matriculas
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_escolas_codigo_med ON educacao_escolas (codigo_med)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_escolas_provincia ON educacao_escolas (provincia)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_escolas_municipio ON educacao_escolas (municipio)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_educacao_escolas_ativa ON educacao_escolas (ativa)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_turmas_escola_id ON educacao_turmas (escola_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_turmas_ano_letivo_id ON educacao_turmas (ano_letivo_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_matriculas_numero_processo ON educacao_matriculas (numero_processo)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_matriculas_citizen_id ON educacao_matriculas (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_matriculas_escola_id ON educacao_matriculas (escola_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_matriculas_ano_letivo_id ON educacao_matriculas (ano_letivo_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_matriculas_status ON educacao_matriculas (status)"
    )

    # Seed institucional (Angola) - idempotente
    op.execute(
        """
        INSERT INTO educacao_anos_letivos (id, ano, data_inicio, data_fim, ativo)
        VALUES
            ('e5047a40-cd8a-4e40-bfdd-467f76d467bb', 2025, DATE '2025-09-01', DATE '2026-06-30', TRUE),
            ('36a95d8c-8f7a-4d1b-b5f1-2ec39570ab7f', 2026, DATE '2026-09-01', DATE '2027-06-30', FALSE)
        ON CONFLICT (ano) DO UPDATE SET
            data_inicio = EXCLUDED.data_inicio,
            data_fim = EXCLUDED.data_fim,
            ativo = EXCLUDED.ativo,
            updated_at = now()
        """
    )
    op.execute(
        """
        INSERT INTO educacao_escolas (
            id, codigo_med, nome, tipo, ciclos, provincia, municipio, comuna, bairro, endereco, contacto, email, ativa
        )
        VALUES
            (
                'd7668e8f-c6b6-4ad8-a9d8-696c16ea95a6',
                'LUA/KAZ/0012',
                'Escola Primaria 1 de Maio',
                'publica',
                '["primario"]'::jsonb,
                'Luanda',
                'Cazenga',
                'Hoji-ya-Henda',
                '11 de Novembro',
                'Rua Principal, Hoji-ya-Henda',
                '+244 923 000 120',
                'ep1maio.luanda@med.gov.ao',
                TRUE
            ),
            (
                '0a59f4cb-2086-4a7f-809f-65ca08a7a9f9',
                'HUA/CBB/0007',
                'Complexo Escolar 4 de Fevereiro',
                'publica',
                '["primario","secundario_1"]'::jsonb,
                'Huambo',
                'Caala',
                'Sede',
                'Centro',
                'Avenida da Independencia, Caala',
                '+244 923 000 707',
                'ce4fevereiro.huambo@med.gov.ao',
                TRUE
            ),
            (
                'f5d80d94-8a6f-4f7a-8ef0-f58ecb9b86dc',
                'BGU/LOB/0018',
                'Liceu Nacional de Lobito',
                'publico_privada',
                '["secundario_1","secundario_2","tecnico"]'::jsonb,
                'Benguela',
                'Lobito',
                'Restinga',
                'Compao',
                'Rua do Porto, Restinga',
                '+244 923 000 918',
                'liceu.lobito@med.gov.ao',
                TRUE
            )
        ON CONFLICT (codigo_med) DO UPDATE SET
            nome = EXCLUDED.nome,
            tipo = EXCLUDED.tipo,
            ciclos = EXCLUDED.ciclos,
            provincia = EXCLUDED.provincia,
            municipio = EXCLUDED.municipio,
            comuna = EXCLUDED.comuna,
            bairro = EXCLUDED.bairro,
            endereco = EXCLUDED.endereco,
            contacto = EXCLUDED.contacto,
            email = EXCLUDED.email,
            ativa = EXCLUDED.ativa,
            updated_at = now()
        """
    )
    op.execute(
        """
        INSERT INTO educacao_turmas (id, escola_id, ano_letivo_id, codigo, classe, turno, capacidade, ativa)
        VALUES
            (
                '0d72a671-e141-4f0b-a07c-93289f86045f',
                'd7668e8f-c6b6-4ad8-a9d8-696c16ea95a6',
                'e5047a40-cd8a-4e40-bfdd-467f76d467bb',
                '1A',
                '1a',
                'manha',
                45,
                TRUE
            ),
            (
                '9a15b238-ecf8-4857-81cb-e53405695f8a',
                'd7668e8f-c6b6-4ad8-a9d8-696c16ea95a6',
                'e5047a40-cd8a-4e40-bfdd-467f76d467bb',
                '5A',
                '5a',
                'tarde',
                45,
                TRUE
            ),
            (
                '9dd7ebad-d831-4f48-b177-6f2f6d87d0f7',
                '0a59f4cb-2086-4a7f-809f-65ca08a7a9f9',
                'e5047a40-cd8a-4e40-bfdd-467f76d467bb',
                '7A',
                '7a',
                'manha',
                40,
                TRUE
            ),
            (
                'e2f67dc3-8552-4b61-9256-10c08986cc22',
                '0a59f4cb-2086-4a7f-809f-65ca08a7a9f9',
                'e5047a40-cd8a-4e40-bfdd-467f76d467bb',
                '9B',
                '9a',
                'tarde',
                40,
                TRUE
            ),
            (
                'e48736e4-f219-4cb6-b85d-4308bcbca04f',
                'f5d80d94-8a6f-4f7a-8ef0-f58ecb9b86dc',
                'e5047a40-cd8a-4e40-bfdd-467f76d467bb',
                '10A',
                '10a',
                'manha',
                35,
                TRUE
            ),
            (
                '1072e2bd-5688-472f-95ad-f3017f945ab7',
                'f5d80d94-8a6f-4f7a-8ef0-f58ecb9b86dc',
                'e5047a40-cd8a-4e40-bfdd-467f76d467bb',
                '12T',
                '12a',
                'noite',
                30,
                TRUE
            )
        ON CONFLICT (escola_id, ano_letivo_id, codigo) DO UPDATE SET
            classe = EXCLUDED.classe,
            turno = EXCLUDED.turno,
            capacidade = EXCLUDED.capacidade,
            ativa = EXCLUDED.ativa
        """
    )


def downgrade():
    # Remove seed institucional
    op.execute(
        """
        DELETE FROM educacao_turmas
        WHERE id IN (
            '0d72a671-e141-4f0b-a07c-93289f86045f',
            '9a15b238-ecf8-4857-81cb-e53405695f8a',
            '9dd7ebad-d831-4f48-b177-6f2f6d87d0f7',
            'e2f67dc3-8552-4b61-9256-10c08986cc22',
            'e48736e4-f219-4cb6-b85d-4308bcbca04f',
            '1072e2bd-5688-472f-95ad-f3017f945ab7'
        )
        """
    )
    op.execute(
        """
        DELETE FROM educacao_escolas
        WHERE id IN (
            'd7668e8f-c6b6-4ad8-a9d8-696c16ea95a6',
            '0a59f4cb-2086-4a7f-809f-65ca08a7a9f9',
            'f5d80d94-8a6f-4f7a-8ef0-f58ecb9b86dc'
        )
        """
    )
    op.execute(
        """
        DELETE FROM educacao_anos_letivos
        WHERE id IN (
            'e5047a40-cd8a-4e40-bfdd-467f76d467bb',
            '36a95d8c-8f7a-4d1b-b5f1-2ec39570ab7f'
        )
        """
    )

    op.execute("DROP INDEX IF EXISTS ix_educacao_matriculas_status")
    op.execute("DROP INDEX IF EXISTS ix_educacao_matriculas_ano_letivo_id")
    op.execute("DROP INDEX IF EXISTS ix_educacao_matriculas_escola_id")
    op.execute("DROP INDEX IF EXISTS ix_educacao_matriculas_citizen_id")
    op.execute("DROP INDEX IF EXISTS ix_educacao_matriculas_numero_processo")
    op.execute("DROP INDEX IF EXISTS ix_educacao_turmas_ano_letivo_id")
    op.execute("DROP INDEX IF EXISTS ix_educacao_turmas_escola_id")
    op.execute("DROP INDEX IF EXISTS ix_educacao_escolas_ativa")
    op.execute("DROP INDEX IF EXISTS ix_educacao_escolas_municipio")
    op.execute("DROP INDEX IF EXISTS ix_educacao_escolas_provincia")
    op.execute("DROP INDEX IF EXISTS ix_educacao_escolas_codigo_med")
    op.execute("DROP TABLE IF EXISTS educacao_matriculas")
    op.execute("DROP TABLE IF EXISTS educacao_turmas")
    op.execute("DROP TABLE IF EXISTS educacao_escolas")
    op.execute("DROP TABLE IF EXISTS educacao_anos_letivos")
