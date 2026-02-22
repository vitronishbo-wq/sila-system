"""create iam tables

Revision ID: 001_create_iam_tables
Revises: 
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '001_create_iam_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table(
        'iam_users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING_VERIFICATION'),
        sa.Column('is_superuser', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('department', sa.String(255), nullable=True),
        sa.Column('position', sa.String(255), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer, nullable=False, server_default='0'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_ip', sa.String(50), nullable=True),
        sa.Column('password_changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('password_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('mfa_enabled', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('mfa_secret', sa.String(255), nullable=True),
        sa.Column('mfa_type', sa.String(50), nullable=False, server_default='NONE'),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_iam_users_username', 'iam_users', ['username'], unique=True)
    op.create_index('ix_iam_users_email', 'iam_users', ['email'], unique=True)
    op.create_index('ix_iam_users_status', 'iam_users', ['status'])
    op.create_index('ix_iam_users_username_lower', 'iam_users', [sa.text('lower(username)')])
    op.create_index('ix_iam_users_email_lower', 'iam_users', [sa.text('lower(email)')])
    op.create_index('ix_iam_users_status_created', 'iam_users', ['status', 'created_at'])

    # Create roles table
    op.create_table(
        'iam_roles',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('role_type', sa.String(50), nullable=False, server_default='CUSTOM'),
        sa.Column('is_system', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_iam_roles_name', 'iam_roles', ['name'], unique=True)
    op.create_index('ix_iam_roles_type', 'iam_roles', ['role_type'])

    # Create permissions table
    op.create_table(
        'iam_permissions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('module', sa.String(50), nullable=False),
        sa.Column('resource', sa.String(50), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('scope', sa.String(50), nullable=False, server_default='OWN'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_system', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('module', 'resource', 'action', name='uq_permission_components')
    )
    op.create_index('ix_iam_permissions_code', 'iam_permissions', ['code'], unique=True)
    op.create_index('ix_iam_permissions_module', 'iam_permissions', ['module'])
    op.create_index('ix_iam_permissions_resource', 'iam_permissions', ['resource'])
    op.create_index('ix_iam_permissions_action', 'iam_permissions', ['action'])
    op.create_index('ix_iam_permissions_module_resource', 'iam_permissions', ['module', 'resource'])
    op.create_index('ix_iam_permissions_resource_action', 'iam_permissions', ['resource', 'action'])

    # Create user_roles association table
    op.create_table(
        'iam_user_roles',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('role_id', sa.String(36), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('assigned_by', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['user_id'], ['iam_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['iam_roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_by'], ['iam_users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'role_id', name='uq_user_role')
    )
    op.create_index('ix_iam_user_roles_user', 'iam_user_roles', ['user_id'])
    op.create_index('ix_iam_user_roles_role', 'iam_user_roles', ['role_id'])

    # Create role_permissions association table
    op.create_table(
        'iam_role_permissions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('role_id', sa.String(36), nullable=False),
        sa.Column('permission_id', sa.String(36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['role_id'], ['iam_roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['iam_permissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('role_id', 'permission_id', name='uq_role_permission')
    )
    op.create_index('ix_iam_role_permissions_role', 'iam_role_permissions', ['role_id'])
    op.create_index('ix_iam_role_permissions_permission', 'iam_role_permissions', ['permission_id'])

    # Create user_permissions table (direct assignments)
    op.create_table(
        'iam_user_permissions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('permission_id', sa.String(36), nullable=False),
        sa.Column('granted_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('granted_by', sa.String(36), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['user_id'], ['iam_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['iam_permissions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['granted_by'], ['iam_users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'permission_id', name='uq_user_permission')
    )
    op.create_index('ix_iam_user_permissions_user', 'iam_user_permissions', ['user_id'])
    op.create_index('ix_iam_user_permissions_permission', 'iam_user_permissions', ['permission_id'])
    op.create_index('ix_iam_user_permissions_expires', 'iam_user_permissions', ['expires_at'])

    # Create refresh_tokens table
    op.create_table(
        'iam_refresh_tokens',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('token_hash', sa.String(128), nullable=False),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['user_id'], ['iam_users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_iam_refresh_tokens_token_hash', 'iam_refresh_tokens', ['token_hash'], unique=True)
    op.create_index('ix_iam_refresh_tokens_user', 'iam_refresh_tokens', ['user_id', 'expires_at'])
    op.create_index('ix_iam_refresh_tokens_expires', 'iam_refresh_tokens', ['expires_at'])
    op.create_index('ix_iam_refresh_tokens_revoked', 'iam_refresh_tokens', ['revoked'])

    # Create sessions table
    op.create_table(
        'iam_sessions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('refresh_token_id', sa.String(36), nullable=False),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('device_id', sa.String(255), nullable=True),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['iam_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['refresh_token_id'], ['iam_refresh_tokens.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_iam_sessions_user', 'iam_sessions', ['user_id'])
    op.create_index('ix_iam_sessions_user_active', 'iam_sessions', ['user_id', 'is_active'])
    op.create_index('ix_iam_sessions_expires', 'iam_sessions', ['expires_at'])
    op.create_index('ix_iam_sessions_last_activity', 'iam_sessions', ['last_activity_at'])

    # Create audit_logs table
    op.create_table(
        'iam_audit_logs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('username', sa.String(100), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('resource', sa.String(50), nullable=False),
        sa.Column('resource_id', sa.String(36), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('details', JSONB(), nullable=True),
        sa.Column('success', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['user_id'], ['iam_users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_iam_audit_logs_user_time', 'iam_audit_logs', ['user_id', 'created_at'])
    op.create_index('ix_iam_audit_logs_resource_time', 'iam_audit_logs', ['resource', 'resource_id', 'created_at'])
    op.create_index('ix_iam_audit_logs_action_time', 'iam_audit_logs', ['action', 'created_at'])
    op.create_index('ix_iam_audit_logs_search', 'iam_audit_logs', ['created_at', 'user_id', 'action'])
    op.create_index('ix_iam_audit_logs_created_at', 'iam_audit_logs', ['created_at'])

    # Create token_blacklist table
    op.create_table(
        'iam_token_blacklist',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('token_jti', sa.String(128), nullable=False),
        sa.Column('token_type', sa.String(20), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('revoked_by', sa.String(36), nullable=True),
        sa.Column('reason', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['revoked_by'], ['iam_users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_iam_token_blacklist_jti', 'iam_token_blacklist', ['token_jti'], unique=True)
    op.create_index('ix_iam_token_blacklist_expires', 'iam_token_blacklist', ['expires_at'])


def downgrade():
    op.drop_table('iam_token_blacklist')
    op.drop_table('iam_audit_logs')
    op.drop_table('iam_sessions')
    op.drop_table('iam_refresh_tokens')
    op.drop_table('iam_user_permissions')
    op.drop_table('iam_role_permissions')
    op.drop_table('iam_user_roles')
    op.drop_table('iam_permissions')
    op.drop_table('iam_roles')
    op.drop_table('iam_users')
