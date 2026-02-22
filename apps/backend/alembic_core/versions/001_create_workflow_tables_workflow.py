"""create workflow tables

Revision ID: 001_create_workflow_tables
Revises: 
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

revision = '001_create_workflow_tables'
# Set down_revision to the current alembic head to chain the migration
down_revision = '30a2bcc8c697'
branch_labels = None
depends_on = None


def upgrade():
    # wf_definitions
    op.create_table(
        'wf_definitions',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('is_public', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('timeout_hours', sa.Integer, nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('tags', ARRAY(sa.String), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.Column('created_by', UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wf_definitions_code', 'wf_definitions', ['code'])
    op.create_index('ix_wf_definitions_code_version', 'wf_definitions', ['code', 'version'], unique=True)
    op.create_index('ix_wf_definitions_entity_type', 'wf_definitions', ['entity_type'])

    # wf_states
    op.create_table(
        'wf_states',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('workflow_id', UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_initial', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('is_final', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('is_auto_forward', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('timeout_hours', sa.Integer, nullable=True),
        sa.Column('form_schema', JSONB(), nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['workflow_id'], ['wf_definitions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wf_states_workflow_code', 'wf_states', ['workflow_id', 'code'], unique=True)

    # wf_transitions
    op.create_table(
        'wf_transitions',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('workflow_id', UUID(as_uuid=True), nullable=False),
        sa.Column('from_state_id', UUID(as_uuid=True), nullable=False),
        sa.Column('to_state_id', UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('transition_type', sa.String(50), nullable=False, server_default='USER'),
        sa.Column('assignment_type', sa.String(50), nullable=False, server_default='ROLE'),
        sa.Column('assignment_value', sa.String(255), nullable=True),
        sa.Column('condition_expression', sa.Text(), nullable=True),
        sa.Column('required_permissions', ARRAY(sa.String), nullable=True),
        sa.Column('required_roles', ARRAY(sa.String), nullable=True),
        sa.Column('pre_actions', JSONB(), nullable=True),
        sa.Column('post_actions', JSONB(), nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['workflow_id'], ['wf_definitions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['from_state_id'], ['wf_states.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['to_state_id'], ['wf_states.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wf_transitions_workflow_code', 'wf_transitions', ['workflow_id', 'code'], unique=True)
    op.create_index('ix_wf_transitions_from_state', 'wf_transitions', ['from_state_id'])

    # wf_instances
    op.create_table(
        'wf_instances',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('workflow_id', UUID(as_uuid=True), nullable=False),
        sa.Column('current_state_id', UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', UUID(as_uuid=True), nullable=False),
        sa.Column('citizen_id', UUID(as_uuid=True), nullable=False),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('assigned_to', UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='ACTIVE'),
        sa.Column('variables', JSONB(), nullable=True),
        sa.Column('context', JSONB(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('timeout_hours', sa.Integer, nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['workflow_id'], ['wf_definitions.id']),
        sa.ForeignKeyConstraint(['current_state_id'], ['wf_states.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wf_instances_entity', 'wf_instances', ['entity_type', 'entity_id'])
    op.create_index('ix_wf_instances_citizen', 'wf_instances', ['citizen_id'])
    op.create_index('ix_wf_instances_assigned', 'wf_instances', ['assigned_to'])
    op.create_index('ix_wf_instances_status', 'wf_instances', ['status'])
    op.create_index('ix_wf_instances_deadline', 'wf_instances', ['deadline'])

    # wf_tasks
    op.create_table(
        'wf_tasks',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('instance_id', UUID(as_uuid=True), nullable=False),
        sa.Column('state_id', UUID(as_uuid=True), nullable=False),
        sa.Column('transition_id', UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('assigned_to', UUID(as_uuid=True), nullable=True),
        sa.Column('assigned_role', sa.String(100), nullable=True),
        sa.Column('assignment_type', sa.String(50), nullable=False, server_default='ROLE'),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING'),
        sa.Column('priority', sa.String(20), nullable=False, server_default='MEDIUM'),
        sa.Column('form_data', JSONB(), nullable=True),
        sa.Column('result_data', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('due_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('timeout_hours', sa.Integer, nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['instance_id'], ['wf_instances.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['state_id'], ['wf_states.id']),
        sa.ForeignKeyConstraint(['transition_id'], ['wf_transitions.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wf_tasks_assigned', 'wf_tasks', ['assigned_to', 'status'])
    op.create_index('ix_wf_tasks_due', 'wf_tasks', ['due_at'])

    # wf_history
    op.create_table(
        'wf_history',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('instance_id', UUID(as_uuid=True), nullable=False),
        sa.Column('from_state_id', UUID(as_uuid=True), nullable=True),
        sa.Column('to_state_id', UUID(as_uuid=True), nullable=True),
        sa.Column('transition_id', UUID(as_uuid=True), nullable=True),
        sa.Column('task_id', UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('performed_by', UUID(as_uuid=True), nullable=True),
        sa.Column('performed_by_role', sa.String(100), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('data', JSONB(), nullable=True),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['instance_id'], ['wf_instances.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wf_history_instance', 'wf_history', ['instance_id', 'created_at'])
    op.create_index('ix_wf_history_performed_by', 'wf_history', ['performed_by'])


def downgrade():
    op.drop_table('wf_history')
    op.drop_table('wf_tasks')
    op.drop_table('wf_instances')
    op.drop_table('wf_transitions')
    op.drop_table('wf_states')
    op.drop_table('wf_definitions')
