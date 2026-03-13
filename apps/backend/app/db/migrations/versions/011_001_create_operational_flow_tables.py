"""create operational flow tables

Revision ID: 011_001_create_operational_flow_tables
Revises: 010_002_add_health_indexes
Create Date: 2026-02-27
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = '011_001_create_operational_flow_tables'
down_revision = '010_002_add_health_indexes'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('operational_orders', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('citizen_id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('service_id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('workflow_instance_id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('total_amount', sa.Numeric(12, 2), nullable=False), sa.Column('status', sa.String(length=32), nullable=False), sa.Column('status_history', postgresql.JSONB(astext_type=sa.Text()), nullable=False), sa.Column('receipt_number', sa.String(length=64), nullable=True), sa.Column('proof_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True), sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True), sa.ForeignKeyConstraint(['service_id'], ['services.id'], ondelete='RESTRICT'), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('receipt_number'))
    op.create_index('ix_operational_orders_citizen_id', 'operational_orders', ['citizen_id'], unique=False)
    op.create_index('ix_operational_orders_service_id', 'operational_orders', ['service_id'], unique=False)
    op.create_index('ix_operational_orders_status', 'operational_orders', ['status'], unique=False)
    op.create_index('ix_operational_orders_workflow_instance_id', 'operational_orders', ['workflow_instance_id'], unique=False)
    op.create_table('operational_order_documents', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('filename', sa.String(length=255), nullable=False), sa.Column('content_type', sa.String(length=120), nullable=False), sa.Column('size_bytes', sa.Integer(), nullable=False), sa.Column('uri', sa.String(length=500), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.ForeignKeyConstraint(['order_id'], ['operational_orders.id'], ondelete='CASCADE'), sa.PrimaryKeyConstraint('id'))
    op.create_index('ix_operational_order_documents_order_id', 'operational_order_documents', ['order_id'], unique=False)
    op.create_table('operational_payments', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False), sa.Column('reference', sa.String(length=64), nullable=False), sa.Column('amount', sa.Numeric(12, 2), nullable=False), sa.Column('status', sa.String(length=24), nullable=False), sa.Column('provider', sa.String(length=40), nullable=False), sa.Column('failure_reason', sa.String(length=255), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('confirmed_at', sa.DateTime(timezone=True), nullable=True), sa.ForeignKeyConstraint(['order_id'], ['operational_orders.id'], ondelete='CASCADE'), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('reference'))
    op.create_index('ix_operational_payments_order_id', 'operational_payments', ['order_id'], unique=False)
    op.create_index('ix_operational_payments_reference', 'operational_payments', ['reference'], unique=True)
    op.create_index('ix_operational_payments_status', 'operational_payments', ['status'], unique=False)

def downgrade():
    op.drop_index('ix_operational_payments_status', table_name='operational_payments')
    op.drop_index('ix_operational_payments_reference', table_name='operational_payments')
    op.drop_index('ix_operational_payments_order_id', table_name='operational_payments')
    op.drop_table('operational_payments')
    op.drop_index('ix_operational_order_documents_order_id', table_name='operational_order_documents')
    op.drop_table('operational_order_documents')
    op.drop_index('ix_operational_orders_workflow_instance_id', table_name='operational_orders')
    op.drop_index('ix_operational_orders_status', table_name='operational_orders')
    op.drop_index('ix_operational_orders_service_id', table_name='operational_orders')
    op.drop_index('ix_operational_orders_citizen_id', table_name='operational_orders')
    op.drop_table('operational_orders')