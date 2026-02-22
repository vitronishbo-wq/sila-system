"""add_saude_primaria

Revision ID: 20231027001
Revises: 
Create Date: 2023-10-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20231027001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Criação dos tipos ENUM no PostgreSQL para garantir integridade com o domínio SILA
    saude_service_type = postgresql.ENUM(
        '022_consulta_medica_geral', 
        '023_consulta_medica_especializada', 
        '029_atendimento_de_saude_materno_infantil', 
        '030_planeamento_familiar', 
        '032_assistencia_pre_natal', 
        '033_assistencia_pos_natal', 
        '035_aconselhamento_nutricional', 
        '040_apoio_psicologico_comunitario', 
        '0968_acompanhamento_de_doentes_cronicos', 
        '0969_alertas_de_saude_personalizados', 
        '756_educacao_alimentar_comunitaria', 
        '758_monitorizacao_nutricional_comunitaria', 
        name='healthcareservicetype'
    )
    saude_service_type.create(op.get_bind())
    
    appointment_status = postgresql.ENUM(
        'pending', 'scheduled', 'in_progress', 'completed', 'cancelled', 'no_show', 
        name='appointmentstatus'
    )
    appointment_status.create(op.get_bind())
    
    maternal_risk_level = postgresql.ENUM('low', 'medium', 'high', name='maternalrisklevel')
    maternal_risk_level.create(op.get_bind())
    
    chronic_severity = postgresql.ENUM('mild', 'moderate', 'severe', name='chronicseverity')
    chronic_severity.create(op.get_bind())
    
    notification_channel = postgresql.ENUM('sms', 'email', 'app', name='notificationchannel')
    notification_channel.create(op.get_bind())

    # Tabela Principal: saude_requests (Workflow Motor)
    op.create_table(
        'saude_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('citizen_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('service_type', saude_service_type, nullable=False),
        sa.Column('status', appointment_status, server_default='pending', nullable=True),
        sa.Column('preferred_date', sa.DateTime(), nullable=True),
        sa.Column('scheduled_date', sa.DateTime(), nullable=True),
        sa.Column('health_unit_id', sa.String(), nullable=True),
        sa.Column('clinical_notes', sa.Text(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saude_requests_citizen_id'), 'saude_requests', ['citizen_id'], unique=False)
    op.create_index(op.f('ix_saude_requests_service_type'), 'saude_requests', ['service_type'], unique=False)
    op.create_index(op.f('ix_saude_requests_status'), 'saude_requests', ['status'], unique=False)
    op.create_index('ix_saude_requests_citizen_status', 'saude_requests', ['citizen_id', 'status'], unique=False)

    # Tabela Especializada: Maternal (Saúde Materna)
    op.create_table(
        'saude_maternal_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('gestational_weeks', sa.Integer(), nullable=True),
        sa.Column('risk_level', maternal_risk_level, nullable=True),
        sa.Column('expected_delivery_date', sa.Date(), nullable=True),
        sa.Column('parity', sa.Integer(), nullable=True),
        sa.Column('prenatal_visits', sa.Integer(), server_default='0', nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['saude_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )

    # Tabela Especializada: Pós-Natal
    op.create_table(
        'saude_post_natal_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('days_post_partum', sa.Integer(), nullable=False),
        sa.Column('healing_status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['saude_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )

    # Tabela Especializada: Doentes Crónicos
    op.create_table(
        'saude_chronic_monitoring',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('condition_name', sa.String(), nullable=False),
        sa.Column('severity', chronic_severity, nullable=False),
        sa.Column('medication_plan', sa.Text(), nullable=True),
        sa.Column('monitoring_frequency', sa.String(), nullable=True),
        sa.Column('last_measurements', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['saude_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )

    # Tabela Especializada: Nutrição
    op.create_table(
        'saude_nutrition_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('height', sa.Float(), nullable=False),
        sa.Column('bmi', sa.Float(), nullable=False),
        sa.Column('nutritional_status', sa.String(), nullable=True),
        sa.Column('risk_category', sa.String(), nullable=True),
        sa.Column('diet_plan', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['saude_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )

    # Tabela Especializada: Psicologia
    op.create_table(
        'saude_psychology_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_type', sa.String(), nullable=False),
        sa.Column('risk_assessment', sa.Text(), nullable=True),
        sa.Column('referral_needed', sa.Boolean(), server_default='false', nullable=True),
        sa.Column('suicide_risk_flag', sa.Boolean(), server_default='false', nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['saude_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )

    # Tabela Especializada: Alertas
    op.create_table(
        'saude_health_alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('alert_type', sa.String(), nullable=False),
        sa.Column('threshold_value', sa.String(), nullable=True),
        sa.Column('notification_channel', notification_channel, nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['saude_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )


def downgrade():
    op.drop_table('saude_health_alerts')
    op.drop_table('saude_psychology_sessions')
    op.drop_table('saude_nutrition_records')
    op.drop_table('saude_chronic_monitoring')
    op.drop_table('saude_post_natal_records')
    op.drop_table('saude_maternal_records')
    op.drop_table('saude_requests')
    
    sa.Enum(name='notificationchannel').drop(op.get_bind())
    sa.Enum(name='chronicseverity').drop(op.get_bind())
    sa.Enum(name='maternalrisklevel').drop(op.get_bind())
    sa.Enum(name='appointmentstatus').drop(op.get_bind())
    sa.Enum(name='healthcareservicetype').drop(op.get_bind())
