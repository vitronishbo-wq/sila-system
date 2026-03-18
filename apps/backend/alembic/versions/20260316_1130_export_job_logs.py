"""export job logs

Revision ID: 9a1d2b7c3e10
Revises: 8c4e3f2ab9cd
Create Date: 2026-03-16 11:30:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '9a1d2b7c3e10'
down_revision: Union[str, Sequence[str], None] = '8c4e3f2ab9cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names(schema="public"))

    if "export_job_logs" not in tables:
        op.create_table(
            "export_job_logs",
            sa.Column(
                "id",
                postgresql.UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
                server_default=sa.text("gen_random_uuid()"),
            ),
            sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("level", sa.String(length=20), nullable=False, server_default="info"),
            sa.Column("message", sa.Text(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(["job_id"], ["export_jobs.id"], ondelete="CASCADE"),
        )
        op.create_index("ix_export_job_logs_job_id", "export_job_logs", ["job_id"])
        op.create_index("ix_export_job_logs_created_at", "export_job_logs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_export_job_logs_created_at", table_name="export_job_logs")
    op.drop_index("ix_export_job_logs_job_id", table_name="export_job_logs")
    op.drop_table("export_job_logs")
