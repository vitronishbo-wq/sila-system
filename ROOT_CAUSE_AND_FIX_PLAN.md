# 🔧 SILA System - Root Cause Analysis & Fix Implementation

**Date**: 2026-02-22  
**Status**: ROOT CAUSE IDENTIFIED - Schema vs Model Misalignment  
**Priority**: 🔴 CRITICAL - Blocking seed execution and ORM operations

---

## 🎯 ROOT CAUSE IDENTIFIED

### The Real Issue: Schema vs Model Mismatch

The **actual PostgreSQL schema** (created by migrations) does NOT match the **SQLAlchemy ORM model**.

**Evidence**:
```
Migrations Applied: migration/versions/2025_12_27_1310-*.py
Tables Created: 21 tables in sila_db
Users Table: ✅ EXISTS with ACTUAL columns
actual values    | Model Expectations        | Status
-----------------|--------------------------|--------
hashed_password  | password_hash            | ❌ NAME MISMATCH
region_id        | territory_id             | ❌ NAME MISMATCH  
roles (JSON)     | role (scalar string)     | ❌ TYPE MISMATCH
administrative_level | level (scalar)      | ❌ NAME MISMATCH
uuid (varchar)   | (no field)               | ⚠️  MODEL MISSING
Actual DB Schema Updated "level" but still no territory_id
```

---

## 📋 ACTUAL DATABASE SCHEMA

```sql
-- VERIFIED ON 2026-02-22 via psql
TABLE "users" (
    id                 INTEGER PRIMARY KEY AUTO-INCREMENT
    uuid               VARCHAR(36)           -- UUID v4 string representation
    email              VARCHAR(255) UNIQUE
    hashed_password    VARCHAR(255)          -- ← NOT "password_hash"
    phone              VARCHAR(20)
    bi_number          VARCHAR(20) UNIQUE
    is_active          BOOLEAN DEFAULT true
    is_verified        BOOLEAN DEFAULT false
    status             VARCHAR(20)           -- e.g., 'ACTIVE', 'INACTIVE', 'SUSPENDED'
    level              VARCHAR(20)           -- e.g., 'LOCAL', 'PROVINCIAL', 'NATIONAL'
    region_id          INTEGER FK→locations  -- ← NOT "territory_id", refs locations NOT territories
    roles              JSON                  -- ← ARRAY OF ROLES, not scalar
    created_at         TIMESTAMP DEFAULT NOW
    updated_at         TIMESTAMP DEFAULT NOW
    last_login         TIMESTAMP             -- Nullable
    full_name          VARCHAR(100)
    administrative_level VARCHAR(20)
    
    Indexes:
    - UNIQUE on email, bi_number, uuid
    - FK constraint on region_id → locations.id
)
```

---

## 🔴 PROBLEM 1: ORM Model Doesn't Match Schema

### Current Model (`app/core/iam/models/user.py`)

```python
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)  # ❌ Model: String
    # ^^^^^^ DB INTEGER
    
    username: Mapped[str] = mapped_column(String, unique=True)  # ❌ COLUMN DOESN'T EXIST
    
    password_hash: Mapped[str] = mapped_column(String)  # ❌ DB: "hashed_password"
    # ^^^^^^^^^^^^^^
    
    role: Mapped[str] = ...  # Single scalar
    # ^^^^ DB: roles (JSON array)
    
    level: Mapped[str] = ...  # Scalar
    # ^^^^ DB: administrative_level
    
    territory_id: Mapped[uuid.UUID | None] = ForeignKey("territories.id")
    # ^^^^^^^^^^^^ DB: region_id → locations.id
    # ALSO: territories table doesn't exist, it's "locations"
    
    citizen_id: Mapped[uuid.UUID | None] = ForeignKey("citizen_fuc.citizen_id")
    # ^^^^^^^^^ COLUMN DOESN'T EXIST IN DB
```

**Consequence**: When any ORM query tries to load a User:
```python
async with AsyncSession() as db:
    stmt = select(User)
    result = await db.execute(stmt)
    user = result.scalars().first()  # ❌ FAILS - column mismatches
```

---

## 🔴 PROBLEM 2: Seed Scripts Reference Wrong Table

### Current Seed Script (`apps/backend/seeds/core/seed_founding_users_with_territories.py`)

