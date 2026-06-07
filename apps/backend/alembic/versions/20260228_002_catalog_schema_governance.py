"""create/expand institutional catalog schema with governance fields

Revision ID: 20260228_002_catalog_schema
Revises: 20260228_001_merge_legacy_heads
Create Date: 2026-02-28 02:35:00.000000
"""

from alembic import op

revision = "20260228_002_catalog_schema"
down_revision = "20260228_001_merge_legacy_heads"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS modules (
            id SERIAL PRIMARY KEY,
            slug VARCHAR(100) NOT NULL UNIQUE,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            icon VARCHAR(50) NOT NULL DEFAULT 'module',
            color VARCHAR(20) NOT NULL DEFAULT '#0B5E8E',
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            is_foundational BOOLEAN NOT NULL DEFAULT FALSE,
            "order" INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id UUID PRIMARY KEY,
            code VARCHAR NOT NULL UNIQUE,
            name VARCHAR NOT NULL,
            description TEXT,
            scope VARCHAR NOT NULL DEFAULT 'public',
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            module_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,
            price NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
            estimated_days INTEGER NOT NULL DEFAULT 5,
            workflow_definition_key VARCHAR(120),
            required_documents JSONB NOT NULL DEFAULT '[]'::jsonb,
            visibility VARCHAR(20) NOT NULL DEFAULT 'PUBLIC',
            version INTEGER NOT NULL DEFAULT 1,
            business_priority INTEGER NOT NULL DEFAULT 100,
            territory_id UUID NULL,
            is_public BOOLEAN NOT NULL DEFAULT FALSE,
            is_essential BOOLEAN NOT NULL DEFAULT FALSE,
            icon_slug VARCHAR NULL,
            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("ALTER TABLE IF EXISTS services ADD COLUMN IF NOT EXISTS description TEXT")
    op.execute(
        "ALTER TABLE IF EXISTS services ADD COLUMN IF NOT EXISTS workflow_definition_key VARCHAR(120)"
    )
    op.execute(
        "ALTER TABLE IF EXISTS services "
        "ADD COLUMN IF NOT EXISTS required_documents JSONB NOT NULL DEFAULT '[]'::jsonb"
    )
    op.execute(
        "ALTER TABLE IF EXISTS services "
        "ADD COLUMN IF NOT EXISTS visibility VARCHAR(20) NOT NULL DEFAULT 'PUBLIC'"
    )
    op.execute(
        "ALTER TABLE IF EXISTS services ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1"
    )
    op.execute(
        "ALTER TABLE IF EXISTS services ADD COLUMN IF NOT EXISTS business_priority INTEGER NOT NULL DEFAULT 100"
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_modules_slug ON modules (slug)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_services_code ON services (code)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_services_module_id ON services (module_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_services_territory_id ON services (territory_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_services_visibility ON services (visibility)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_services_module_active ON services (module_id, is_active)"
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'ck_services_visibility'
            ) THEN
                ALTER TABLE services
                ADD CONSTRAINT ck_services_visibility
                CHECK (visibility IN ('PUBLIC', 'INTERNAL'));
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        UPDATE services
        SET workflow_definition_key = code
        WHERE workflow_definition_key IS NULL
        """
    )


def downgrade():
    op.execute("ALTER TABLE IF EXISTS services DROP CONSTRAINT IF EXISTS ck_services_visibility")
    op.execute("DROP INDEX IF EXISTS ix_services_module_active")
    op.execute("DROP INDEX IF EXISTS ix_services_visibility")
    op.execute("DROP INDEX IF EXISTS ix_services_territory_id")
    op.execute("DROP INDEX IF EXISTS ix_services_module_id")
    op.execute("DROP INDEX IF EXISTS ix_services_code")
    op.execute("DROP INDEX IF EXISTS ix_modules_slug")
    op.execute("ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS business_priority")
    op.execute("ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS version")
    op.execute("ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS visibility")
    op.execute("ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS required_documents")
    op.execute("ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS workflow_definition_key")
    op.execute("ALTER TABLE IF EXISTS services DROP COLUMN IF EXISTS description")
    # Keep tables to avoid destructive downgrades in shared environments.
