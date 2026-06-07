"""create estatistica enterprise tables

Revision ID: 20260305_047_estatistica_enterprise_foundation
Revises: 20260305_046_cultura_slice3_espacos_projetos_editais
Create Date: 2026-03-05 09:10:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260305_047_estatistica_enterprise_foundation"
down_revision = "20260305_046_cultura_slice3_espacos_projetos_editais"
branch_labels = None
depends_on = None


def _create_named_table(table_name: str) -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("conteudo", sa.JSON(), nullable=True),
        sa.Column(
            "data_criacao", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("data_atualizacao", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(f"ix_{table_name}_nome", table_name, ["nome"], unique=False)


def upgrade() -> None:
    op.create_table(
        "est_metricas",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("tipo", sa.String(length=40), nullable=False),
        sa.Column("unidade", sa.String(length=50), nullable=False),
        sa.Column("fonte_dados", sa.String(length=60), nullable=False),
        sa.Column("periodicidade", sa.String(length=40), nullable=False),
        sa.Column("formula", sa.String(length=500), nullable=True),
        sa.Column("parametros", sa.JSON(), nullable=True),
        sa.Column("valor_atual", sa.Float(), nullable=True),
        sa.Column("valor_anterior", sa.Float(), nullable=True),
        sa.Column("variacao_percentual", sa.Float(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "data_criacao", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("data_atualizacao", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ultima_atualizacao", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_est_metricas_nome", "est_metricas", ["nome"], unique=True)
    op.create_index("ix_est_metricas_tipo", "est_metricas", ["tipo"], unique=False)
    op.create_index("ix_est_metricas_fonte_dados", "est_metricas", ["fonte_dados"], unique=False)
    op.create_index(
        "ix_est_metricas_periodicidade", "est_metricas", ["periodicidade"], unique=False
    )
    op.create_index("ix_est_metricas_ativo", "est_metricas", ["ativo"], unique=False)

    op.create_table(
        "est_kpis",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column(
            "metrica_id",
            sa.Integer(),
            sa.ForeignKey("est_metricas.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("valor_alvo", sa.Float(), nullable=True),
        sa.Column("valor_atual", sa.Float(), nullable=True),
        sa.Column("valor_anterior", sa.Float(), nullable=True),
        sa.Column("unidade", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="ativo"),
        sa.Column("peso", sa.Float(), nullable=False, server_default="1"),
        sa.Column("limite_inferior", sa.Float(), nullable=True),
        sa.Column("limite_superior", sa.Float(), nullable=True),
        sa.Column(
            "data_criacao", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("data_atualizacao", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_est_kpis_nome", "est_kpis", ["nome"], unique=True)
    op.create_index("ix_est_kpis_metrica_id", "est_kpis", ["metrica_id"], unique=False)
    op.create_index("ix_est_kpis_status", "est_kpis", ["status"], unique=False)

    op.create_table(
        "est_timeseries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "metrica_id",
            sa.Integer(),
            sa.ForeignKey("est_metricas.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valor", sa.Float(), nullable=False),
        sa.Column("dimensao_1", sa.String(length=100), nullable=True),
        sa.Column("dimensao_2", sa.String(length=100), nullable=True),
        sa.Column("dimensao_3", sa.String(length=100), nullable=True),
        sa.Column("origem", sa.String(length=100), nullable=True),
        sa.Column(
            "criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_est_timeseries_metrica_id", "est_timeseries", ["metrica_id"], unique=False)
    op.create_index("ix_est_timeseries_timestamp", "est_timeseries", ["timestamp"], unique=False)
    op.create_index(
        "ix_est_timeseries_metrica_timestamp",
        "est_timeseries",
        ["metrica_id", "timestamp"],
        unique=False,
    )
    op.create_index(
        "ix_est_timeseries_dimensoes",
        "est_timeseries",
        ["dimensao_1", "dimensao_2", "dimensao_3"],
        unique=False,
    )

    op.create_table(
        "est_dashboards",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("tipo", sa.String(length=40), nullable=False),
        sa.Column("configuracoes", sa.JSON(), nullable=True),
        sa.Column("kpi_ids", sa.JSON(), nullable=False),
        sa.Column("criado_por", sa.Integer(), nullable=True),
        sa.Column(
            "data_criacao", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("data_atualizacao", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_est_dashboards_nome", "est_dashboards", ["nome"], unique=False)
    op.create_index("ix_est_dashboards_tipo", "est_dashboards", ["tipo"], unique=False)

    for name in [
        "est_relatorios",
        "est_indicadores",
        "est_agregacoes",
        "est_exportacoes",
        "est_analises",
        "est_previsoes",
        "est_comparativos",
        "est_rankings",
        "est_tendencias",
        "est_alertas",
    ]:
        _create_named_table(name)

    op.create_table(
        "est_outbox_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("event_name", sa.String(length=120), nullable=False),
        sa.Column("aggregate_type", sa.String(length=120), nullable=False),
        sa.Column("aggregate_id", sa.String(length=120), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_est_outbox_events_event_name", "est_outbox_events", ["event_name"], unique=False
    )
    op.create_index(
        "ix_est_outbox_events_aggregate_type", "est_outbox_events", ["aggregate_type"], unique=False
    )
    op.create_index(
        "ix_est_outbox_events_aggregate_id", "est_outbox_events", ["aggregate_id"], unique=False
    )
    op.create_index("ix_est_outbox_events_status", "est_outbox_events", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_est_outbox_events_status", table_name="est_outbox_events")
    op.drop_index("ix_est_outbox_events_aggregate_id", table_name="est_outbox_events")
    op.drop_index("ix_est_outbox_events_aggregate_type", table_name="est_outbox_events")
    op.drop_index("ix_est_outbox_events_event_name", table_name="est_outbox_events")
    op.drop_table("est_outbox_events")

    for name in [
        "est_alertas",
        "est_tendencias",
        "est_rankings",
        "est_comparativos",
        "est_previsoes",
        "est_analises",
        "est_exportacoes",
        "est_agregacoes",
        "est_indicadores",
        "est_relatorios",
    ]:
        op.drop_index(f"ix_{name}_nome", table_name=name)
        op.drop_table(name)

    op.drop_index("ix_est_dashboards_tipo", table_name="est_dashboards")
    op.drop_index("ix_est_dashboards_nome", table_name="est_dashboards")
    op.drop_table("est_dashboards")

    op.drop_index("ix_est_timeseries_dimensoes", table_name="est_timeseries")
    op.drop_index("ix_est_timeseries_metrica_timestamp", table_name="est_timeseries")
    op.drop_index("ix_est_timeseries_timestamp", table_name="est_timeseries")
    op.drop_index("ix_est_timeseries_metrica_id", table_name="est_timeseries")
    op.drop_table("est_timeseries")

    op.drop_index("ix_est_kpis_status", table_name="est_kpis")
    op.drop_index("ix_est_kpis_metrica_id", table_name="est_kpis")
    op.drop_index("ix_est_kpis_nome", table_name="est_kpis")
    op.drop_table("est_kpis")

    op.drop_index("ix_est_metricas_ativo", table_name="est_metricas")
    op.drop_index("ix_est_metricas_periodicidade", table_name="est_metricas")
    op.drop_index("ix_est_metricas_fonte_dados", table_name="est_metricas")
    op.drop_index("ix_est_metricas_tipo", table_name="est_metricas")
    op.drop_index("ix_est_metricas_nome", table_name="est_metricas")
    op.drop_table("est_metricas")
