# SILA System - GitHub Copilot Instructions for AI Agents

> **Note**: These instructions are designed to guide AI coding agents (including GitHub
> Copilot) through the SILA codebase. Developers using these instructions should
> understand the architectural patterns, coding standards, and validation requirements
> outlined herein.

## 1. Architecture Overview

### Stack & Framework

- **Backend Framework**: FastAPI 0.104+ with async/await throughout
- **ORM**: SQLAlchemy 2.0+ with AsyncSession for non-blocking database operations
- **Schema Validation**: Pydantic V2 with field validators and ConfigDict
- **Database**: PostgreSQL with asyncpg driver for async connections
- **Testing**: pytest 9.0+ with pytest-asyncio for async test support
- **Python Version**: 3.12.3+

### Directory Structure

```
sila-system/
├── apps/backend/                      # Backend application root
│   ├── modules/                       # Domain modules (DDD pattern)
│   │   ├── payment/
│   │   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── schemas/              # Pydantic validation schemas
│   │   │   ├── services/             # Business logic layer
│   │   │   └── endpoints/            # FastAPI routers
│   │   ├── documents/
│   │   ├── location/
│   │   └── [other modules]
│   ├── core/
│   │   ├── config.py                 # Settings & environment config
│   │   ├── db/
│   │   │   ├── base_class.py        # SQLAlchemy declarative base
│   │   │   └── session.py            # AsyncSession factory
│   │   └── security.py               # Authentication & authorization
│   └── conftest.py                   # CENTRAL pytest configuration
├── tests/modules/                     # Module-specific tests
├── docs/                              # Documentation
└── .github/                           # GitHub workflows & config
```

### Key Architectural Patterns

#### 1. Domain-Driven Design (DDD)

- Each feature is organized as a **module** (`payment/`, `documents/`, `location/`)
- Each module contains: models, schemas, services, endpoints
- Modules are independently testable and deployable

#### 2. Layered Architecture (3-tier)

```
API Layer (endpoints/router.py)
    ↓
Business Logic Layer (services/*.py)
    ↓
Data Access Layer (models/*.py + database)
```

#### 3. Async-First Design

- All database operations use `AsyncSession`
- All service methods are `async def`
- All tests use `pytest.mark.asyncio`
- No blocking operations in request handlers

#### 4. Type Safety

- All functions have type hints (Python 3.12 style)
- Pydantic V2 for runtime validation
- SQLAlchemy for database schema validation

---

## 2. Code Standards & Patterns

### Import Organization

**ABSOLUTE IMPORTS ONLY** - Never use relative imports:

```python
# ✅ CORRECT - Absolute imports
from core.security import get_current_user
from core.db.session import get_db
from modules.payment.services import PaymentService
from modules.payment.models.enums import PaymentStatus

# ❌ WRONG - Relative imports (will cause ImportError)
from ....core.security import get_current_user  # This breaks!
from ...models import Payment                   # This breaks!
```

**Import Order** (follow this sequence):

1. Python standard library (`datetime`, `asyncio`, `json`)
2. Third-party packages (`pydantic`, `sqlalchemy`, `fastapi`)
3. Local application imports (absolute paths starting with `core`, `modules`, `apps`)

### File Naming Conventions

```
models/
├── payment.py          # ORM model: class Payment(Base)
├── transaction.py      # ORM model: class PaymentTransaction(Base)
├── refund.py           # ORM model: class Refund(Base)
└── enums.py            # Enums: class PaymentStatus(str, Enum)

schemas/
├── payment.py          # Pydantic models: PaymentCreate, PaymentResponse
└── [domain].py         # One schema file per domain

services/
├── payment_service.py  # Business logic: class PaymentService
└── [domain]_service.py

endpoints/
├── __init__.py         # Export router: from .router import router
└── router.py           # FastAPI routes: router = APIRouter()
```

### Database Table Naming

**Convention**: `{module}_{entity}` (lowercase, snake_case)

