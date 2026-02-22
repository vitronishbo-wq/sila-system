"""
Add pgcrypto extension to support bcrypt crypt() in SQL

Revision ID: a1b2c3d4e5f6
Revises: 74535044d6a9
Create Date: 2025-10-16 20:35:00.000000
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "74535044d6a9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Safe on idempotency; will not fail if already installed
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")


def downgrade() -> None:
    # Warning: dropping the extension may fail if other objects depend on it
    op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
