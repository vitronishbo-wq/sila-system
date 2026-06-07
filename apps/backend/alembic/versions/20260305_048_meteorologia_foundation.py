"""create meteorologia foundation tables

Revision ID: 20260305_048_meteorologia_foundation
Revises: 20260305_048_justica_add_materia_processual
Create Date: 2026-03-05 16:10:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "20260305_048_meteorologia_foundation"
down_revision = "20260305_048_justica_add_materia_processual"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "meteorologia_estacoes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("codigo", sa.String(length=30), nullable=False),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("altitude", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="ACTIVE"),
        sa.Column("municipio", sa.String(length=120), nullable=True),
        sa.Column("provincia", sa.String(length=120), nullable=True),
        sa.Column("metadata", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "latitude >= -90 AND latitude <= 90", name="ck_meteorologia_estacoes_latitude"
        ),
        sa.CheckConstraint(
            "longitude >= -180 AND longitude <= 180", name="ck_meteorologia_estacoes_longitude"
        ),
    )
    op.create_index(
        "ix_meteorologia_estacoes_codigo", "meteorologia_estacoes", ["codigo"], unique=True
    )
    op.create_index(
        "ix_meteorologia_estacoes_status", "meteorologia_estacoes", ["status"], unique=False
    )
    op.create_index(
        "ix_meteorologia_estacoes_municipio", "meteorologia_estacoes", ["municipio"], unique=False
    )
    op.create_index(
        "ix_meteorologia_estacoes_provincia", "meteorologia_estacoes", ["provincia"], unique=False
    )
    op.create_index(
        "ix_meteorologia_estacoes_deleted_at", "meteorologia_estacoes", ["deleted_at"], unique=False
    )
    op.create_index(
        "idx_meteorologia_estacoes_status_provincia",
        "meteorologia_estacoes",
        ["status", "provincia"],
        unique=False,
    )

    op.create_table(
        "meteorologia_observacoes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("estacao_id", UUID(as_uuid=True), nullable=False),
        sa.Column("data_observacao", sa.DateTime(timezone=True), nullable=False),
        sa.Column("temperatura", sa.Float(), nullable=True),
        sa.Column("humidade", sa.Float(), nullable=True),
        sa.Column("pressao", sa.Float(), nullable=True),
        sa.Column("velocidade_vento", sa.Float(), nullable=True),
        sa.Column("direcao_vento", sa.Float(), nullable=True),
        sa.Column("precipitacao", sa.Float(), nullable=True),
        sa.Column("radiacao_solar", sa.Float(), nullable=True),
        sa.Column("tipo", sa.String(length=20), nullable=False, server_default="SURFACE"),
        sa.Column(
            "qualidade_dados", sa.String(length=20), nullable=False, server_default="VALIDADO"
        ),
        sa.Column("has_alerts", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("alertas", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("metadata", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(["estacao_id"], ["meteorologia_estacoes.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_meteorologia_observacoes_estacao_id",
        "meteorologia_observacoes",
        ["estacao_id"],
        unique=False,
    )
    op.create_index(
        "ix_meteorologia_observacoes_data_observacao",
        "meteorologia_observacoes",
        ["data_observacao"],
        unique=False,
    )
    op.create_index(
        "ix_meteorologia_observacoes_has_alerts",
        "meteorologia_observacoes",
        ["has_alerts"],
        unique=False,
    )
    op.create_index(
        "ix_meteorologia_observacoes_created_at",
        "meteorologia_observacoes",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        "idx_meteorologia_obs_estacao_data",
        "meteorologia_observacoes",
        ["estacao_id", "data_observacao"],
        unique=False,
    )
    op.create_index(
        "idx_meteorologia_obs_alertas_true",
        "meteorologia_observacoes",
        ["created_at"],
        unique=False,
        postgresql_where=sa.text("has_alerts IS TRUE"),
    )


def downgrade() -> None:
    op.drop_index("idx_meteorologia_obs_alertas_true", table_name="meteorologia_observacoes")
    op.drop_index("idx_meteorologia_obs_estacao_data", table_name="meteorologia_observacoes")
    op.drop_index("ix_meteorologia_observacoes_created_at", table_name="meteorologia_observacoes")
    op.drop_index("ix_meteorologia_observacoes_has_alerts", table_name="meteorologia_observacoes")
    op.drop_index(
        "ix_meteorologia_observacoes_data_observacao", table_name="meteorologia_observacoes"
    )
    op.drop_index("ix_meteorologia_observacoes_estacao_id", table_name="meteorologia_observacoes")
    op.drop_table("meteorologia_observacoes")

    op.drop_index("idx_meteorologia_estacoes_status_provincia", table_name="meteorologia_estacoes")
    op.drop_index("ix_meteorologia_estacoes_deleted_at", table_name="meteorologia_estacoes")
    op.drop_index("ix_meteorologia_estacoes_provincia", table_name="meteorologia_estacoes")
    op.drop_index("ix_meteorologia_estacoes_municipio", table_name="meteorologia_estacoes")
    op.drop_index("ix_meteorologia_estacoes_status", table_name="meteorologia_estacoes")
    op.drop_index("ix_meteorologia_estacoes_codigo", table_name="meteorologia_estacoes")
    op.drop_table("meteorologia_estacoes")