```python
cursor.execute("""
    UPDATE iam_users          # ❌ TABLE DOESN'T EXIST
    SET territory_id = %s, role = %s, level = %s
    WHERE email = %s
    """, (territory_id, role, level, email)
)
```

**Error When Run**:
```
psycopg2.errors.UndefinedTable: relation "iam_users" does not exist
```

---

## ✅ FIX PLAN (Step-by-Step)

### FIX 1: Update SQLAlchemy User Model

**File**: `apps/backend/app/core/iam/models/user.py`

**Change**:
```python
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON as JSONType

class User(Base):
    __tablename__ = "users"

    # Primary Key: INTEGER (not String!)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # UUID field (legacy/alternative key)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    
    # User info
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)  # Updated name!
    # REMOVED: username (doesn't exist in DB)
    
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bi_number: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    
    # Status fields
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")
    
    # Authorization fields
    level: Mapped[str] = mapped_column(String(20), default="LOCAL")
    administrative_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Roles - now as JSON array
    roles: Mapped[dict] = mapped_column(JSONType, default=lambda: [])
    
    # Geographic assignment: region_id (not territory_id!)
    region_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Relationship
    region = relationship("Location", foreign_keys=[region_id])
    
    # REMOVED: citizen_id (doesn't exist in DB yet)
    # REMOVED: territory_id (use region_id instead)
    # REMOVED: territory relationship
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
```

---

### FIX 2: Update Seed Script - Fix Table Name

**File**: `apps/backend/seeds/core/seed_founding_users_with_territories.py`

**Change** (Line ~140):
```python
# OLD (WRONG):
cursor.execute("""
    UPDATE iam_users 
    SET territory_id = %s, role = %s, level = %s
    WHERE email = %s
""", (territory_id, role, level, email))

# NEW (CORRECT):
cursor.execute("""
    UPDATE users 
    SET region_id = %s, level = %s, status = %s
    WHERE email = %s
""", (region_id, level, "ACTIVE", email))
```

---

### FIX 3: Adapt Python Seed Script to Use ORM

**File**: `apps/backend/seeds/core/seed_founding_users.py` (BEST APPROACH)

This script ALREADY uses ORM correctly! The issue is just field names. Update it:

```python
# The script already does:
user = User(
    id=uuid4(),                    # ❌ Should be: id auto-generated (no manual set)
    email=user_config["email"],    # ✅ OK
    username=user_config["username"],  # ❌ REMOVE (doesn't exist in DB)
    password_hash=get_password_hash(...),  # ✅ OK (rename to hashed_password)
    role=role_enum.value,          # ⚠️  MAYBE - roles is JSON array
    level=level,                   # ✅ OK  (rename to administrative_level)
    is_active=True,                # ✅ OK
    territory_id=territory_id,     # ❌ RENAME to region_id
)

# FIXED:
user = User(
    # id: let DB auto-generate
    uuid=str(uuid4()),             # Set UUID for backward compat
    email=user_config["email"],    # ✅
    # username: REMOVED - not in DB
    hashed_password=get_password_hash(UNIVERSAL_PASSWORD),  # Renamed!
    full_name=user_config.get("full_name", user_config["email"]),  # Add
    status="ACTIVE",               # Add explicit status
    level=level,                   # Keep level
    administrative_level=role_enum.value,  # Use for admin level
    roles=[role_enum.value],       # Convert role to array
    region_id=territory_id,        # Renamed from territory_id!
    is_active=True,
)
```

---

### FIX 4: SQL Seeds - Update All References

**Files to Update**:
- ❌ `seed_founding_users_with_territories.py` Line 140 - change `iam_users` → `users`
- ❌ `seed_founding_users.py` - uses ORM (just fix model fields)
- ❌ `seed_and_token.py` - check for SQL references
- ❌ `seed_*.py` in scripts/ - validate

**Replace Pattern**:
```sql
UPDATE iam_users      ← WRONG
  ↓
UPDATE users          ← CORRECT
```

---

### FIX 5: Create Migration Fix (Optional but Recommended)

If you want to add columns that are missing (recommended for future expansion):

```bash
cd apps/backend

# Create migration to add citizen_id and territory_id if needed
python -m alembic revision --autogenerate -m "add_citizen_id_and_territory_id_to_users"

# Edit the generated migration file to:
# - ADD citizen_id foreign key to appropriate citizen table
# - ADD territory_id as alternative to region_id (or just use region_id)
```

