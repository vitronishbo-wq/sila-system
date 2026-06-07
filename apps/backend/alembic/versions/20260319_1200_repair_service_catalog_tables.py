"""repair service catalog tables (idempotent)

Revision ID: 20260319_1200_repair_service_catalog_tables
Revises: 20260319_0900_create_service_catalog_tables
Create Date: 2026-03-19 12:00:00.000000
"""

from __future__ import annotations

from alembic import op

revision: str = "20260319_1200_repair_service_catalog_tables"
down_revision = "20260319_0900_create_service_catalog_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS service_catalog (
            id varchar(36) PRIMARY KEY,
            service_code varchar(80) NOT NULL UNIQUE,
            name varchar(255) NOT NULL,
            category varchar(120),
            description varchar(500),
            price numeric(14,2) NOT NULL DEFAULT 0,
            is_active boolean NOT NULL DEFAULT true,
            created_at timestamptz NOT NULL DEFAULT now(),
            updated_at timestamptz NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_service_catalog_category ON service_catalog (category);"
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS service_forms (
            id varchar(36) PRIMARY KEY,
            service_code varchar(80) NOT NULL REFERENCES service_catalog(service_code) ON DELETE CASCADE,
            version varchar(32) NOT NULL DEFAULT '1',
            schema json NOT NULL,
            is_active boolean NOT NULL DEFAULT true,
            created_at timestamptz NOT NULL DEFAULT now(),
            updated_at timestamptz NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_service_forms_service_code ON service_forms (service_code);"
    )
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_service_forms_service_code ON service_forms (service_code);"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ux_service_forms_service_code;")
    op.execute("DROP INDEX IF EXISTS ix_service_forms_service_code;")
    op.execute("DROP TABLE IF EXISTS service_forms;")
    op.execute("DROP INDEX IF EXISTS ix_service_catalog_category;")
    op.execute("DROP TABLE IF EXISTS service_catalog;")
