"""expand service catalog governance metadata

Revision ID: 012_001_expand_service_catalog_governance
Revises: 011_001_create_operational_flow_tables
Create Date: 2026-02-28
"""
from alembic import op
revision = '012_001_expand_service_catalog_governance'
down_revision = '011_001_create_operational_flow_tables'
branch_labels = None
depends_on = None

def upgrade():
    op.execute('\n        CREATE TABLE IF NOT EXISTS modules (\n            id SERIAL PRIMARY KEY,\n            slug VARCHAR(100) NOT NULL UNIQUE,\n            title VARCHAR(200) NOT NULL,\n            description TEXT,\n            icon VARCHAR(50) NOT NULL DEFAULT \'module\',\n            color VARCHAR(20) NOT NULL DEFAULT \'#0B5E8E\',\n            is_active BOOLEAN NOT NULL DEFAULT TRUE,\n            is_foundational BOOLEAN NOT NULL DEFAULT FALSE,\n            "order" INTEGER NOT NULL DEFAULT 0,\n            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),\n            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()\n        )\n        ')
    op.execute("\n        CREATE TABLE IF NOT EXISTS services (\n            id UUID PRIMARY KEY,\n            code VARCHAR NOT NULL UNIQUE,\n            name VARCHAR NOT NULL,\n            description TEXT,\n            scope VARCHAR NOT NULL DEFAULT 'public',\n            is_active BOOLEAN NOT NULL DEFAULT TRUE,\n            module_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,\n            price NUMERIC(12, 2) NOT NULL DEFAULT 0.00,\n            estimated_days INTEGER NOT NULL DEFAULT 5,\n            workflow_definition_key VARCHAR(120),\n            required_documents JSONB NOT NULL DEFAULT '[]'::jsonb,\n            visibility VARCHAR(20) NOT NULL DEFAULT 'PUBLIC',\n            version INTEGER NOT NULL DEFAULT 1,\n            business_priority INTEGER NOT NULL DEFAULT 100,\n            territory_id UUID NULL,\n            is_public BOOLEAN NOT NULL DEFAULT FALSE,\n            is_essential BOOLEAN NOT NULL DEFAULT FALSE,\n            icon_slug VARCHAR NULL,\n            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()\n        )\n        ")
    op.execute('CREATE INDEX IF NOT EXISTS ix_modules_slug ON modules (slug)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_services_code ON services (code)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_services_module_id ON services (module_id)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_services_territory_id ON services (territory_id)')
    op.execute('\n        ALTER TABLE IF EXISTS services\n        ADD COLUMN IF NOT EXISTS description TEXT\n        ')
    op.execute('\n        ALTER TABLE IF EXISTS services\n        ADD COLUMN IF NOT EXISTS workflow_definition_key VARCHAR(120)\n        ')
    op.execute("\n        ALTER TABLE IF EXISTS services\n        ADD COLUMN IF NOT EXISTS required_documents JSONB NOT NULL DEFAULT '[]'::jsonb\n        ")
    op.execute("\n        ALTER TABLE IF EXISTS services\n        ADD COLUMN IF NOT EXISTS visibility VARCHAR(20) NOT NULL DEFAULT 'PUBLIC'\n        ")
    op.execute('\n        ALTER TABLE IF EXISTS services\n        ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1\n        ')
    op.execute('\n        ALTER TABLE IF EXISTS services\n        ADD COLUMN IF NOT EXISTS business_priority INTEGER NOT NULL DEFAULT 100\n        ')
    op.execute("\n        DO $$\n        BEGIN\n            IF EXISTS (\n                SELECT 1\n                FROM information_schema.tables\n                WHERE table_schema = current_schema()\n                AND table_name = 'services'\n            ) THEN\n                UPDATE services\n                SET workflow_definition_key = code\n                WHERE workflow_definition_key IS NULL;\n            END IF;\n        END $$;\n        ")
    op.execute('\n        CREATE INDEX IF NOT EXISTS ix_services_visibility\n        ON services (visibility)\n        ')
    op.execute('\n        CREATE INDEX IF NOT EXISTS ix_services_module_active\n        ON services (module_id, is_active)\n        ')
    op.execute("\n        DO $$\n        BEGIN\n            IF EXISTS (\n                SELECT 1\n                FROM information_schema.tables\n                WHERE table_schema = current_schema()\n                AND table_name = 'services'\n            ) AND NOT EXISTS (\n                SELECT 1 FROM pg_constraint\n                WHERE conname = 'ck_services_visibility'\n            ) THEN\n                ALTER TABLE services\n                ADD CONSTRAINT ck_services_visibility\n                CHECK (visibility IN ('PUBLIC', 'INTERNAL'));\n            END IF;\n        END $$;\n        ")

def downgrade():
    op.execute('ALTER TABLE IF EXISTS services DROP CONSTRAINT IF EXISTS ck_services_visibility')
    op.execute('DROP INDEX IF EXISTS ix_services_module_active')
    op.execute('DROP INDEX IF EXISTS ix_services_visibility')
    op.execute('ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS business_priority')
    op.execute('ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS version')
    op.execute('ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS visibility')
    op.execute('ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS required_documents')
    op.execute('ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS workflow_definition_key')
    op.execute('ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS description')