```python
# apps/backend/modules/payment/models/payment.py
class Payment(Base):
    __tablename__ = "payment_payments"  # Module prefix required!

class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

class Refund(Base):
    __tablename__ = "payment_refunds"
```

⚠️ **CRITICAL**: Foreign keys must use exact table names including module prefix:

```python
# CORRECT
payment_id = Column(Integer, ForeignKey("payment_payments.id"))

# WRONG - Will cause "Can't find any foreign key relationships"
payment_id = Column(Integer, ForeignKey("payments.id"))
```

### Field Aliasing (Python Keywords)

When a column name conflicts with Python keywords, use aliases:

```python
class Payment(Base):
    # Python's "metadata" is a reserved word in some contexts
    # Solution: name the column one thing, map to schema differently
    metadata_ = Column("metadata", JSON)  # Column stored as "metadata" in DB
```

In Pydantic schemas, map the alias:

```python
class PaymentResponse(BaseModel):
    metadata: Optional[Dict[str, Any]] = Field(None, alias="metadata_")

    model_config = ConfigDict(
        from_attributes=True,      # Enable ORM mode for model_validate()
        populate_by_name=True       # Accept both "metadata" and "metadata_"
    )
```

---

## 3. Pydantic V2 Best Practices

### ConfigDict Requirements

```python
class PaymentInDB(BaseModel):
    id: int
    status: PaymentStatus

    model_config = ConfigDict(
        from_attributes=True,      # Required for ORM.model_validate(orm_obj)
        populate_by_name=True       # Accept field names and aliases
    )

# Usage with ORM object
payment_orm = session.query(Payment).first()
payment_schema = PaymentInDB.model_validate(payment_orm)  # Works with from_attributes=True
```

### Field Validators

Use `@field_validator` for cross-field validation and field mapping:

```python
from pydantic import field_validator

class PaymentResponse(BaseModel):
    amount: float
    currency: str

    @field_validator('amount', mode='before')
    @classmethod
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('amount must be positive')
        return v
```

### Optional Fields Pattern

```python
# Optional for request (user may not provide)
class PaymentCreate(BaseModel):
    amount: float
    description: Optional[str] = None  # Optional with default None

# Required for response (database always returns)
class PaymentResponse(BaseModel):
    id: int               # Required - always in DB
    created_at: datetime  # Required - always in DB
    status: PaymentStatus # Required - always has default PENDING
```

---

## 4. SQLAlchemy Patterns

### ORM Models (SQLAlchemy 2.0 Style)

```python
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.db.base_class import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payment_payments"

    id = Column(Integer, primary_key=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    reference = Column(String(100), unique=True, nullable=False)
    metadata_ = Column("metadata", JSON)

    # Relationships
    transactions = relationship("PaymentTransaction", back_populates="payment")
    refunds = relationship("Refund", back_populates="payment")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Async Database Operations

```python
# ✅ CORRECT - Async patterns
class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, data: PaymentCreate) -> PaymentInDB:
        payment = Payment(**data.model_dump())
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return PaymentInDB.model_validate(payment)

    async def get_payment(self, payment_id: int) -> Optional[PaymentInDB]:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await self.db.execute(stmt)
        payment = result.scalars().first()
        return PaymentInDB.model_validate(payment) if payment else None

# ❌ WRONG - Blocking operations
class PaymentService:
    def __init__(self, db: Session):  # Should be AsyncSession!
        self.db = db

    def create_payment(self, data):  # Should be async!
        payment = Payment(**data.model_dump())
        self.db.add(payment)
        self.db.commit()  # Should be await self.db.commit()!
```

---

## 5. Status Transition State Machine

### Payment Status Transitions

Valid transitions for `PaymentStatus`:

```
PENDING ──→ PROCESSING ──→ COMPLETED ──→ REFUNDED
    ├─→ CANCELLED          └────────→ PARTIALLY_REFUNDED ──→ REFUNDED
    └─→ FAILED ──→ PENDING
