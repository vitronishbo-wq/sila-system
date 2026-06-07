"""Add new IAM system tables (iam_users, iam_roles, iam_permissions)

Revision ID: 003_add_iam_system
Revises: 002_create_citizen_table
Create Date: 2026-02-26 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "003_add_iam_system"
down_revision = "002_create_citizen_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create new IAM system tables."""

    # 1. Create iam_users table
    op.create_table(
        "iam_users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("citizen_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "status", sa.String(length=50), nullable=False, server_default="PENDING_VERIFICATION"
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
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("updated_by", sa.String(length=36), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username", name="uq_iam_users_username"),
        sa.UniqueConstraint("email", name="uq_iam_users_email"),
        sa.UniqueConstraint("citizen_id", name="uq_iam_users_citizen_id"),
        sa.ForeignKeyConstraint(["citizen_id"], ["citizen.citizen_id"], ondelete="SET NULL"),
    )
    op.create_index(
        "ix_iam_users_status_created", "iam_users", ["status", "created_at"], unique=False
    )
    op.create_index(
        "ix_iam_users_username_lower",
        "iam_users",
        [sa.func.lower(sa.column("username"))],
        unique=False,
    )
    op.create_index(
        "ix_iam_users_email_lower", "iam_users", [sa.func.lower(sa.column("email"))], unique=False
    )
    op.create_index("ix_iam_users_citizen_id", "iam_users", ["citizen_id"], unique=False)
    op.create_index("ix_iam_users_status", "iam_users", ["status"], unique=False)

    # 2. Create iam_roles table
    op.create_table(
        "iam_roles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("role_type", sa.String(length=50), server_default="CUSTOM", nullable=False),
        sa.Column("is_system", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
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

    # 3. Create iam_permissions table
    op.create_table(
        "iam_permissions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("resource", sa.String(length=100), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_system", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
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

    # 4. Create iam_user_roles table (relationship)
    op.create_table(
        "iam_user_roles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column(
            "assigned_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("assigned_by", sa.String(length=36), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("updated_by", sa.String(length=36), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "role_id", name="uq_user_role"),
        sa.ForeignKeyConstraint(["user_id"], ["iam_users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["iam_roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["assigned_by"], ["iam_users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_iam_user_roles_user_id", "iam_user_roles", ["user_id"], unique=False)
    op.create_index("ix_iam_user_roles_role_id", "iam_user_roles", ["role_id"], unique=False)

    # 5. Create iam_role_permissions table (relationship)
    op.create_table(
        "iam_role_permissions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column("permission_id", sa.String(length=36), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
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
        "ix_iam_role_permissions_role_id", "iam_role_permissions", ["role_id"], unique=False
    )
    op.create_index(
        "ix_iam_role_permissions_permission_id",
        "iam_role_permissions",
        ["permission_id"],
        unique=False,
    )

    # 6. Create iam_user_permissions table (direct user permissions)
    op.create_table(
        "iam_user_permissions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("permission_id", sa.String(length=36), nullable=False),
        sa.Column(
            "granted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("granted_by", sa.String(length=36), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
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
        "ix_iam_user_permissions_user_id", "iam_user_permissions", ["user_id"], unique=False
    )
    op.create_index(
        "ix_iam_user_permissions_permission_id",
        "iam_user_permissions",
        ["permission_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop new IAM system tables."""

    # Drop in reverse order of dependencies
    op.drop_index("ix_iam_user_permissions_permission_id", table_name="iam_user_permissions")
    op.drop_index("ix_iam_user_permissions_user_id", table_name="iam_user_permissions")
    op.drop_table("iam_user_permissions")

    op.drop_index("ix_iam_role_permissions_permission_id", table_name="iam_role_permissions")
    op.drop_index("ix_iam_role_permissions_role_id", table_name="iam_role_permissions")
    op.drop_table("iam_role_permissions")

    op.drop_index("ix_iam_user_roles_role_id", table_name="iam_user_roles")
    op.drop_index("ix_iam_user_roles_user_id", table_name="iam_user_roles")
    op.drop_table("iam_user_roles")

    op.drop_index("ix_iam_permissions_resource_action", table_name="iam_permissions")
    op.drop_index("ix_iam_permissions_name", table_name="iam_permissions")
    op.drop_table("iam_permissions")

    op.drop_index("ix_iam_roles_type", table_name="iam_roles")
    op.drop_index("ix_iam_roles_name", table_name="iam_roles")
    op.drop_table("iam_roles")

    op.drop_index("ix_iam_users_citizen_id", table_name="iam_users")
    op.drop_index("ix_iam_users_email_lower", table_name="iam_users")
    op.drop_index("ix_iam_users_username_lower", table_name="iam_users")
    op.drop_index("ix_iam_users_status_created", table_name="iam_users")
    op.drop_table("iam_users")
