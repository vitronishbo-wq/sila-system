# Common Layer Documentation

## Overview

The common layer (`modules/common/`) provides shared components that reduce code
duplication and establish consistent patterns across all modules in the SILA system.
This layer serves as the foundation for cross-cutting concerns and reusable
functionality.

## Components

### 1. Exceptions (`exceptions/`)

Custom exception classes that provide standardized error handling across all modules.

#### Key Features:

- **Base Exception**: `SILAError` - Base class for all custom exceptions
- **Resource Errors**: `ResourceNotFoundError`, `DuplicateResourceError`
- **Validation Errors**: `ValidationError`, `BusinessRuleError`
- **Security Errors**: `AuthenticationError`, `AuthorizationError`
- **System Errors**: `DatabaseError`, `ExternalServiceError`, `ConfigurationError`
- **HTTP Conversion**: `handle_sila_error()` - Converts exceptions to HTTP responses

#### Usage Example:

```python
from modules.common.exceptions import ResourceNotFoundError, handle_sila_error

# Raise custom exception
if not user:
    raise ResourceNotFoundError("User", user_id)

# Convert to HTTP response
try:
    # some operation
except ResourceNotFoundError as e:
    http_exception = handle_sila_error(e)
    return JSONResponse(
        status_code=http_exception.status_code,
        content=http_exception.detail
    )
```

### 2. Base Models and Schemas (`bases/`)

Abstract base classes for consistent data structures and validation patterns.

#### SQLAlchemy Base Models:

- **`SILABase`**: Base model with common fields (id, timestamps, audit fields)
- **`TimestampMixin`**: Adds created_at/updated_at fields
- **`UUIDMixin`**: Adds UUID primary key
- **`AuditMixin`**: Adds created_by/updated_by/version fields

#### Pydantic Base Schemas:

- **`BaseSchema`**: Base schema with common configuration
- **`BaseResponseSchema`**: Standard response schema with common fields
- **`BaseCreateSchema`**: Schema for creating entities
- **`BaseUpdateSchema`**: Schema for updating entities
- **`BaseListResponse`**: Generic paginated response schema
- **`BaseSearchSchema`**: Standard search parameters schema
- **`BaseFilterSchema`**: Common filter parameters schema

#### Usage Example:

```python
from modules.common.bases import SILABase, BaseResponseSchema, BaseCreateSchema
from sqlalchemy import Column, String

# SQLAlchemy model
class UserModel(SILABase):
    __tablename__ = "users"
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

# Pydantic schemas
class UserCreate(BaseCreateSchema):
    email: str
    name: str

class UserResponse(BaseResponseSchema):
    email: str
    name: str
```

### 3. Utilities (`utils/`)

General-purpose utility functions for common operations.

#### Categories:

- **Security**: Password hashing, token generation, API key creation
- **Validation**: Email, phone, NIF, BI number validation
- **String**: Normalization, slug generation, data masking
- **Date/Time**: ISO formatting, parsing, age calculation
- **Data Transformation**: Document cleaning, number extraction, currency formatting
- **Dictionary**: Deep merging, flattening
- **List**: Chunking, deduplication
- **Hash**: Data hashing and verification
- **UUID**: Validation and short generation
- **Error Handling**: Safe type conversions

#### Usage Example:

```python
from modules.common.utils import (
    validate_email, hash_password, generate_slug,
    format_datetime_iso, clean_document_number
)

# Validation
if validate_email(user.email):
    # process valid email

# Security
hashed_Truman1*Marcelo1*plain_password")

# String processing
slug = generate_slug("User Name Registration")
clean_nif = clean_document_number("00.123.456/AB-CD")

# Date/time
iso_time = format_datetime_iso(datetime.utcnow())
```

## Benefits

### 1. Code Reduction

- Eliminates duplicate exception handling across modules
- Provides reusable base models and schemas
- Centralizes common utility functions

### 2. Consistency

