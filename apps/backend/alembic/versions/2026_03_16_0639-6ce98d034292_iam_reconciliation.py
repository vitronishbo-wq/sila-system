"""iam reconciliation

Revision ID: 6ce98d034292
Revises: 47abb2f40d12
Create Date: 2026-03-16 06:39:50.454112

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6ce98d034292"
down_revision: str | Sequence[str] | None = "47abb2f40d12"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names(schema="public"))

    if "users" not in tables:
        op.create_table(
            "users",
            sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
            sa.Column(
                "uuid",
                sa.VARCHAR(length=36),
                server_default=sa.text("gen_random_uuid()"),
                nullable=False,
            ),
            sa.Column("email", sa.VARCHAR(length=255), nullable=False),
            sa.Column("hashed_password", sa.VARCHAR(length=255), nullable=False),
            sa.Column("phone", sa.VARCHAR(length=20), nullable=True),
            sa.Column("bi_number", sa.VARCHAR(length=20), nullable=True),
            sa.Column("is_active", sa.BOOLEAN(), nullable=False),
            sa.Column("is_verified", sa.BOOLEAN(), nullable=False),
            sa.Column("status", sa.VARCHAR(length=20), nullable=False),
            sa.Column("region_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("roles", postgresql.JSON(astext_type=sa.Text()), nullable=False),
            sa.Column(
                "created_at",
                postgresql.TIMESTAMP(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                postgresql.TIMESTAMP(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("last_login", postgresql.TIMESTAMP(timezone=True), nullable=True),
            sa.Column("full_name", sa.VARCHAR(length=100), nullable=True),
            sa.Column(
                "administrative_level",
                sa.VARCHAR(length=20),
                server_default=sa.text("'LOCAL'::character varying"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(
                ["region_id"], ["locations.id"], name=op.f("users_region_id_fkey")
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
        )
        op.create_index(op.f("ix_users_uuid"), "users", ["uuid"], unique=True)
        op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
        op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
        op.create_index(op.f("ix_users_bi_number"), "users", ["bi_number"], unique=True)
        tables.add("users")

    if "iam_users" not in tables:
        op.create_table(
            "iam_users",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("username", sa.String(length=100), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column(
                "status",
                sa.String(length=50),
                server_default="PENDING_VERIFICATION",
                nullable=False,
            ),
            sa.Column("is_superuser", sa.Boolean(), server_default="false", nullable=False),
            sa.Column("full_name", sa.String(length=255), nullable=True),
            sa.Column("phone", sa.String(length=50), nullable=True),
            sa.Column("department", sa.String(length=255), nullable=True),
            sa.Column("position", sa.String(length=255), nullable=True),
            sa.Column("failed_login_attempts", sa.Integer(), server_default="0", nullable=False),
            sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("last_login_ip", sa.String(length=50), nullable=True),
            sa.Column("password_changed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("password_expires_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("mfa_enabled", sa.Boolean(), server_default="false", nullable=False),
            sa.Column("mfa_secret", sa.String(length=255), nullable=True),
            sa.Column("mfa_type", sa.String(length=50), server_default="NONE", nullable=False),
            sa.Column("custom_metadata", sa.JSON(), nullable=True),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_by", sa.String(length=36), nullable=True),
            sa.Column("updated_by", sa.String(length=36), nullable=True),
            sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("username", name="uq_iam_users_username"),
            sa.UniqueConstraint("email", name="uq_iam_users_email"),
            sa.UniqueConstraint("citizen_id", name="uq_iam_users_citizen_id"),
        )
        op.create_index(
            "ix_iam_users_status_created",
            "iam_users",
            ["status", "created_at"],
            unique=False,
        )
        op.create_index(
            "ix_iam_users_username_lower",
            "iam_users",
            [sa.func.lower(sa.column("username"))],
            unique=False,
        )
        op.create_index(
            "ix_iam_users_email_lower",
            "iam_users",
            [sa.func.lower(sa.column("email"))],
            unique=False,
        )
        op.create_index("ix_iam_users_citizen_id", "iam_users", ["citizen_id"], unique=False)
        op.create_index("ix_iam_users_status", "iam_users", ["status"], unique=False)
        tables.add("iam_users")

    if "iam_roles" not in tables:
        op.create_table(
            "iam_roles",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False, unique=True),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("role_type", sa.String(length=50), server_default="CUSTOM", nullable=False),
            sa.Column("is_system", sa.Boolean(), server_default="false", nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_by", sa.String(length=36), nullable=True),
            sa.Column("updated_by", sa.String(length=36), nullable=True),
            sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name", name="uq_iam_roles_name"),
        )
        op.create_index("ix_iam_roles_name", "iam_roles", ["name"], unique=False)
        op.create_index("ix_iam_roles_type", "iam_roles", ["role_type"], unique=False)
        tables.add("iam_roles")

    if "iam_permissions" not in tables:
        op.create_table(
            "iam_permissions",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False, unique=True),
            sa.Column("resource", sa.String(length=100), nullable=False),
            sa.Column("action", sa.String(length=100), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("is_system", sa.Boolean(), server_default="false", nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_by", sa.String(length=36), nullable=True),
            sa.Column("updated_by", sa.String(length=36), nullable=True),
            sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name", name="uq_iam_permissions_name"),
            sa.UniqueConstraint("resource", "action", name="uq_iam_permissions_resource_action"),
        )
        op.create_index("ix_iam_permissions_name", "iam_permissions", ["name"], unique=False)
        op.create_index(
            "ix_iam_permissions_resource_action",
            "iam_permissions",
            ["resource", "action"],
            unique=False,
        )
        tables.add("iam_permissions")

    if "iam_role_permissions" not in tables:
        op.create_table(
            "iam_role_permissions",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("role_id", sa.String(length=36), nullable=False),
            sa.Column("permission_id", sa.String(length=36), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_by", sa.String(length=36), nullable=True),
            sa.Column("updated_by", sa.String(length=36), nullable=True),
            sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
            sa.ForeignKeyConstraint(["role_id"], ["iam_roles.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["permission_id"], ["iam_permissions.id"], ondelete="CASCADE"),
        )
        op.create_index(
            "ix_iam_role_permissions_role_id",
            "iam_role_permissions",
            ["role_id"],
            unique=False,
        )
        op.create_index(
            "ix_iam_role_permissions_permission_id",
            "iam_role_permissions",
            ["permission_id"],
            unique=False,
        )
        tables.add("iam_role_permissions")

    if "iam_user_permissions" not in tables:
        op.create_table(
            "iam_user_permissions",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("user_id", sa.String(length=36), nullable=False),
            sa.Column("permission_id", sa.String(length=36), nullable=False),
            sa.Column(
                "granted_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column("granted_by", sa.String(length=36), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_by", sa.String(length=36), nullable=True),
            sa.Column("updated_by", sa.String(length=36), nullable=True),
            sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "permission_id", name="uq_user_permission"),
            sa.ForeignKeyConstraint(["user_id"], ["iam_users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["permission_id"], ["iam_permissions.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["granted_by"], ["iam_users.id"], ondelete="SET NULL"),
        )
        op.create_index(
            "ix_iam_user_permissions_user_id",
            "iam_user_permissions",
            ["user_id"],
            unique=False,
        )
        op.create_index(
            "ix_iam_user_permissions_permission_id",
            "iam_user_permissions",
            ["permission_id"],
            unique=False,
        )
        tables.add("iam_user_permissions")

    if "iam_users" in tables and "citizenship_citizens" in tables:
        fks = inspector.get_foreign_keys("iam_users", schema="public")
        fk_names = {fk.get("name") for fk in fks}
        if "fk_iam_users_citizen" not in fk_names:
            op.create_foreign_key(
                "fk_iam_users_citizen",
                "iam_users",
                "citizenship_citizens",
                ["citizen_id"],
                ["id"],
            )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names(schema="public"))

    if "iam_users" in tables:
        fks = inspector.get_foreign_keys("iam_users", schema="public")
        if any(fk.get("name") == "fk_iam_users_citizen" for fk in fks):
            op.drop_constraint("fk_iam_users_citizen", "iam_users", type_="foreignkey")

    if "iam_user_permissions" in tables:
        op.drop_index(
            "ix_iam_user_permissions_permission_id",
            table_name="iam_user_permissions",
        )
        op.drop_index(
            "ix_iam_user_permissions_user_id",
            table_name="iam_user_permissions",
        )
        op.drop_table("iam_user_permissions")

    if "iam_role_permissions" in tables:
        op.drop_index(
            "ix_iam_role_permissions_permission_id",
            table_name="iam_role_permissions",
        )
        op.drop_index(
            "ix_iam_role_permissions_role_id",
            table_name="iam_role_permissions",
        )
        op.drop_table("iam_role_permissions")

    if "iam_permissions" in tables:
        op.drop_index("ix_iam_permissions_resource_action", table_name="iam_permissions")
        op.drop_index("ix_iam_permissions_name", table_name="iam_permissions")
        op.drop_table("iam_permissions")

    if "iam_roles" in tables:
        op.drop_index("ix_iam_roles_type", table_name="iam_roles")
        op.drop_index("ix_iam_roles_name", table_name="iam_roles")
        op.drop_table("iam_roles")

    if "iam_users" in tables:
        op.drop_index("ix_iam_users_status", table_name="iam_users")
        op.drop_index("ix_iam_users_citizen_id", table_name="iam_users")
        op.drop_index("ix_iam_users_email_lower", table_name="iam_users")
        op.drop_index("ix_iam_users_username_lower", table_name="iam_users")
        op.drop_index("ix_iam_users_status_created", table_name="iam_users")
        op.drop_table("iam_users")

    if "users" in tables:
        op.drop_index(op.f("ix_users_bi_number"), table_name="users")
        op.drop_index(op.f("ix_users_email"), table_name="users")
        op.drop_index(op.f("ix_users_id"), table_name="users")
        op.drop_index(op.f("ix_users_uuid"), table_name="users")
        op.drop_table("users")
