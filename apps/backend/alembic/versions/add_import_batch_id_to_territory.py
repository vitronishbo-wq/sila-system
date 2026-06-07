"""
Add import_batch_id to territory table
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "add_import_batch_id_to_territory"
down_revision = "add_import_audit_table"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "territory" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("territory")}
    if "import_batch_id" in existing_columns:
        return

    op.add_column(
        "territory",
        sa.Column("import_batch_id", sa.UUID(as_uuid=True), nullable=True),
    )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "territory" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("territory")}
    if "import_batch_id" not in existing_columns:
        return

    op.drop_column("territory", "import_batch_id")
