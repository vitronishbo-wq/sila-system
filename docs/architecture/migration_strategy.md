# Migration Strategy (Domain-Oriented)

## Goal
Scale database evolution for 60+ modules without turning Alembic into an operational bottleneck.

## Current State
- Single Alembic stream in `apps/backend/alembic/versions`
- Fast growth of revisions from multiple domains
- Risk: merge conflicts, slow review, migration coupling

## Target Model
Use a **single Alembic runtime** with **domain-scoped governance** first, then optional physical split.

Phase 1 (immediate):
- keep one Alembic chain
- enforce domain tag in migration filename and header comment
- generate inventory report grouped by domain

Phase 2 (when needed):
- move to domain folders while preserving a unified execution order
- examples:
  - `migrations/core/`
  - `migrations/identity/`
  - `migrations/social/`
  - `migrations/economy/`

## Naming Convention (mandatory)

Pattern:
- `<timestamp>_<seq>_<domain>_<description>.py`

Examples:
- `20260310_001_identity_add_citizen_indexes.py`
- `20260310_002_social_health_add_triage_table.py`
- `20260310_003_economy_taxation_add_retencao.py`

## Domain Set
- `governance`
- `economy`
- `social`
- `infrastructure`
- `environment`
- `security`
- `identity`
- `core_system`

## Review Rules
- each migration must declare impacted domain(s)
- cross-domain migrations require explicit rationale
- avoid combining unrelated domains in one revision
- rollback notes required for destructive operations

## Operational Rules
- run migration report before merge:
  - `python3 scripts/migration_domain_inventory.py --output reports/migration_domain_inventory.md`
- keep revisions linear and deterministic
- validate both `upgrade` and `downgrade` paths in CI for critical domains

## Exit Criteria for Phase 1
- 100% of new migrations tagged by domain
- migration inventory generated in CI artifacts
- no untagged migration merged

