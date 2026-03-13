"""
Add import_batch_id to territory table
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "add_import_batch_id_to_territory"
down_revision = "add_import_audit_table"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        "territory",
        sa.Column("import_batch_id", sa.UUID(as_uuid=True), nullable=True),
    )

def downgrade():
    op.drop_column("territory", "import_batch_id")
