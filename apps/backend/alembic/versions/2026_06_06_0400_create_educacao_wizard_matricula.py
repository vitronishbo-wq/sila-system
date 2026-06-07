"""create educacao_wizard_matricula table

Revision ID: 20260606_0400_create_educacao_wizard_matricula
Revises: 20260527_001_marketplace_institution_projection
Create Date: 2026-06-06 04:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "20260606_0400_create_educacao_wizard_matricula"
down_revision = "20260527_001_marketplace_institution_projection"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "educacao_wizard_matricula",
        sa.Column("id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("citizen_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("status", sa.String(24), nullable=False, default="em_curso", index=True),
        sa.Column("passo_atual", sa.Integer, nullable=False, default=1),
        sa.Column("dados_estudante", JSONB, nullable=True),
        sa.Column("dados_encarregado", JSONB, nullable=True),
        sa.Column("selecao_escola", JSONB, nullable=True),
        sa.Column("documentos", JSONB, nullable=True),
        sa.Column("resultado_elegibilidade", JSONB, nullable=True),
        sa.Column("pagamento", JSONB, nullable=True),
        sa.Column("matricula_id", UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            onupdate=sa.func.now(),
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table("educacao_wizard_matricula")
