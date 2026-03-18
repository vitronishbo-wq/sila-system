"""Create audit_logs table for core audit system

Revision ID: 20260316_054_create_audit_logs
Revises: 4b8e10487f5a
Create Date: 2026-03-16 10:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID, ENUM

# revision identifiers, used by Alembic.
revision: str = "20260316_054_create_audit_logs"
down_revision: str = "4b8e10487f5a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create audit_logs table with proper indexing and constraints."""
    
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names(schema="public"))
    
    # Only create table if it doesn't exist
    if 'audit_logs' not in tables:
        # Create main audit_logs table using string columns instead of enums
        # to avoid conflicts with existing enum types
        op.create_table(
            'audit_logs',
            sa.Column('audit_id', UUID(as_uuid=True), primary_key=True, nullable=False),
            sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column('user_id', sa.String(length=255), nullable=True),
            sa.Column('module', sa.String(length=100), nullable=True),
            sa.Column('action', sa.String(length=50), nullable=False),  # Store as string
            sa.Column('status', sa.String(length=50), nullable=False),  # Store as string
            sa.Column('request_path', sa.String(length=500), nullable=True),
            sa.Column('result_code', sa.Integer(), nullable=True),
            sa.Column('result_message', sa.Text(), nullable=True),
            sa.Column('severity', sa.String(length=20), nullable=False, server_default='INFO'),  # Store as string
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        
        # Create indices for efficient querying
        op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'], unique=False)
        op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'], unique=False)
        op.create_index('ix_audit_logs_module', 'audit_logs', ['module'], unique=False)
        op.create_index('ix_audit_logs_action', 'audit_logs', ['action'], unique=False)
        op.create_index('ix_audit_logs_status', 'audit_logs', ['status'], unique=False)
        op.create_index('ix_audit_logs_severity', 'audit_logs', ['severity'], unique=False)
        
        # Composite index for common queries
        op.create_index(
            'ix_audit_logs_user_timestamp',
            'audit_logs',
            ['user_id', 'timestamp'],
            unique=False
        )
        op.create_index(
            'ix_audit_logs_module_action',
            'audit_logs',
            ['module', 'action'],
            unique=False
        )


def downgrade() -> None:
    """Drop audit_logs table and ENUM types."""
    
    # Drop indices
    op.drop_index('ix_audit_logs_module_action', table_name='audit_logs')
    op.drop_index('ix_audit_logs_user_timestamp', table_name='audit_logs')
    op.drop_index('ix_audit_logs_severity', table_name='audit_logs')
    op.drop_index('ix_audit_logs_status', table_name='audit_logs')
    op.drop_index('ix_audit_logs_action', table_name='audit_logs')
    op.drop_index('ix_audit_logs_module', table_name='audit_logs')
    op.drop_index('ix_audit_logs_user_id', table_name='audit_logs')
    op.drop_index('ix_audit_logs_timestamp', table_name='audit_logs')
    
    # Drop table
    op.drop_table('audit_logs')
    
    # Drop ENUM types
    audit_severity_enum = ENUM('INFO', 'ERROR', 'CRITICAL', name='audit_severity')
    audit_severity_enum.drop(op.get_bind(), checkfirst=True)
    
    audit_status_enum = ENUM('INITIATED', 'COMPLETED', 'FAILED', name='audit_status')
    audit_status_enum.drop(op.get_bind(), checkfirst=True)
    
    audit_action_enum = ENUM('CREATE', 'READ', 'UPDATE', 'DELETE', 'APPROVE', 'LOGIN', name='audit_action')
    audit_action_enum.drop(op.get_bind(), checkfirst=True)
