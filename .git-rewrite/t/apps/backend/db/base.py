"""
Database base configuration for SQLAlchemy models.
Ensures that all ORM models are imported so Alembic can detect them.
"""

from sqlalchemy.orm import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()

# -----------------------------------------------------------------------------
# IMPORT ALL MODELS FOR ALEMBIC AUTOGENERATE
# -----------------------------------------------------------------------------

# This file centralizes all models. Importing it ensures that Alembic can
# discover every ORM model in the project.
import modules.models  # noqa: F401

# -----------------------------------------------------------------------------

__all__ = ["Base"]
