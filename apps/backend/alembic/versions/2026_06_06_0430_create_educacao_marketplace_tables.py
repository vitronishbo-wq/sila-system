"""create educacao marketplace tables (institutions, vacancies, seat_reservations)

Revision ID: 20260606_0430_create_educacao_marketplace_tables
Revises: 20260606_0400_create_educacao_wizard_matricula
Create Date: 2026-06-06 04:30:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "20260606_0430_create_educacao_marketplace_tables"
down_revision = "20260606_0400_create_educacao_wizard_matricula"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "educacao_marketplace_institutions",
        sa.Column("id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("institution_id", UUID(as_uuid=True), nullable=False, index=True, unique=True),
        sa.Column("nome", sa.String(255), nullable=False, index=True),
        sa.Column("tipo", sa.String(32), nullable=False),
        sa.Column("nivel_ensino", sa.String(64), nullable=False, index=True),
        sa.Column("provincia", sa.String(128), nullable=False, index=True),
        sa.Column("municipio", sa.String(128), nullable=False, index=True),
        sa.Column("bairro", sa.String(128), nullable=True),
        sa.Column("latitude", sa.Float, nullable=True),
        sa.Column("longitude", sa.Float, nullable=True),
        sa.Column("turnos", sa.String(128), nullable=False, server_default="manha,tarde"),
        sa.Column("contactos", sa.Text, nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="activa"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    op.create_table(
        "educacao_marketplace_vacancies",
        sa.Column("id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("institution_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("ano_letivo", sa.String(32), nullable=False, index=True),
        sa.Column("classe", sa.String(32), nullable=False, index=True),
        sa.Column("turno", sa.String(32), nullable=False),
        sa.Column("vagas_totais", sa.Integer, nullable=False, server_default="0"),
        sa.Column("vagas_ocupadas", sa.Integer, nullable=False, server_default="0"),
        sa.Column("vagas_disponiveis", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.UniqueConstraint("institution_id", "ano_letivo", "classe", "turno", name="uq_marketplace_vacancy"),
    )

    op.create_table(
        "educacao_seat_reservations",
        sa.Column("id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("student_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("institution_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("classe", sa.String(32), nullable=False),
        sa.Column("turno", sa.String(32), nullable=False, server_default="manha"),
        sa.Column("ano_letivo", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="activa"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table("educacao_seat_reservations")
    op.drop_table("educacao_marketplace_vacancies")
    op.drop_table("educacao_marketplace_institutions")
