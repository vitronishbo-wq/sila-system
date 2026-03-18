"""Create sequence table

Revision ID: 004_create_sequence_table
Revises: 003_create_certificate_audit_tables
Create Date: 2024-01-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid

# Revision identifiers, used by Alembic.
revision = '004_create_sequence_table'
down_revision = '003_create_certificate_audit_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sequence table
    op.create_table(
        'payment_sequences',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('sequence_type', sa.String(50), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('last_value', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id', name='payment_sequences_pkey'),
        sa.UniqueConstraint('sequence_type', 'year', name='uq_sequence_type_year'),
    )
    
    # Insert initial sequences
    op.execute(
        """INSERT INTO payment_sequences (id, sequence_type, year, last_value, created_at, updated_at)
        VALUES 
        ('{}'::uuid, 'DECLARATION', 2024, 0, NOW(), NOW()),
        ('{}'::uuid, 'DEBT', 2024, 0, NOW(), NOW()),
        ('{}'::uuid, 'PAYMENT', 2024, 0, NOW(), NOW()),
        ('{}'::uuid, 'CERTIFICATE', 2024, 0, NOW(), NOW())
        """.format(
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        )
    )


def downgrade() -> None:
    op.drop_table('payment_sequences')
