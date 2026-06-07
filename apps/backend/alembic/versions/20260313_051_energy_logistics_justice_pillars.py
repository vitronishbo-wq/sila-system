"""create energy, logistics, and justice persistence pillars

Revision ID: 20260313_051_energy_logistics_justice_pillars
Revises: 20260306_050_defesa_consumidor_reclamacoes
Create Date: 2026-03-13 09:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "20260313_051_energy_logistics_justice_pillars"
down_revision = "20260306_050_defesa_consumidor_reclamacoes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "energy_telemetry",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("sensor_id", sa.String(length=50), nullable=False),
        sa.Column("load_kw", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_energy_telemetry_sensor_id", "energy_telemetry", ["sensor_id"], unique=False
    )
    op.create_index(
        "ix_energy_telemetry_timestamp", "energy_telemetry", ["timestamp"], unique=False
    )

    op.create_table(
        "energy_invoices",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("numero_fatura", sa.String(length=64), nullable=False),
        sa.Column("consumo_id", UUID(as_uuid=True), nullable=False),
        sa.Column("unidade_consumidora_id", UUID(as_uuid=True), nullable=False),
        sa.Column("cpf_titular", sa.String(length=32), nullable=False),
        sa.Column("mes_referencia", sa.String(length=16), nullable=False),
        sa.Column("consumo_kwh", sa.Numeric(14, 3), nullable=False),
        sa.Column("tarifa_kwh", sa.Numeric(14, 6), nullable=False),
        sa.Column("bandeira_tarifaria", sa.String(length=32), nullable=False),
        sa.Column("valor_consumo", sa.Numeric(14, 2), nullable=False),
        sa.Column("valor_bandeira", sa.Numeric(14, 2), nullable=False),
        sa.Column("valor_iluminacao_publica", sa.Numeric(14, 2), nullable=False),
        sa.Column("valor_total", sa.Numeric(14, 2), nullable=False),
        sa.Column("data_emissao", sa.Date(), nullable=False),
        sa.Column("data_vencimento", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("data_pagamento", sa.Date(), nullable=True),
        sa.Column("valor_pago", sa.Numeric(14, 2), nullable=True),
        sa.Column("metodo_pagamento", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.UniqueConstraint("numero_fatura", name="uq_energy_invoices_numero_fatura"),
    )
    op.create_index(
        "ix_energy_invoices_cpf_titular", "energy_invoices", ["cpf_titular"], unique=False
    )
    op.create_index(
        "ix_energy_invoices_consumo_id", "energy_invoices", ["consumo_id"], unique=False
    )
    op.create_index(
        "ix_energy_invoices_unidade_consumidora_id",
        "energy_invoices",
        ["unidade_consumidora_id"],
        unique=False,
    )
    op.create_index("ix_energy_invoices_status", "energy_invoices", ["status"], unique=False)
    op.create_index(
        "ix_energy_invoices_mes_referencia", "energy_invoices", ["mes_referencia"], unique=False
    )

    op.create_table(
        "toll_passages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("vehicle_did", sa.String(length=128), nullable=False),
        sa.Column("gantry_id", sa.String(length=64), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="Kz"),
        sa.Column(
            "category", sa.String(length=64), nullable=False, server_default="TRANSPORT_TOLL"
        ),
        sa.Column(
            "occurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_index("ix_toll_passages_vehicle_did", "toll_passages", ["vehicle_did"], unique=False)
    op.create_index("ix_toll_passages_gantry_id", "toll_passages", ["gantry_id"], unique=False)
    op.create_index("ix_toll_passages_occurred_at", "toll_passages", ["occurred_at"], unique=False)

    op.create_table(
        "traffic_violations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("citizen_id", UUID(as_uuid=True), nullable=True),
        sa.Column("vehicle_plate", sa.String(length=32), nullable=True),
        sa.Column("violation_code", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("fine_amount", sa.Numeric(14, 2), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="Kz"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("issued_by", sa.String(length=100), nullable=True),
        sa.Column("source_service", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_index(
        "ix_traffic_violations_citizen_id", "traffic_violations", ["citizen_id"], unique=False
    )
    op.create_index(
        "ix_traffic_violations_vehicle_plate", "traffic_violations", ["vehicle_plate"], unique=False
    )
    op.create_index(
        "ix_traffic_violations_violation_code",
        "traffic_violations",
        ["violation_code"],
        unique=False,
    )
    op.create_index("ix_traffic_violations_status", "traffic_violations", ["status"], unique=False)
    op.create_index(
        "ix_traffic_violations_occurred_at", "traffic_violations", ["occurred_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_traffic_violations_occurred_at", table_name="traffic_violations")
    op.drop_index("ix_traffic_violations_status", table_name="traffic_violations")
    op.drop_index("ix_traffic_violations_violation_code", table_name="traffic_violations")
    op.drop_index("ix_traffic_violations_vehicle_plate", table_name="traffic_violations")
    op.drop_index("ix_traffic_violations_citizen_id", table_name="traffic_violations")
    op.drop_table("traffic_violations")

    op.drop_index("ix_toll_passages_occurred_at", table_name="toll_passages")
    op.drop_index("ix_toll_passages_gantry_id", table_name="toll_passages")
    op.drop_index("ix_toll_passages_vehicle_did", table_name="toll_passages")
    op.drop_table("toll_passages")

    op.drop_index("ix_energy_invoices_mes_referencia", table_name="energy_invoices")
    op.drop_index("ix_energy_invoices_status", table_name="energy_invoices")
    op.drop_index("ix_energy_invoices_unidade_consumidora_id", table_name="energy_invoices")
    op.drop_index("ix_energy_invoices_consumo_id", table_name="energy_invoices")
    op.drop_index("ix_energy_invoices_cpf_titular", table_name="energy_invoices")
    op.drop_table("energy_invoices")

    op.drop_index("ix_energy_telemetry_timestamp", table_name="energy_telemetry")
    op.drop_index("ix_energy_telemetry_sensor_id", table_name="energy_telemetry")
    op.drop_table("energy_telemetry")
