"""core identity reconciliation

Revision ID: 4fabf7e6d527
Revises: 4b8e10487f5a
Create Date: 2026-03-16 07:52:17.445334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4fabf7e6d527'
down_revision: Union[str, Sequence[str], None] = '4b8e10487f5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE SCHEMA IF NOT EXISTS core")
    op.execute("CREATE SCHEMA IF NOT EXISTS citizenship")

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_namespace n ON n.oid = t.typnamespace
                WHERE t.typname = 'user_type' AND n.nspname = 'core'
            ) THEN
                CREATE TYPE core.user_type AS ENUM ('citizen', 'public_servant', 'system', 'foreign');
            END IF;
        END$$;
        """
    )

    bind = op.get_bind()
    inspector = sa.inspect(bind)
    core_tables = set(inspector.get_table_names(schema="core"))
    public_tables = set(inspector.get_table_names(schema="public"))
    citizenship_tables = set(inspector.get_table_names(schema="citizenship"))

    if "roles" not in core_tables:
        op.create_table(
            "roles",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False, unique=True),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            schema="core",
        )
        core_tables.add("roles")

    if "citizens" not in citizenship_tables:
        op.create_table(
            "citizens",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
            sa.Column("name", sa.VARCHAR(length=200), nullable=True),
            sa.Column("email", sa.VARCHAR(length=200), nullable=True),
            sa.Column("phone", sa.VARCHAR(length=50), nullable=True),
            sa.Column(
                "created_at",
                postgresql.TIMESTAMP(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            schema="citizenship",
        )
        citizenship_tables.add("citizens")

        if "citizenship_citizens" in public_tables:
            op.execute(
                """
                INSERT INTO citizenship.citizens (id, name, email, phone, created_at)
                SELECT id, name, email, phone, COALESCE(created_at, now())
                FROM public.citizenship_citizens
                ON CONFLICT (id) DO NOTHING
                """
            )

    enum_type = postgresql.ENUM(
        "citizen",
        "public_servant",
        "system",
        "foreign",
        name="user_type",
        schema="core",
        create_type=False,
    )

    if "users" not in core_tables:
        op.create_table(
            "users",
            sa.Column(
                "id",
                postgresql.UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
                server_default=sa.text("gen_random_uuid()"),
            ),
            sa.Column("username", sa.String(length=255), nullable=False, unique=True),
            sa.Column("email", sa.String(length=255), nullable=True, unique=True),
            sa.Column("user_type", enum_type),
            sa.Column("external_id", postgresql.UUID(as_uuid=True), nullable=True, unique=True),
            sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("status", sa.String(length=50), server_default="active", nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            schema="core",
        )
        core_tables.add("users")

    if "organizations" not in core_tables:
        op.create_table(
            "organizations",
            sa.Column(
                "id",
                postgresql.UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
                server_default=sa.text("gen_random_uuid()"),
            ),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("parent_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("code", sa.String(length=50), nullable=True, unique=True),
            sa.ForeignKeyConstraint(
                ["parent_id"], ["core.organizations.id"], name=op.f("organizations_parent_id_fkey")
            ),
            schema="core",
        )
        core_tables.add("organizations")

    if "user_org_roles" not in core_tables:
        op.create_table(
            "user_org_roles",
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("attributes", postgresql.JSONB, nullable=True),
            sa.ForeignKeyConstraint(
                ["user_id"], ["core.users.id"], name=op.f("user_org_roles_user_id_fkey")
            ),
            sa.ForeignKeyConstraint(
                ["org_id"], ["core.organizations.id"], name=op.f("user_org_roles_org_id_fkey")
            ),
            sa.ForeignKeyConstraint(
                ["role_id"], ["core.roles.id"], name=op.f("user_org_roles_role_id_fkey")
            ),
            sa.PrimaryKeyConstraint("user_id", "org_id", "role_id"),
            schema="core",
        )

    if "users" in core_tables and "citizens" in citizenship_tables:
        fks = inspector.get_foreign_keys("users", schema="core")
        if not any(fk.get("name") == "fk_core_users_citizen" for fk in fks):
            op.create_foreign_key(
                "fk_core_users_citizen",
                "users",
                "citizens",
                ["citizen_id"],
                ["id"],
                source_schema="core",
                referent_schema="citizenship",
            )

    if "iam_roles" in public_tables and "roles" in core_tables:
        op.execute(
            """
            INSERT INTO core.roles (id, name, description, created_at)
            SELECT
                CASE
                    WHEN iam_roles.id ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                    THEN iam_roles.id::uuid
                    ELSE gen_random_uuid()
                END,
                iam_roles.name,
                iam_roles.description,
                COALESCE(iam_roles.created_at, now())
            FROM iam_roles
            ON CONFLICT DO NOTHING
            """
        )

    if "iam_users" in public_tables and "users" in core_tables:
        op.execute(
            """
            INSERT INTO core.users (id, username, email, user_type, external_id, citizen_id, status, created_at)
            SELECT
                CASE
                    WHEN iam_users.id ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                    THEN iam_users.id::uuid
                    ELSE gen_random_uuid()
                END,
                iam_users.username,
                iam_users.email,
                CASE
                    WHEN iam_users.is_superuser THEN 'system'::core.user_type
                    WHEN iam_users.email ILIKE '%@sila.gov.ao' THEN 'public_servant'::core.user_type
                    ELSE 'citizen'::core.user_type
                END,
                NULL,
                iam_users.citizen_id,
                COALESCE(NULLIF(lower(iam_users.status), ''), CASE WHEN iam_users.is_active THEN 'active' ELSE 'inactive' END),
                COALESCE(iam_users.created_at, now())
            FROM iam_users
            ON CONFLICT DO NOTHING
            """
        )

    if "users" in public_tables and "users" in core_tables:
        op.execute(
            """
            INSERT INTO core.users (id, username, email, user_type, external_id, citizen_id, status, created_at)
            SELECT
                CASE
                    WHEN users.uuid ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                    THEN users.uuid::uuid
                    ELSE gen_random_uuid()
                END,
                users.email,
                users.email,
                'citizen'::core.user_type,
                NULL,
                NULL,
                COALESCE(NULLIF(lower(users.status), ''), CASE WHEN users.is_active THEN 'active' ELSE 'inactive' END),
                COALESCE(users.created_at, now())
            FROM public.users
            ON CONFLICT DO NOTHING
            """
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    core_tables = set(inspector.get_table_names(schema="core"))
    citizenship_tables = set(inspector.get_table_names(schema="citizenship"))

    if "users" in core_tables:
        fks = inspector.get_foreign_keys("users", schema="core")
        if any(fk.get("name") == "fk_core_users_citizen" for fk in fks):
            op.drop_constraint(
                "fk_core_users_citizen", "users", type_="foreignkey", schema="core"
            )

    if "user_org_roles" in core_tables:
        op.drop_table("user_org_roles", schema="core")

    if "organizations" in core_tables:
        op.drop_table("organizations", schema="core")

    if "users" in core_tables:
        op.drop_table("users", schema="core")

    if "roles" in core_tables:
        op.drop_table("roles", schema="core")

    if "citizens" in citizenship_tables:
        op.drop_table("citizens", schema="citizenship")

    op.execute("DROP TYPE IF EXISTS core.user_type")
