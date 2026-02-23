"""Template DDD module structure.

This is the canonical structure for all modules in SILA.
Copy this to: modules/{domain}/__init__.py

Structure:
modules/{domain}/
├── __init__.py              (this file)
├── domain/
│   ├── __init__.py
│   ├── entities.py          # Domain entities
│   ├── value_objects.py     # Value objects
│   └── exceptions.py        # Domain exceptions
├── application/
│   ├── __init__.py
│   ├── use_cases.py         # Business logic (services)
│   ├── dto.py               # Data Transfer Objects
│   └── ports.py             # Abstract interfaces
├── infrastructure/
│   ├── __init__.py
│   ├── persistence.py       # Database adapters
│   └── repositories.py      # Repository implementations
├── api/
│   ├── __init__.py
│   ├── routes.py            # FastAPI router
│   ├── schemas.py           # Pydantic schemas
│   └── dependencies.py      # Module dependencies
├── models/
│   ├── __init__.py
│   └── {entity}.py          # SQLAlchemy ORM models
└── seeds/
    ├── __init__.py
    └── seed_data.py         # Test data generation
"""

__all__ = []
