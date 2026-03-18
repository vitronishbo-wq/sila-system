"""iam reconciliation

Revision ID: 6ce98d034292
Revises: 47abb2f40d12
Create Date: 2026-03-16 06:39:50.454112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '6ce98d034292'
down_revision: Union[str, Sequence[str], None] = '47abb2f40d12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
        op.create_index(
            "ix_iam_permissions_name", "iam_permissions", ["name"], unique=False
        )
        op.create_index(
            "ix_iam_permissions_resource_action",
            "iam_permissions",
            ["resource", "action"],
            unique=False,
        )

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
            sa.ForeignKeyConstraint(
                ["role_id"], ["iam_roles.id"], ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["permission_id"], ["iam_permissions.id"], ondelete="CASCADE"
            ),
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
            sa.ForeignKeyConstraint(
                ["permission_id"], ["iam_permissions.id"], ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["granted_by"], ["iam_users.id"], ondelete="SET NULL"
            ),
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

    if "users" in tables:
        op.drop_index(op.f("ix_users_bi_number"), table_name="users")
        op.drop_index(op.f("ix_users_email"), table_name="users")
        op.drop_index(op.f("ix_users_id"), table_name="users")
        op.drop_index(op.f("ix_users_uuid"), table_name="users")
        op.drop_table("users")