---

##🧪 VALIDATION CHECKS

After applying fixes, run these:

### Check 1: Model Can Load Records
```python
from app.core.iam.models.user import User
from sqlalchemy import select

async with AsyncSessionLocal() as db:
    stmt = select(User).limit(1)
result = await db.execute(stmt)
user = result.scalars().first()
print(f"✅ Loaded user: {user.email}")  # Should work now!
```

### Check 2: Seed Can Run
```bash
export PYTHONPATH=/home/dev03wsl/sila-system/apps/backend:$PYTHONPATH

# First seed geographic data
python apps/backend/seeds/core/seed_angola_dpa_v3.py

# Then seed users
python apps/backend/seeds/core/seed_founding_users.py --verbose
```

### Check 3: Users Exist
```bash
PGPASSWORD='Trumanmarcelo_1983' psql -h 127.0.0.1 -U sila_user sila_db -c "
SELECT email, status, level, administrative_level FROM users ORDER BY email;
"
```

Expected output after seeds run:
```
            email            | status |  level   | administrative_level
-----------------------------+--------+----------+----------------------
central@sila.gov.ao         | ACTIVE | NATIONAL | ADMIN_CENTRAL
prov.huambo@sila.gov.ao     | ACTIVE | PROVINCIAL | ADMIN_PROVINCIAL
mun.huambo@sila.gov.ao      | ACTIVE | MUNICIPAL | ADMIN_MUNICIPAL
comun.huambo@sila.gov.ao    | ACTIVE | COMMUNAL | ADMIN_COMMUNAL
truman@gmail.com            | ACTIVE | LOCAL | CITIZEN
```

---

## 📋 CHECKLIST

### Phase 1: Fix Models (30 min)
- [ ] **1.1** Update `app/core/iam/models/user.py`
  - [ ] Change `id` from `String` to `Integer`
  - [ ] Add `uuid` field as alternative key
  - [ ] Rename `password_hash` → `hashed_password`
  - [ ] Rename `level` usage or add `administrative_level`
  - [ ] Change `role` to `roles` (+ convert to array in seed)
  - [ ] Rename `territory_id` → `region_id`
  - [ ] Update FK reference: `territories.id` → `locations.id`
  - [ ] Remove unused fields: `username`, `citizen_id` (optional)
  - [ ] Update relationship name from `territory` → `region`

- [ ] **1.2** Verify imports in other files
  - [ ] Search for imports of User model
  - [ ] Check that no code expects old field names

### Phase 2: Fix Seeds (20 min)
- [ ] **2.1** Update SQL seeds:
  - [ ] `seed_founding_users_with_territories.py` - change `iam_users` → `users`
  - [ ] `seed_founding_users.py` - update ORM field names
  - [ ] `seed_*.py` - audit other scripts

### Phase 3: Test Seeds (30 min)
- [ ] **3.1** Seed geographic data:
  ```bash
  python apps/backend/seeds/core/seed_angola_dpa_v3.py
  ```

- [ ] **3.2** Seed users:
  ```bash
  python apps/backend/seeds/core/seed_founding_users.py
  ```

- [ ] **3.3** Validate data:
  ```bash
  psql -h 127.0.0.1 -U sila_user sila_db -c "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM locations;"
  ```

### Phase 4: Verify Access Control (20 min)
- [ ] **4.1** Test user login with each role
- [ ] **4.2** Verify territory/region access restrictions
- [ ] **4.3** Test RBAC enforcement

---

## 🎓 LESSONS LEARNED

1. **Schema Evolution**: Migrations created one schema, but models expected another
2. **Table Names**: `locations` vs `territories`, `users` vs `iam_users`
3. **Field Names**: `region_id` vs `territory_id`, `hashed_password` vs `password_hash`
4. **Seeds Maintenance**: SQL seeds hardcoded table names that don't match ORM
5. **Documentation Gap**: No clear mapping between migrations and models

---

## ⏱️ TIMELINE

- **Completed**: ✅ Root cause analysis & diagnosis
- **Next**: 🔧 Fix models & seeds (this week)
- **Then**: Testing & validation
- **Final**: Documentation update

---

**Owner**: DevOps/Backend Team  
**Next Review**: After fixes applied  
**Status**: ⚠️ AWAITING IMPLEMENTATION
