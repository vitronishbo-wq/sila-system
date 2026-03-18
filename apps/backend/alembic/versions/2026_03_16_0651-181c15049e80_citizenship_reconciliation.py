"""citizenship reconciliation

Revision ID: 181c15049e80
Revises: 6ce98d034292
Create Date: 2026-03-16 06:51:17.670631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '181c15049e80'
down_revision: Union[str, Sequence[str], None] = '6ce98d034292'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names(schema="public"))

    def _is_uuid(col_type: sa.types.TypeEngine | None) -> bool:
        if col_type is None:
            return False
        if isinstance(col_type, postgresql.UUID):
            return True
        return col_type.__class__.__name__.lower() == "uuid"

    def _get_col_type(table_name: str, column_name: str) -> sa.types.TypeEngine | None:
        for col in inspector.get_columns(table_name, schema="public"):
            if col.get("name") == column_name:
                return col.get("type")
        return None

    locations_id_type = _get_col_type("locations", "id")
    users_id_type = _get_col_type("users", "id")

    location_fk_type = (
        postgresql.UUID(as_uuid=True) if _is_uuid(locations_id_type) else sa.Integer()
    )
    user_fk_type = (
        postgresql.UUID(as_uuid=True) if _is_uuid(users_id_type) else sa.Integer()
    )

    if "citizenship_citizens" not in tables:
        residence_nullable = _is_uuid(locations_id_type)
        residence_default = None if residence_nullable else sa.text("28")

        op.create_table(
            "citizenship_citizens",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("name", sa.VARCHAR(length=200), nullable=False),
            sa.Column("email", sa.VARCHAR(length=200), nullable=True),
            sa.Column("phone", sa.VARCHAR(length=50), nullable=True),
            sa.Column("address", sa.VARCHAR(length=500), nullable=True),
            sa.Column("is_active", sa.BOOLEAN(), nullable=False),
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
            sa.Column("bi_number", sa.VARCHAR(length=20), nullable=True),
            sa.Column("birth_date", sa.DATE(), nullable=True),
            sa.Column("birth_location_id", location_fk_type, nullable=True),
            sa.Column(
                "residence_location_id",
                location_fk_type,
                server_default=residence_default,
                nullable=residence_nullable,
            ),
            sa.Column("user_id", user_fk_type, nullable=True),
            sa.PrimaryKeyConstraint("id", name=op.f("citizenship_citizens_pkey")),
            sa.UniqueConstraint(
                "bi_number",
                name=op.f("citizenship_citizens_bi_number_key"),
                postgresql_include=[],
                postgresql_nulls_not_distinct=False,
            ),
            sa.UniqueConstraint(
                "user_id",
                name=op.f("citizenship_citizens_user_id_key"),
                postgresql_include=[],
                postgresql_nulls_not_distinct=False,
            ),
        )

        op.create_index(
            op.f("ix_citizenship_citizens_residence_location"),
            "citizenship_citizens",
            ["residence_location_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_citizenship_citizens_name"),
            "citizenship_citizens",
            ["name"],
            unique=False,
        )
        op.create_index(
            op.f("ix_citizenship_citizens_id"),
            "citizenship_citizens",
            ["id"],
            unique=True,
        )
        op.create_index(
            op.f("ix_citizenship_citizens_email"),
            "citizenship_citizens",
            ["email"],
            unique=True,
        )
        op.create_index(
            op.f("ix_citizenship_citizens_birth_location"),
            "citizenship_citizens",
            ["birth_location_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_citizenship_citizens_bi_number"),
            "citizenship_citizens",
            ["bi_number"],
            unique=False,
        )

        if "locations" in tables:
            op.create_foreign_key(
                op.f("fk_citizenship_citizens_birth_location_id"),
                "citizenship_citizens",
                "locations",
                ["birth_location_id"],
                ["id"],
                ondelete="SET NULL",
            )
            op.create_foreign_key(
                op.f("fk_citizenship_citizens_residence_location_id"),
                "citizenship_citizens",
                "locations",
                ["residence_location_id"],
                ["id"],
                ondelete="RESTRICT",
            )
        if "users" in tables:
            op.create_foreign_key(
                op.f("fk_citizenship_citizens_user_id"),
                "citizenship_citizens",
                "users",
                ["user_id"],
                ["id"],
                ondelete="SET NULL",
            )

        tables.add("citizenship_citizens")

    if "iam_users" in tables and "citizenship_citizens" in tables:
        fks = inspector.get_foreign_keys("iam_users", schema="public")
        fk_names = {fk.get("name") for fk in fks}
        if "fk_iam_users_citizen" not in fk_names:
            missing = bind.execute(
                sa.text(
                    """
                    SELECT DISTINCT citizen_id
                    FROM iam_users
                    WHERE citizen_id IS NOT NULL
                      AND citizen_id NOT IN (SELECT id FROM citizenship_citizens)
                    """
                )
            ).fetchall()
            for row in missing:
                citizen_id = row[0]
                bind.execute(
                    sa.text(
                        """
                        INSERT INTO citizenship_citizens (id, name, is_active)
                        VALUES (:id, :name, :is_active)
                        """
                    ),
                    {
                        "id": citizen_id,
                        "name": f"Imported citizen {citizen_id}",
                        "is_active": True,
                    },
                )
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

    if "citizenship_citizens" in tables:
        op.drop_constraint(
            op.f("fk_citizenship_citizens_user_id"),
            "citizenship_citizens",
            type_="foreignkey",
        )
        op.drop_constraint(
            op.f("fk_citizenship_citizens_residence_location_id"),
            "citizenship_citizens",
            type_="foreignkey",
        )
        op.drop_constraint(
            op.f("fk_citizenship_citizens_birth_location_id"),
            "citizenship_citizens",
            type_="foreignkey",
        )
        op.drop_index(
            op.f("ix_citizenship_citizens_bi_number"),
            table_name="citizenship_citizens",
        )
        op.drop_index(
            op.f("ix_citizenship_citizens_birth_location"),
            table_name="citizenship_citizens",
        )
        op.drop_index(
            op.f("ix_citizenship_citizens_email"),
            table_name="citizenship_citizens",
        )
        op.drop_index(
            op.f("ix_citizenship_citizens_id"),
            table_name="citizenship_citizens",
        )
        op.drop_index(
            op.f("ix_citizenship_citizens_name"),
            table_name="citizenship_citizens",
        )
        op.drop_index(
            op.f("ix_citizenship_citizens_residence_location"),
            table_name="citizenship_citizens",
        )
        op.drop_table("citizenship_citizens")
