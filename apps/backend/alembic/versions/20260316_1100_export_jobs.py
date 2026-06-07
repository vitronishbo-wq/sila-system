"""export jobs persistence

Revision ID: 8c4e3f2ab9cd
Revises: 4fabf7e6d527
Create Date: 2026-03-16 11:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "8c4e3f2ab9cd"
down_revision: str | Sequence[str] | None = "4fabf7e6d527"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names(schema="public"))

    if "export_jobs" not in tables:
        op.create_table(
            "export_jobs",
            sa.Column(
                "id",
                postgresql.UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
                server_default=sa.text("gen_random_uuid()"),
            ),
            sa.Column("module", sa.String(length=50), nullable=False),
            sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
            sa.Column("request_payload", postgresql.JSONB, nullable=True),
            sa.Column("result_data", sa.LargeBinary, nullable=True),
            sa.Column("result_content_type", sa.String(length=100), nullable=True),
            sa.Column("result_filename", sa.String(length=255), nullable=True),
            sa.Column("error", sa.Text(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
        )
        op.create_index("ix_export_jobs_owner_id", "export_jobs", ["owner_id"])
        op.create_index("ix_export_jobs_status", "export_jobs", ["status"])
        op.create_index("ix_export_jobs_created_at", "export_jobs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_export_jobs_created_at", table_name="export_jobs")
    op.drop_index("ix_export_jobs_status", table_name="export_jobs")
    op.drop_index("ix_export_jobs_owner_id", table_name="export_jobs")
    op.drop_table("export_jobs")