```

Implementation:

```python
class PaymentService:
    def _is_valid_status_transition(
        self,
        current_status: PaymentStatus,
        new_status: PaymentStatus
    ) -> bool:
        """Validate status transitions."""
        valid_transitions = {
            PaymentStatus.PENDING: [
                PaymentStatus.PROCESSING,
                PaymentStatus.CANCELLED,
                PaymentStatus.FAILED,
            ],
            PaymentStatus.PROCESSING: [
                PaymentStatus.COMPLETED,
                PaymentStatus.FAILED,
                PaymentStatus.CANCELLED,
            ],
            PaymentStatus.COMPLETED: [
                PaymentStatus.REFUNDED,
                PaymentStatus.PARTIALLY_REFUNDED,
            ],
            PaymentStatus.FAILED: [
                PaymentStatus.PENDING,
                PaymentStatus.CANCELLED,
            ],
            PaymentStatus.CANCELLED: [],
            PaymentStatus.REFUNDED: [],
            PaymentStatus.PARTIALLY_REFUNDED: [
                PaymentStatus.REFUNDED,
            ],
        }
        return new_status in valid_transitions.get(current_status, [])

    async def update_payment_status(
        self,
        payment_id: int,
        new_status: PaymentStatus
    ) -> PaymentInDB:
        """Update payment status with validation."""
        payment = await self.get_payment(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        if not self._is_valid_status_transition(payment.status, new_status):
            raise ValueError(
                f"Invalid status transition from {payment.status.value} to {new_status.value}"
            )

        payment.status = new_status
        await self.db.commit()
        await self.db.refresh(payment)
        return PaymentInDB.model_validate(payment)
```

---

## 6. Testing Guidelines

### Test File Organization

```
tests/modules/payment/
├── __init__.py
├── test_service.py        # Service layer tests
├── test_endpoints.py      # API endpoint tests (integration)
└── test_models.py         # Model validation tests (rarely needed)
```

### AsyncMock Fixture Pattern

```python
# apps/backend/conftest.py - CENTRAL CONFIGURATION
@pytest.fixture
def mock_db_session():
    """Proper AsyncMock setup for database operations."""
    session = AsyncMock()
    mock_scalars = MagicMock()
    mock_scalars.first = MagicMock()

    session.execute = AsyncMock(return_value=MagicMock(scalars=mock_scalars))
    session.commit = AsyncMock()
    session.add = MagicMock()
    session.refresh = AsyncMock()

    # Store mock objects for test access
    session._mock_scalars = mock_scalars

    return session
```

### Test Pattern: Service Layer

```python
@pytest.mark.asyncio
async def test_update_payment_status_valid_transition(
    payment_service: PaymentService,
    mock_db_session: AsyncMock
):
    """Test valid status transition."""
    # Setup
    mock_payment = MagicMock()
    mock_payment.id = 1
    mock_payment.status = PaymentStatus.PROCESSING
    mock_payment.amount = 100.0

    mock_db_session._mock_scalars.first.return_value = mock_payment
    payment_service.db = mock_db_session

    # Execute
    result = await payment_service.update_payment_status(
        payment_id=1,
        new_status=PaymentStatus.COMPLETED
    )

    # Assert
    assert result is not None
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
```

### Test Pattern: ORM Object Refreshing

When testing code that calls `db.refresh(obj)`, configure the mock to update the object:

```python
@pytest.mark.asyncio
async def test_create_refund(payment_service, mock_db_session):
    """Test refund creation with proper refresh handling."""
    now = datetime.now()

    # Mock payment record
    mock_payment = MagicMock()
    mock_payment.id = 1
    mock_payment.amount = 200.0
    mock_payment.status = PaymentStatus.COMPLETED

    mock_db_session._mock_scalars.first.return_value = mock_payment

    # Configure refresh to populate ORM object (simulates DB flush)
    async def mock_refresh(obj):
        obj.id = 2
        obj.created_at = now
        obj.status = TransactionStatus.PENDING

    mock_db_session.refresh = mock_refresh

    # Test code that does:
    # transaction = PaymentTransaction(...)
    # db.add(transaction)
    # await db.commit()
    # await db.refresh(transaction)  ← This will populate obj.id and obj.created_at
    # return RefundResponse(..., id=transaction.id, created_at=transaction.created_at)

    result = await payment_service.create_refund(...)
    assert result.id == 2
    assert result.created_at == now
```

### Running Tests

```bash
# All tests in a module
pytest tests/modules/payment/test_service.py -v

# Specific test
pytest tests/modules/payment/test_service.py::test_update_payment_status_valid_transition -v

# With coverage
pytest tests/modules/payment/ --cov=apps.backend.modules.payment --cov-report=html

# Set PYTHONPATH
export PYTHONPATH=$(pwd)/apps/backend
pytest tests/modules/payment/test_service.py -v
```

---

## 7. Environment Configuration

### Configuration Files

```
.env               # Development (default)
.env.test          # Testing (isolated, in-memory DB)
.env.staging       # Staging environment
.env.production    # Production (not in Git!)
```

### Loading Configuration

```python
# apps/backend/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/sila"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
```

### Test Configuration

```bash
# .env.test
ENVIRONMENT=test
DATABASE_URL=sqlite:///:memory:
ASYNC_DATABASE_URL=sqlite+aiosqlite:///:memory:
DEBUG=false
```

---

## 8. FastAPI Endpoint Patterns

### Router Setup

```python
# apps/backend/modules/payment/endpoints/router.py
from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_user
from core.db.session import get_db
from ..schemas import PaymentCreate, PaymentResponse
from ..services import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={404: {"description": "Payment not found"}}
)

