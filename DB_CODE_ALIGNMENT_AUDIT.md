# 📊 SILA System - Database & Code Alignment Audit

**Date**: 2026-02-22  
**Environment**: Local PostgreSQL (127.0.0.1:5432, sila_db, sila_user)  
**Status**: ⚠️ MISALIGNMENT DETECTED - Schema ✅ Created | Data ❌ EMPTY | Seeds ⚠️ REFERENCE MISMATCH

---

## 🔍 DIAGNOSTIC SUMMARY

| Component | Status | Notes |
|-----------|--------|-------|
| **PostgreSQL Connection** | ✅ OK | Successful (asyncpg + psql verified) |
| **Alembic Migrations** | ✅ APPLIED | 6 migration files successfully executed |
| **Database Tables** | ✅ CREATED | 21 tables exist in schema |
| **User Data** | ❌ EMPTY | 0 users in `users` table |
| **Geographic Data** | ❌ EMPTY | 0 locations in `locations` table |
| **Seed Scripts** | ⚠️ REFERENCE MISMATCH | Scripts reference `iam_users` but table is `users` |
| **SQLAlchemy Models** | ⚠️ MULTIPLE LOCATIONS | Found User models in 3+ different paths |

---

## 📋 DATABASE SCHEMA (21 Tables)

### Core Infrastructure
1. **alembic_version** - Migration tracking
2. **locations** - Geographic hierarchy (provinces, municipalities, communes)
3. **users** - System users (currently empty)
4. **notifications** - User notifications
5. **audit_logs** - System audit trail

### Citizenship/Identity Module
6. **citizenship_citizens** - Citizen records
7. **citizenship_service_requests** - Service requests (B.I., Passport, etc.)
8. **citizenship_services** - Service definitions
9. **citizenship_service_request_history** - Request status tracking
10. **citizenship_atualizacao_b_i** - B.I. update requests
11. **citizenship_atualizacao_b_i_documents** - B.I. update documents
12. **identities** - Identity information linked to users

### Document Management Module
13. **documents** - Document records
14. **document_folders** - Document folder structure
15. **document_versions** - Document version history

### Payment Module
16. **payments** - Payment records
17. **refunds** - Refund records
18. **payment_transactions** - Payment transactions
19. **payment_webhooks** - Webhook configurations
20. **payment_webhook_events** - Webhook event logs
21. **payment_audit_logs** - Payment audit trail

---

## 🔗 FOREIGN KEY RELATIONSHIPS

```
users (id)
  ├── references: locations (id) via region_id
  └── referenced_by:
      ├── audit_logs.user_id
      ├── citizenship_atualizacao_b_i.user_id
      ├── document_folders.owner_id
      ├── document_versions.uploaded_by_id
      ├── documents.owner_id
      ├── identities.user_id
      ├── notifications.user_id
      └── payments.owner_id

locations (id)
  ├── references: locations (id) via parent_id [self-referential, hierarchical]
  └── referenced_by:
      └── users.region_id
```

---

## 👥 TARGET USER SETUP (Not Yet Implemented)

Per requirements, the system needs these 5 test users:

