"""
Add import_audit table
"""

from uuid import uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "add_import_audit_table"
down_revision = "20260220_001_create_citizen_documents"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "import_audit",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("source", sa.Text, nullable=False),
        sa.Column("province_code", sa.Text, nullable=False),
        sa.Column("dry_run", sa.Boolean, nullable=False),
        sa.Column("created_municipalities", sa.Integer, default=0),
        sa.Column("updated_municipalities", sa.Integer, default=0),
        sa.Column("created_communes", sa.Integer, default=0),
        sa.Column("updated_communes", sa.Integer, default=0),
        sa.Column("errors", sa.JSON, default=[]),
        sa.Column("executed_at", sa.TIMESTAMP, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("import_audit")
