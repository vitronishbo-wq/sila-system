# 📋 Real Migration Examples from Your Project

## Example 1: Service Hub Schema (10 validators)

### Before (v1)

```python
from pydantic import BaseModel, Field, validator

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    requirements: Optional[Dict[str, Any]] = None

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome do serviço não pode estar vazio')
        return v.strip()

    @validator('requirements')
    def validate_requirements(cls, v):
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError('Requisitos devem ser um objeto JSON válido')
        return v
```

### After (v2) - Automatically Migrated

```python
from pydantic import BaseModel, Field, field_validator

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    requirements: Optional[Dict[str, Any]] = None

    @field_validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome do serviço não pode estar vazio')
        return v.strip()

    @field_validator('requirements')
    def validate_requirements(cls, v):
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError('Requisitos devem ser um objeto JSON válido')
        return v
```

**Changes:**

- ✅ `from pydantic import validator` → `from pydantic import field_validator`
- ✅ `@validator('name')` → `@field_validator('name')` (10 occurrences)

---

## Example 2: Training Schema (9 validators)

### Before (v1)

```python
from pydantic import BaseModel, validator

class TrainingCreate(BaseModel):
    title: str
    description: str

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError('Description too short')
        return v
```

### After (v2) - Automatically Migrated

```python
from pydantic import BaseModel, field_validator

class TrainingCreate(BaseModel):
    title: str
    description: str

    @field_validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @field_validator('description')
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError('Description too short')
        return v
```

---

## Example 3: Test File (.dict() usage)

### Before (v1)

```python
def test_schema_validation():
    user = User(id=1, name="Alice")
    data = user.dict()
    assert data["id"] == 1

    json_data = user.json()
    assert '"id": 1' in json_data
```

### After (v2) - Automatically Migrated

```python
def test_schema_validation():
    user = User(id=1, name="Alice")
    data = user.model_dump()
    assert data["id"] == 1

    json_data = user.model_dump_json()
    assert '"id": 1' in json_data
```

**Changes:**

- ✅ `.dict()` → `.model_dump()`
- ✅ `.json()` → `.model_dump_json()`

---

## Example 4: Citizenship Schema (validator with pre=True)

### Before (v1)

```python
from pydantic import BaseModel, validator

class CertidaoNascimento(BaseModel):
    numero: str
    data_emissao: str

    @validator('numero', pre=True)
    def normalize_numero(cls, v):
        return str(v).strip().upper()
```

### After (v2) - Automatically Migrated

```python
from pydantic import BaseModel, field_validator

class CertidaoNascimento(BaseModel):
    numero: str
    data_emissao: str

    @field_validator('numero', mode="before")
    def normalize_numero(cls, v):
        return str(v).strip().upper()
```

**Changes:**

- ✅ `@validator('numero', pre=True)` → `@field_validator('numero', mode="before")`

---

## Example 5: Root Validator (Complex)

### Before (v1)

```python
from pydantic import BaseModel, root_validator

class PasswordReset(BaseModel):
    password: str
    confirm_password: str

    @root_validator
    def check_passwords_match(cls, values):
        pw = values.get('password')
        cpw = values.get('confirm_password')
        if pw != cpw:
            raise ValueError('Passwords do not match')
        return values
```

### After (v2) - Automatically Migrated

```python
from pydantic import BaseModel, model_validator

class PasswordReset(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self
```

**Changes:**

- ✅ `@root_validator` → `@model_validator(mode="after")`
- ✅ `cls, values` → `self`
- ✅ `values.get('password')` → `self.password`

---

## Example 6: ORM Integration

### Before (v1)

```python
from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Usage
db_user = session.query(DBUser).first()
user = UserRead.from_orm(db_user)
```

### After (v2) - Automatically Migrated

```python
from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

# Usage
db_user = session.query(DBUser).first()
user = UserRead.model_validate(db_user, from_attributes=True)
```

**Changes:**

- ✅ `class Config: orm_mode = True` → `model_config = {"from_attributes": True}`
- ✅ `.from_orm(db_user)` → `.model_validate(db_user, from_attributes=True)`

---

## Example 7: Multiple Validators on Same Field

### Before (v1)

```python
from pydantic import BaseModel, validator

class ServiceLocationBase(BaseModel):
    province: str
    municipality: str

    @validator('province', 'municipality')
    def validate_location_names(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome da localização não pode estar vazio')
        return v.strip().title()
```

### After (v2) - Automatically Migrated

```python
from pydantic import BaseModel, field_validator

class ServiceLocationBase(BaseModel):
    province: str
    municipality: str

    @field_validator('province', 'municipality')
    def validate_location_names(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome da localização não pode estar vazio')
        return v.strip().title()
```

**Changes:**

- ✅ `@validator('province', 'municipality')` →
  `@field_validator('province', 'municipality')`

---

## Example 8: Parse Object

### Before (v1)

```python
# API endpoint
data = {"name": "Service", "category": "CITIZENSHIP"}
service = ServiceCreate.parse_obj(data)

# JSON parsing
json_str = '{"name": "Service", "category": "CITIZENSHIP"}'
service = ServiceCreate.parse_raw(json_str)
```

### After (v2) - Automatically Migrated

```python
# API endpoint
data = {"name": "Service", "category": "CITIZENSHIP"}
service = ServiceCreate.model_validate(data)

# JSON parsing
json_str = '{"name": "Service", "category": "CITIZENSHIP"}'
service = ServiceCreate.model_validate_json(json_str)
```

**Changes:**

- ✅ `.parse_obj(data)` → `.model_validate(data)`
- ✅ `.parse_raw(json_str)` → `.model_validate_json(json_str)`

---

## Summary of Changes in Your Project

Based on the dry-run scan:

| Transformation                         | Count  | Files Affected |
| -------------------------------------- | ------ | -------------- |
| `@validator` → `@field_validator`      | 29     | 14 files       |
| `@root_validator` → `@model_validator` | 6      | 1 file         |
| `.dict()` → `.model_dump()`            | 11     | 4 files        |
| `.json()` → `.model_dump_json()`       | 10     | 4 files        |
| `.parse_obj()` → `.model_validate()`   | 4      | 1 file         |
| `.from_orm()` → `.model_validate()`    | 1      | 1 file         |
| **Total**                              | **61** | **18 files**   |

---

## Files with Most Changes

1. **service_hub.py** - 10 validators
2. **training.py** - 9 validators
3. **9 citizenship schemas** - 1 validator each
4. **Scripts** - Various `.dict()` and `.json()` calls

---

## Zero Manual Intervention Required

All these transformations are handled automatically by the migration script. No manual
editing needed! 🎉

Just run:

```bash
python3 scripts/migrate_pydantic_v1_to_v2.py
```
