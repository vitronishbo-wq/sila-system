# backend/app/modules/identity/models/role_permission.py
"""
Association table for roles <-> permissions.

Usamos uma Table (não uma classe ORM com colunas igualmente nomeadas em outro
módulo) para evitar redefinição de colunas primárias que causa:
    sqlalchemy.exc.ArgumentError: Trying to redefine primary-key column 'role_id' ...
"""
from sqlalchemy import Column, ForeignKey, Integer, Table

from core.db.base_class import Base

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
