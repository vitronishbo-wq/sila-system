"""Add territory_id, role, level to iam_users

Revision ID: 06cf90ab5741
Revises: c9ee6f47b996
Create Date: 2026-02-21 22:41:08.854788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06cf90ab5741'
down_revision: Union[str, Sequence[str], None] = 'c9ee6f47b996'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add territory_id column with FK to territories
    op.add_column(
        'iam_users',
        sa.Column('territory_id', sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        'fk_iam_users_territory_id',
        'iam_users',
        'territories',
        ['territory_id'],
        ['id'],
        ondelete='SET NULL'
    )
    op.create_index('ix_iam_users_territory_id', 'iam_users', ['territory_id'])
    
    # Add role column (VARCHAR for flexibility in RBAC evolution)
    op.add_column(
        'iam_users',
        sa.Column('role', sa.String(100), nullable=True)
    )
    op.create_index('ix_iam_users_role', 'iam_users', ['role'])
    
    # Add level column (redundant but useful for JWT claims and performance)
    op.add_column(
        'iam_users',
        sa.Column('level', sa.String(50), nullable=True)
    )
    op.create_index('ix_iam_users_level', 'iam_users', ['level'])


def downgrade() -> None:
    op.drop_index('ix_iam_users_level', table_name='iam_users')
    op.drop_column('iam_users', 'level')
    
    op.drop_index('ix_iam_users_role', table_name='iam_users')
    op.drop_column('iam_users', 'role')
    
    op.drop_index('ix_iam_users_territory_id', table_name='iam_users')
    op.drop_constraint('fk_iam_users_territory_id', 'iam_users', type_='foreignkey')
    op.drop_column('iam_users', 'territory_id')
