"""SQLAlchemy Declarative Base Class.

This module defines the Base class from which all ORM models must inherit.
It provides:
  - Automatic table name generation from class names
  - Standard ID column
  - Unified declarative configuration for all models

All models MUST explicitly define __tablename__ with module prefix:
    Example: __tablename__ = "payment_payments"
"""

import re
from typing import Any

from sqlalchemy import Column, Integer
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class Base:
    """Base class providing standard structure for all ORM models.

    All application models must inherit from this class.

    Attributes:
        id: Auto-increment primary key (can be overridden in subclasses)
        __tablename__: Auto-generated from class name in snake_case format
    """

    __name__: str

    # Standard ID column (can be overridden in model subclasses if needed)
    id: Any = Column(Integer, primary_key=True, index=True, nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name (CamelCase → snake_case).

        Examples:
            Payment → payment
            PaymentTransaction → payment_transaction
            ServiceModel → service_model
        """
        # Insert underscore before uppercase letters preceded by lowercase
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    def __repr__(self) -> str:
        """Standard string representation for all model instances."""
        return f"<{self.__class__.__name__}(id={self.id})>"


__all__ = ["Base"]
