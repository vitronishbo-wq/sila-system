"""Consolidate migration heads - merge 4 branches into single chain

Revision ID: 20260314_151759_merge_migrations_consolidation
Revises: "001_create_workflow_tables", "003_create_request_events", "004_add_citizen_id", "012_001_expand_service_catalog_governance"
Create Date: 2026-03-14T15:17:59.361029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260314_151759_merge_migrations_consolidation'
down_revision = ("001_create_workflow_tables", "003_create_request_events", "004_add_citizen_id", "012_001_expand_service_catalog_governance",)
branch_labels = None
depends_on = None


def upgrade():
    """
    This is a merge migration that combines 4 separate migration branches.
    No schema changes are made - this only consolidates the migration history.
    
    Merged heads:
    - 001_create_workflow_tables (001_001_create_workflow_tables.py)
    - 003_create_request_events (002_003_create_request_events.py)
    - 004_add_citizen_id (006_004_add_citizen_id_to_invoices.py)
    - 012_001_expand_service_catalog_governance (012_001_expand_service_catalog_governance.py)
    """
    pass


def downgrade():
    """Downgrade is not supported for merge migrations."""
    raise NotImplementedError('Downgrade is not supported for this merge migration')