@router.post("/", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment_data: PaymentCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create a new payment."""
    service = PaymentService(db)
    try:
        return await service.create_payment(payment_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    db = Depends(get_db)
):
    """Retrieve a payment by ID."""
    service = PaymentService(db)
    payment = await service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
```

### Export Pattern

```python
# apps/backend/modules/payment/endpoints/__init__.py
from .router import router

__all__ = ["router"]
```

### Main App Registration

```python
# apps/backend/main.py
from fastapi import FastAPI
from modules.payment.endpoints import router as payment_router

app = FastAPI()
app.include_router(payment_router)
```

---

## 9. Error Handling

### Service Layer Errors

```python
class PaymentService:
    async def update_payment_status(self, payment_id: int, status: PaymentStatus):
        # Validation errors (400)
        payment = await self.get_payment(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        # Business logic errors (422)
        if not self._is_valid_status_transition(payment.status, status):
            raise ValueError(
                f"Cannot transition from {payment.status.value} to {status.value}"
            )

        # Database errors (500) - let them bubble up
        await self.db.commit()
```

### Endpoint Error Mapping

```python
@router.post("/", response_model=PaymentResponse)
async def create_payment(payment_data: PaymentCreate, db = Depends(get_db)):
    service = PaymentService(db)
    try:
        return await service.create_payment(payment_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 10. Documentation Standards

### Docstring Format (Google Style)

```python
async def create_payment(
    self,
    payment_data: PaymentCreate,
    user_id: int
) -> PaymentInDB:
    """Create a new payment.

    Args:
        payment_data: Payment creation details (amount, method, etc.)
        user_id: ID of the user creating the payment

    Returns:
        PaymentInDB: The created payment with ID and timestamps

    Raises:
        ValueError: If payment data is invalid
        PermissionError: If user cannot create payments

    Example:
        >>> service = PaymentService(db)
        >>> payment = await service.create_payment(
        ...     PaymentCreate(amount=100.0, method=PaymentMethod.BNA),
        ...     user_id=42
        ... )
        >>> print(payment.reference)
        'PAY-ABC123XYZ'
    """
```

### Code Comments

Use comments sparingly for complex business logic:

```python
def _is_valid_status_transition(self, current, new) -> bool:
    """Validate status transitions using state machine rules."""
    # Certain statuses are terminal and cannot transition further
    if current in [PaymentStatus.CANCELLED, PaymentStatus.REFUNDED]:
        return False

    # Check against valid transition map
    valid_transitions = {...}
    return new in valid_transitions.get(current, [])
```

---

## 11. Common Pitfalls & Solutions

### Pitfall 1: Relative Imports

```python
# ❌ WRONG
from ....core.security import get_current_user

# ✅ CORRECT
from core.security import get_current_user

# Fix: Delete leading dots, use absolute path from apps/backend root
```

### Pitfall 2: Wrong Foreign Key Table Name

```python
# ❌ WRONG - Uses short table name
payment_id = Column(Integer, ForeignKey("payments.id"))

# ✅ CORRECT - Uses full table name with module prefix
payment_id = Column(Integer, ForeignKey("payment_payments.id"))

# Diagnosis: Run migration and check actual table name in PostgreSQL:
# SELECT table_name FROM information_schema.tables WHERE table_schema='public';
```

### Pitfall 3: Missing `from_attributes=True` in Schema

```python
# ❌ WRONG - ORM object won't map to schema
class PaymentResponse(BaseModel):
    id: int
    status: PaymentStatus

payment = PaymentResponse.model_validate(payment_orm)  # Fails!

# ✅ CORRECT - Enable ORM mode
class PaymentResponse(BaseModel):
    id: int
    status: PaymentStatus

    model_config = ConfigDict(from_attributes=True)

payment = PaymentResponse.model_validate(payment_orm)  # Works!
```

### Pitfall 4: Not Awaiting Async Operations

```python
# ❌ WRONG - Missing await
class PaymentService:
    async def create_payment(self):
        self.db.add(payment)
        self.db.commit()  # Missing await!

# ✅ CORRECT
class PaymentService:
    async def create_payment(self):
        self.db.add(payment)
        await self.db.commit()  # Awaited properly
```

### Pitfall 5: Invalid Status Transitions Not Caught

```python
# ❌ WRONG - No validation
async def update_payment_status(self, payment_id, new_status):
    payment = await self.get_payment(payment_id)
    payment.status = new_status  # No validation!
    await self.db.commit()

# ✅ CORRECT - Validate transitions
async def update_payment_status(self, payment_id, new_status):
    payment = await self.get_payment(payment_id)
    if not self._is_valid_status_transition(payment.status, new_status):
        raise ValueError(f"Invalid transition: {payment.status} → {new_status}")
    payment.status = new_status
    await self.db.commit()
```

---

## 12. Validation Checklist

Before submitting code for review, verify:

### Code Quality

- [ ] All imports are absolute (no relative imports)
- [ ] Type hints on all function signatures
- [ ] Docstrings on all public methods
- [ ] No `print()` statements (use logging instead)
- [ ] No hardcoded values (use environment variables/config)

### Async Compliance

- [ ] All database operations use `await`
- [ ] All service methods are `async def`
- [ ] All tests use `@pytest.mark.asyncio`
- [ ] No blocking operations in request handlers

### Database

- [ ] Table names follow `{module}_{entity}` pattern
- [ ] Foreign keys use full table names with module prefix
- [ ] All relationships use `back_populates` (bidirectional)
- [ ] Timestamps use `created_at` and `updated_at`

### Pydantic Schemas

- [ ] Response schemas have `ConfigDict(from_attributes=True)`
- [ ] Optional fields use `Optional[Type] = None`
- [ ] Required fields have no default
- [ ] Field validators for complex validation

### Testing

- [ ] Unit tests for all service methods
- [ ] Tests use central `conftest.py` fixtures
- [ ] All tests pass (`pytest tests/modules/[module]/ -v`)
- [ ] Test coverage ≥ 80% for business logic

### Status Transitions

- [ ] State machine transitions are validated
- [ ] Invalid transitions raise `ValueError`
- [ ] All valid transitions documented in code comments

### Error Handling

- [ ] Service methods raise `ValueError` for validation errors
- [ ] Service methods raise `PermissionError` for authorization errors
- [ ] Endpoints map errors to appropriate HTTP status codes
- [ ] Error messages are descriptive and actionable

---

## 13. Git Workflow

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(payment): add support for partial refunds
fix(payment): correct foreign key reference in transaction model
docs(payment): update status transition documentation
test(payment): add integration tests for refund flow
refactor(payment): consolidate payment status validation
```

### Pull Request Process

1. **Branch naming**: `feat/payment-refunds` or `fix/fk-reference`
2. **Tests passing**: `pytest tests/modules/[module]/ -v` (100%)
3. **Code review**: At least 1 approval
4. **Merge**: Squash commits to keep history clean

---

## 14. Quick Reference: Project Structure

### Adding a New Feature

1. **Create model** → `apps/backend/modules/[module]/models/[entity].py`
2. **Create schema** → `apps/backend/modules/[module]/schemas/[entity].py`
3. **Create service** → `apps/backend/modules/[module]/services/[entity]_service.py`
4. **Create router** → `apps/backend/modules/[module]/endpoints/router.py`
5. **Create tests** → `tests/modules/[module]/test_service.py`
6. **Update main** → Add router to `apps/backend/main.py`

### Running Tests

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$(pwd)/apps/backend

# All payment module tests
pytest tests/modules/payment/ -v

# Single test file
pytest tests/modules/payment/test_service.py -v

# Specific test
pytest tests/modules/payment/test_service.py::test_update_payment_status_valid_transition -v

# With coverage
pytest tests/modules/payment/ --cov=apps.backend.modules.payment --cov-report=html

# Watch mode (requires pytest-watch)
ptw tests/modules/payment/ -- -v
```

### Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements/backend.txt

# Load environment
export $(cat .env | xargs)

# Run tests
pytest tests/modules/payment/ -v
```

---

## 15. Resources & Links

### Official Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Async Guide](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [pytest Documentation](https://docs.pytest.org/)

### SILA-Specific

- Architecture documentation: `docs/ARQUITETURA_ATUALIZADA.md`
- API documentation: `docs/DOCUMENTS_API.md`
- Deployment guide: `docs/MAINTENANCE_GUIDE.md`
- Integration guide: `docs/integration_gateway_guide.md`

### Code Examples in Repository

- Payment module: `apps/backend/modules/payment/`
- Documents module: `apps/backend/modules/documents/`
- Location module: `apps/backend/modules/location/`

---

## 16. Support & Troubleshooting

### Common Issues

**Q: "ImportError: attempted relative import beyond top-level package"**

- A: Use absolute imports. Change `from ....core.security` to `from core.security`

**Q: "NoForeignKeysError: Can't find any foreign key relationships"**

- A: Check that ForeignKey references the full table name with module prefix (e.g.,
  `"payment_payments.id"`, not `"payments.id"`)

**Q: "ValidationError: id: Input should be a valid integer [input_value=None]"**

- A: In tests, ensure mocked ORM objects have all required fields set (id, created_at,
  etc.)

**Q: "asyncio.InvalidStateError: Event loop is closed"**

- A: Ensure tests use `@pytest.mark.asyncio` and the event loop fixture from conftest.py

### Getting Help

1. Check existing documentation in `docs/` folder
2. Review similar implementations in other modules
3. Search test files for examples of patterns
4. Consult this guide's troubleshooting section

---

## 17. Continuous Integration

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

### GitHub Actions

Tests run automatically on:

- Every pull request
- Before merging to main
- On schedule (nightly builds)

View workflows: `.github/workflows/`

---

## 18. Version Control

### Key Files (Never Commit)

- `.env` (use `.env.example` instead)
- `.env.production` (production secrets only)
- `.venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)

### Key Files (Always Commit)

- `.env.test` (test configuration)
- `requirements/` (dependencies)
- `tests/` (all test files)
- `docs/` (documentation)
- `.gitignore` (version control config)

---

**Last Updated**: 2024 **Status**: ✅ Production Ready **Maintenance**: See
OPERATIONS_LOG.md for recent changes
