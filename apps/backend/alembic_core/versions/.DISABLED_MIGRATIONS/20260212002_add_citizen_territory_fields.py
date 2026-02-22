"""Add territory fields to citizen_fuc table

Revision ID: 20260212002
Revises: 20260212001
Create Date: 2026-02-12 10:05:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "20260212002"
down_revision = "20260212001"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("citizen_fuc", sa.Column("province_id", UUID(as_uuid=True), nullable=True))
    op.add_column("citizen_fuc", sa.Column("municipality_id", UUID(as_uuid=True), nullable=True))
    op.add_column("citizen_fuc", sa.Column("commune_id", UUID(as_uuid=True), nullable=True))
    op.add_column("citizen_fuc", sa.Column("neighborhood_id", UUID(as_uuid=True), nullable=True))
    
    op.create_foreign_key("fk_citizen_fuc_province", "citizen_fuc", "territories", ["province_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_citizen_fuc_municipality", "citizen_fuc", "territories", ["municipality_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_citizen_fuc_commune", "citizen_fuc", "territories", ["commune_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_citizen_fuc_neighborhood", "citizen_fuc", "territories", ["neighborhood_id"], ["id"], ondelete="SET NULL")
    
    op.create_index("ix_citizen_fuc_province", "citizen_fuc", ["province_id"])
    op.create_index("ix_citizen_fuc_municipality", "citizen_fuc", ["municipality_id"])
    op.create_index("ix_citizen_fuc_commune", "citizen_fuc", ["commune_id"])
    op.create_index("ix_citizen_fuc_neighborhood", "citizen_fuc", ["neighborhood_id"])

def downgrade():
    op.drop_index("ix_citizen_fuc_neighborhood", table_name="citizen_fuc")
    op.drop_index("ix_citizen_fuc_commune", table_name="citizen_fuc")
    op.drop_index("ix_citizen_fuc_municipality", table_name="citizen_fuc")
    op.drop_index("ix_citizen_fuc_province", table_name="citizen_fuc")
    
    op.drop_constraint("fk_citizen_fuc_neighborhood", "citizen_fuc", type_="foreignkey")
    op.drop_constraint("fk_citizen_fuc_commune", "citizen_fuc", type_="foreignkey")
    op.drop_constraint("fk_citizen_fuc_municipality", "citizen_fuc", type_="foreignkey")
    op.drop_constraint("fk_citizen_fuc_province", "citizen_fuc", type_="foreignkey")
    
    op.drop_column("citizen_fuc", "neighborhood_id")
    op.drop_column("citizen_fuc", "commune_id")
    op.drop_column("citizen_fuc", "municipality_id")
    op.drop_column("citizen_fuc", "province_id")
