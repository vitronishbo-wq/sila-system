"""Add hierarchy columns to citizenship_citizens table

Revision ID: 008
Revises: 007
Create Date: 2026-02-24

Add columns to link citizens to their birth and residence locations,
respecting the Lei 14/24 hierarchical structure.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = "008"
down_revision = "007_add_views_performance"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add hierarchy columns to citizenship_citizens."""
    # Adicionar colunas de localização
    op.add_column(
        "citizenship_citizens",
        sa.Column("bi_number", sa.String(20), nullable=False, unique=True),
    )
    op.add_column(
        "citizenship_citizens",
        sa.Column("birth_date", sa.Date(), nullable=False),
    )
    op.add_column(
        "citizenship_citizens",
        sa.Column("birth_location_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "citizenship_citizens",
        sa.Column("residence_location_id", sa.Integer(), nullable=False),
    )
    op.add_column(
        "citizenship_citizens",
        sa.Column("user_id", sa.Integer(), nullable=True, unique=True),
    )
    
    # Criar índices para performance
    op.create_index(
        "ix_citizenship_citizens_bi_number",
        "citizenship_citizens",
        ["bi_number"],
        unique=True,
    )
    op.create_index(
        "ix_citizenship_citizens_residence_location",
        "citizenship_citizens",
        ["residence_location_id"],
    )
    op.create_index(
        "ix_citizenship_citizens_birth_location",
        "citizenship_citizens",
        ["birth_location_id"],
    )
    
    # Criar foreign keys
    op.create_foreign_key(
        "fk_citizenship_citizens_user_id",
        "citizenship_citizens",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_citizenship_citizens_birth_location_id",
        "citizenship_citizens",
        "locations",
        ["birth_location_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_citizenship_citizens_residence_location_id",
        "citizenship_citizens",
        "locations",
        ["residence_location_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    """Remove hierarchy columns from citizenship_citizens."""
    # Remover foreign keys
    op.drop_constraint(
        "fk_citizenship_citizens_residence_location_id",
        "citizenship_citizens",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_citizenship_citizens_birth_location_id",
        "citizenship_citizens",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_citizenship_citizens_user_id",
        "citizenship_citizens",
        type_="foreignkey",
    )
    
    # Remover índices
    op.drop_index("ix_citizenship_citizens_birth_location", "citizenship_citizens")
    op.drop_index("ix_citizenship_citizens_residence_location", "citizenship_citizens")
    op.drop_index("ix_citizenship_citizens_bi_number", "citizenship_citizens")
    
    # Remover colunas
    op.drop_column("citizenship_citizens", "user_id")
    op.drop_column("citizenship_citizens", "residence_location_id")
    op.drop_column("citizenship_citizens", "birth_location_id")
    op.drop_column("citizenship_citizens", "birth_date")
    op.drop_column("citizenship_citizens", "bi_number")
