# Governance Module - Alembic Migration Guide

## 📋 Overview

This document describes the Alembic migration for the Governance module tables. The
migration creates four tables:

1. **institutions** - Government institutions and organizations
2. **mandates** - Government mandates and authorizations
3. **council_meetings** - Municipal council meetings
4. **decisions** - Governance decisions and resolutions

## 📁 Migration File

**Location:** `backend/alembic/versions/20250105_governance_module_tables.py`

**Revision ID:** `20250105_governance`

**Down Revision:** `20250105_health` (Health module migration)

## 🏗️ Table Structure

### Institutions Table

- **Primary Key:** `id` (UUID)
- **Foreign Keys:**
  - `parent_institution_id` → `institutions.id` (self-referential, nullable)
- **Indexes:**
  - `id`, `name`, `institution_type`, `parent_institution_id`, `deleted_at`
- **Features:**
  - UUID primary key
  - Soft delete (`deleted_at`)
  - Timestamps (`created_at`, `updated_at`)
  - JSON fields: `contact_info`, `leadership`

### Mandates Table

- **Primary Key:** `id` (UUID)
- **Foreign Keys:**
  - `institution_id` → `institutions.id` (nullable, SET NULL on delete)
- **Indexes:**
  - `id`, `title`, `mandate_type`, `start_date`, `status`, `institution_id`,
    `deleted_at`
- **Features:**
  - UUID primary key
  - Soft delete (`deleted_at`)
  - Timestamps (`created_at`, `updated_at`)
  - JSON fields: `scope`, `related_documents`
  - Default status: `"active"`

### Council Meetings Table

- **Primary Key:** `id` (UUID)
- **Foreign Keys:** None (council_id is a UUID reference, not a foreign key constraint)
- **Indexes:**
  - `id`, `title`, `start_time`, `status`, `council_id`, `deleted_at`
- **Features:**
  - UUID primary key
  - Soft delete (`deleted_at`)
  - Timestamps (`created_at`, `updated_at`)
  - JSON fields: `agenda`, `minutes`, `decisions`, `participants`
  - Default status: `"scheduled"`

### Decisions Table

- **Primary Key:** `id` (UUID)
- **Foreign Keys:**
  - `meeting_id` → `council_meetings.id` (nullable, SET NULL on delete)
- **Indexes:**
  - `id`, `title`, `decision_type`, `status`, `meeting_id`, `deleted_at`
- **Features:**
  - UUID primary key
  - Soft delete (`deleted_at`)
  - Timestamps (`created_at`, `updated_at`)
  - JSON fields: `voting_record`, `related_documents`
  - Default status: `"proposed"`

## 🚀 Usage

### Apply Migration

```bash
# From the backend directory
cd backend

# Check current migration status
alembic current

# View migration history
alembic history

# Apply all pending migrations (including Governance)
alembic upgrade head

# Apply only up to Governance migration
alembic upgrade 20250105_governance
```

### Rollback Migration

```bash
# Rollback to previous revision (Health module)
alembic downgrade 20250105_health

# Rollback one step
alembic downgrade -1
```

### Verify Tables

After applying the migration, verify the tables were created:

```sql
-- Connect to PostgreSQL
psql -U sila_user -d sila_db

-- List Governance tables
\dt institutions
\dt mandates
\dt council_meetings
\dt decisions

-- Check table structure
\d institutions
\d mandates
\d council_meetings
\d decisions

-- Verify indexes
\di ix_institutions_*
\di ix_mandates_*
\di ix_council_meetings_*
\di ix_decisions_*
```

## ✅ Validation Checklist

After applying the migration, verify:

- [ ] All 4 tables are created
- [ ] Primary keys are UUIDs
- [ ] Foreign keys are properly set (institutions → mandates, council_meetings →
      decisions)
- [ ] Soft delete columns (`deleted_at`) exist and are indexed
- [ ] Timestamp columns (`created_at`, `updated_at`) exist with defaults
- [ ] JSON columns are properly defined
- [ ] All indexes are created
- [ ] Default values are set (mandates.status = "active", council_meetings.status =
      "scheduled", decisions.status = "proposed")

## 🔄 Migration Chain

The migration chain is:

```
74535044d6a9 (initial_migration)
  ↓
a1b2c3d4e5f6 (pgcrypto_extension)
  ↓
20250105_health (Health module)
  ↓
20250105_governance (Governance module) ← Current
```

## 📝 Notes

1. **Foreign Key Constraints:**

   - `institutions.parent_institution_id` uses `SET NULL` on delete (allows orphaned
     departments)
   - `mandates.institution_id` uses `SET NULL` on delete (preserves mandate history)
   - `decisions.meeting_id` uses `SET NULL` on delete (preserves decision history)

2. **Self-Referential Foreign Key:**

   - The `institutions` table has a self-referential foreign key for parent institutions
   - This allows hierarchical organization structures

3. **JSON Fields:**

   - All JSON columns use `postgresql.JSON(astext_type=sa.Text())` for compatibility
   - JSON fields are nullable and can store flexible data structures

4. **Soft Delete:**

   - All tables implement soft delete via `deleted_at` column
   - Soft-deleted records are filtered out by the repository layer
   - Indexes on `deleted_at` improve query performance

5. **Production Readiness:**
   - Migration is idempotent-safe (can be run multiple times)
   - Downgrade path is fully implemented
   - All foreign keys have appropriate cascade behaviors
   - Indexes are optimized for common query patterns

## 🐛 Troubleshooting

### Migration Fails with Foreign Key Error

If you encounter foreign key errors, ensure:

1. The Health module migration (`20250105_health`) has been applied
2. The `institutions` table is created before `mandates`
3. The `council_meetings` table is created before `decisions`

### JSON Type Errors

If you see JSON type errors, ensure PostgreSQL version is 9.4+ (JSON support) or 9.5+
(JSONB support).

### Index Creation Fails

If index creation fails, check:

1. No existing indexes with the same name
2. Sufficient database permissions
3. No locked tables

## 🔗 Related Documentation

- [Governance Module README](../governance/README.md)
- [Seed Data Guide](./seed_data.py)
- [Repository Tests](../governance/tests/test_repository.py)
- [Health Module Migration](../alembic/versions/20250105_health_module_tables.py)
