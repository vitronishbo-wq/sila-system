"""create citizen_documents table with versioning and indexes

Revision ID: 20260220_001_create_citizen_documents
Revises: 
Create Date: 2026-02-20
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import enum
from datetime import datetime

class DocumentTypeEnum(str, enum.Enum):
    BI = "BI"
    PASSPORT = "PASSPORT"
    BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    PHOTO = "PHOTO"

def upgrade():
    op.create_table(
        'citizen_documents',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('citizen_id', pg.UUID(as_uuid=True), sa.ForeignKey('citizen.id'), nullable=False),
        sa.Column('type', sa.Enum(DocumentTypeEnum, name='documenttypeenum'), nullable=False),
        sa.Column('file_path', sa.String(256), nullable=False),
        sa.Column('version', sa.Integer, nullable=False, default=1),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=datetime.utcnow),
    )
    op.create_index('ix_citizen_documents_citizen_id', 'citizen_documents', ['citizen_id'])
    op.create_index('ix_citizen_documents_type', 'citizen_documents', ['type'])
    op.create_index('ix_citizen_documents_version', 'citizen_documents', ['version'])

def downgrade():
    op.drop_index('ix_citizen_documents_version', table_name='citizen_documents')
    op.drop_index('ix_citizen_documents_type', table_name='citizen_documents')
    op.drop_index('ix_citizen_documents_citizen_id', table_name='citizen_documents')
    op.drop_table('citizen_documents')