| Email | Role | Level | Territory | Password |
|-------|------|-------|-----------|----------|
| central@sila.gov.ao | ADMIN_CENTRAL | national | NULL | Trumanmarcelo_1983 |
| prov.huambo@sila.gov.ao | ADMIN_PROVINCIAL | provincial | Huambo Province | Trumanmarcelo_1983 |
| mun.huambo@sila.gov.ao | ADMIN_MUNICIPAL | municipal | Huambo Municipality | Trumanmarcelo_1983 |
| comun.huambo@sila.gov.ao | ADMIN_COMMUNAL | communal | Huambo Commune | Trumanmarcelo_1983 |
| truman@gmail.com | CITIZEN | citizen | NULL (or user's home location) | Trumanmarcelo_1983 |

---

## ⚠️ ISSUES IDENTIFIED

### 1. CRITICAL: SQL Schema vs Seed Script Mismatch

**Issue**: Seed script references table `iam_users` but migration created `users`

```
File: apps/backend/seeds/core/seed_founding_users_with_territories.py
Line ~140: UPDATE iam_users SET territory_id = %s, role = %s, level = %s...
              ^^^^^^^^^^^
           Table doesn't exist - should be "users"
```

**Impact**: Seeds cannot run as-is; they will fail with "relation iam_users does not exist"

**Files Affected**:
- ❌ `apps/backend/seeds/core/seed_founding_users_with_territories.py` (uses `iam_users`)
- ❌ `apps/backend/seeds/core/seed_and_token.py` (likely uses `iam_users`)
- ❌ `apps/backend/seeds/core/seed_founding_users.py` (likely uses `iam_users`)
- ❌ `apps/backend/scripts/seed_*.py` (needs validation)

**Solution**: Update all seed scripts to use table name `users` instead of `iam_users`

---

### 2. SQLAlchemy Model Organization Issues

**Issue**: Multiple User model definitions at different paths

Without a single source of truth, ORM mappings may fail or create conflicting metadata.

**Locations Found**:
```
apps/backend/app/core/iam/models/user.py
  └── class User(Base): __tablename__ = "users"

apps/backend/modules/identity/models/user.py
  └── class User(Base): __tablename__ = "users"

app/schemas/user.py
  └── class User(UserBase):  [Pydantic schema, not ORM]
```

**Resolution Path**: 
1. Identify which model is the "canonical" one
2. Remove duplicates
3. Use `core.iam.models.user.User` everywhere as the single source of truth

---

### 3. SQLAlchemy Model vs Database Schema Mismatch

**Current Model** (`app/core/iam/models/user.py`):
```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[str]  # STRING primary key
    email: Mapped[str]
    username: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]
    level: Mapped[str]
    is_active: Mapped[bool]
    citizen_id: Mapped[uuid.UUID | None]  # FK to citizen_fuc.citizen_id
    territory_id: Mapped[uuid.UUID | None]  # FK to territories.id
    timezone: Optional[str]
    theme: Optional[str]
```

**Actual Database Schema** (`users` table):
```sql
id                    INTEGER PRIMARY KEY (not VARCHAR!)
uuid                  VARCHAR(36)
email                 VARCHAR(255)
hashed_password       VARCHAR(255)
phone                 VARCHAR(20)
bi_number             VARCHAR(20)
is_active             BOOLEAN
is_verified           BOOLEAN
status                VARCHAR(20)
region_id             INTEGER (FK to locations)
roles                 JSON
created_at            TIMESTAMP
updated_at            TIMESTAMP
last_login            TIMESTAMP
full_name             VARCHAR(100)
administrative_level  VARCHAR(20)
```

**Mismatches**:
| Model Field | DB Column | Issue |
|------------|-----------|-------|
| `id` (VARCHAR) | `id` (INTEGER) | Type mismatch - Model expects string, DB is integer |
| `password_hash` | `hashed_password` | Field name mismatch |
| `role` (single field) | `roles` (JSON) | Type mismatch - scalar vs array |
| `level` (single field) | `administrative_level` | Field name mismatch |
| `is_active` (present) | `is_active` (present) | ✅ OK |
| `territory_id` (FK) | `region_id` (FK) | Field name completely different |
| `citizen_id` (FK) | MISSING | Field doesn't exist in DB |
| Many model fields | MISSING | `phone`, `bi_number`, `is_verified`, `status`, etc. |

**Impact**: ORM queries will fail when trying to load User objects because column names don't match.

---

### 4. Geographic Data Not Seeded

**Expected**: Hierarchical location structure (21 provinces → municipalities → communes)

**Actual**: 0 locations in database

**Required Seed File**: `apps/backend/seeds/core/seed_angola_dpa_v3.py`

**Files**:
- `seed_angola_dpa_v3.py` - Creates province/municipality/commune hierarchy
- `seed_angola_provinces.py` - Basic province setup
- `seed_fuc_citizen.py` - Citizen data (depends on locations existing first)

---

### 5. Territory vs Location Table Naming

**Confusion**: Models reference `territories` table, but migrations created `locations` table

```python
# In model:
territory: Mapped["Territory"] = relationship("Territory", 
    foreign_keys=[territory_id],
    foreignkey("territories.id")  # References 'territories'
)

# But migration created:
class Location(Base):
    __tablename__ = "locations"  # Not "territories"!
```

**Consequence**: Region hierarchy will reference wrong table name, causing FK constraint failures.

---

## 🛠️ REMEDIATION PLAN

### Phase 1: Fix Schema-Model Mismatches (CRITICAL)

- [ ] **1.1** Update `app/core/iam/models/user.py` to match actual `users` table schema
  - Change `id` from `str` to `int`
  - Rename `password_hash` to match `hashed_password`
  - Change `role` (scalar) to `roles` (JSON array)
  - Rename `level` to `administrative_level`
  - Change `territory_id` FK to match `region_id` column
  - Remove `citizen_id` field (not in table) or add to migration
  - Add missing columns: `phone`, `bi_number`, `is_verified`, `status`, `last_login`, `uuid`

- [ ] **1.2** Consolidate User models (delete duplicate models)
  - Keep only: `app/core/iam/models/user.py`
  - Remove: `modules/identity/models/user.py` (update imports)

- [ ] **1.3** Clarify Location vs Territory naming
  - Decide: Is it `locations` (actual) or `territories` (in models)?
  - Update all FK references to match

### Phase 2: Fix Seed Scripts (BLOCKING)

- [ ] **2.1** Update seed scripts table references
  - Replace `iam_users` → `users` in:
    - `seed_founding_users_with_territories.py`
    - `seed_founding_users.py`
    - `seed_and_token.py`
    - Any script using SQL directly

- [ ] **2.2** Add seed execution order validation
  - Ensure `seed_angola_dpa_v3.py` runs FIRST (creates locations)
  - Then run user seeds (can reference existing locations)

### Phase 3: Populate Seed Data

- [ ] **3.1** Create and run geographic seed
  ```bash
  python apps/backend/seeds/core/seed_angola_dpa_v3.py
  ```

- [ ] **3.2** Create and run user seed
  ```bash
  python apps/backend/seeds/core/seed_founding_users_with_territories.py
  ```

- [ ] **3.3** Verify 5 test users created with correct territories

### Phase 4: Validation & Testing

- [ ] **4.1** Verify all foreign key constraints satisfied
- [ ] **4.2** Test ORM queries load User objects correctly
- [ ] **4.3** Confirm role/territory access control working

---

## 📁 KEY FILES TO UPDATE

**Models**:
- `apps/backend/app/core/iam/models/user.py` - Update schema mapping
- `apps/backend/app/core/location/models/territory.py` or similar - Clarify naming
- `apps/backend/app/core/db/base.py` - Check declarative base setup

**Seeds**:
- `apps/backend/seeds/core/seed_founding_users_with_territories.py` - Fix table name `iam_users` → `users`
- `apps/backend/seeds/core/seed_founding_users.py` - Fix table name
- `apps/backend/seeds/core/seed_and_token.py` - Fix table name
- `applications/backend/seeds/core/seed_angola_dpa_v3.py` - Verify runs first

**Migrations**:
- Review and possibly add new migration to fix User model schema mismatch

---

## 🔧 NEXT STEPS

**Immediate (TODAY)**:
1. ✅ Diagnose schema vs model mismatches [JUST COMPLETED]
2. Create updated User model matching actual schema
3. Update seed scripts to use correct table names
4. Test seed execution

**Short-term (THIS WEEK)**:
1. Consolidate User model locations
2. Run fully populated seeds
3. Verify 5 test users with proper territories
4. Document final schema

**Documentation**:
- [ ] Create migration guide: "From current schema to expected schema"
- [ ] Document role/territory access control rules
- [ ] Add seed execution order documentation

---

**Status**: ⚠️ WORK IN PROGRESS - AWAITING USER ACTION  
**Last Updated**: 2026-02-22 00:00 UTC