- Standardized error codes and messages
- Consistent data structure patterns
- Uniform validation rules

### 3. Maintainability

- Single point of truth for shared functionality
- Easier updates and bug fixes
- Centralized testing of common components

### 4. Standardization

- Common field definitions (IDs, timestamps)
- Standard response formats
- Consistent naming conventions

## Integration Guide

### Step 1: Import Common Components

```python
from modules.common.exceptions import ResourceNotFoundError, ValidationError
from modules.common.bases import SILABase, BaseResponseSchema, BaseCreateSchema
from modules.common.utils import validate_email, hash_password, generate_slug
```

### Step 2: Extend Base Classes

```python
# SQLAlchemy model
class YourModel(SILABase):
    __tablename__ = "your_table"
    # your fields

# Pydantic schemas
class YourCreateSchema(BaseCreateSchema):
    # your fields

class YourResponseSchema(BaseResponseSchema):
    # your fields
```

### Step 3: Use Common Exceptions

```python
def your_function():
    if not resource:
        raise ResourceNotFoundError("YourResource", resource_id)

    if invalid_data:
        raise ValidationError("Invalid data format", "field_name")
```

### Step 4: Apply Utility Functions

```python
def process_user_data(data):
    # Validation
    if not validate_email(data["email"]):
        raise ValidationError("Invalid email", "email")

    # Transformation
    data["slug"] = generate_slug(data["name"])
    data["password_hash"] = hash_password(data["password"])

    return data
```

## Best Practices

### 1. Exception Handling

- Always use specific exception types from the common layer
- Include meaningful error messages and details
- Use `handle_sila_error()` for HTTP response conversion

### 2. Base Class Usage

- Extend `SILABase` for all SQLAlchemy models
- Use appropriate base schemas for different operations
- Follow the naming conventions (Create, Update, Response)

### 3. Utility Functions

- Prefer common utilities over custom implementations
- Validate inputs using common validation functions
- Use consistent formatting functions

### 4. Consistency

- Follow established patterns for new modules
- Use common field definitions and naming
- Maintain consistent error handling approaches

## Migration Guide

### For Existing Modules:

1. **Replace Custom Exceptions**:

   ```python
   # Before
   class MyCustomError(Exception):
       pass

   # After
   from modules.common.exceptions import BusinessRuleError
   raise BusinessRuleError("my_rule", "details")
   ```

2. **Update Base Models**:

   ```python
   # Before
   class MyModel(Base):
       id = Column(UUID, primary_key=True)
       created_at = Column(DateTime, default=datetime.utcnow)

   # After
   from modules.common.bases import SILABase
   class MyModel(SILABase):
       # your specific fields only
   ```

3. **Standardize Schemas**:

   ```python
   # Before
   class MySchema(BaseModel):
       # custom configuration

   # After
   from modules.common.bases import BaseCreateSchema
   class MyCreateSchema(BaseCreateSchema):
       # your fields only
   ```

## Testing

The common layer includes comprehensive tests for all components:

```bash
# Run tests for common layer
pytest modules/common/tests/

# Test specific components
pytest modules/common/tests/test_exceptions.py
pytest modules/common/tests/test_bases.py
pytest modules/common/tests/test_utils.py
```

## Future Enhancements

### Planned Additions:

1. **Advanced Validation**: More sophisticated validation rules
2. **Caching Utilities**: Redis-based caching helpers
3. **Event System**: Common event publishing/subscribing
4. **Logging Enhancements**: Structured logging utilities
5. **Security Helpers**: Additional security-related utilities

### Extension Points:

- Custom exception types for specific domains
- Additional base mixins for common patterns
- Specialized utility functions for specific needs

## Support

For questions or issues related to the common layer:

- Check the examples in `modules/common/examples.py`
- Review the test files for usage patterns
- Contact the core development team

---

_Last updated: 2025-01-17_ _Version: 1.0.0_
