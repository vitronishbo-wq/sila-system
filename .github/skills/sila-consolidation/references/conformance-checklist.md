# Consolidation Conformance Checklist

Use this checklist to verify the consolidated module meets structural and architectural requirements.

## Structural Conformance

### Core Directory Structure
- [ ] `app/modules/<MODULE>/core/domain/` exists and contains entity files
- [ ] `app/modules/<MODULE>/core/application/` exists and contains service files
- [ ] `app/modules/<MODULE>/core/infrastructure/` exists with repositories and models
- [ ] No empty directories in core structure

### Domain Layer (`domain/`)
- [ ] All entity files migrated to `entities/`
- [ ] All domain events in `events/` (if any)
- [ ] All value objects in `value_objects/` (if any)
- [ ] `__init__.py` exports all public domain types
- [ ] No application or infrastructure code in domain layer

### Application Layer (`application/`)
- [ ] All service classes documented with `@dataclass` or protocol
- [ ] Ports defined in `ports/` subdirectory (interfaces for external deps)
- [ ] Services accept port instances as dependencies (dependency injection ready)
- [ ] No infrastructure code (no DB access, adapters, or API calls)

### Infrastructure Layer (`infrastructure/`)
- [ ] Repository implementations inherit from domain ports
- [ ] Models use SQLAlchemy ORM or equivalent
- [ ] Adapters isolated for external API calls (X-Road, MinIO, etc.)
- [ ] No business logic in repositories or models
- [ ] Configuration and environment handling centralized

## Dependency Conformance

### No Circular Imports
- [ ] Run: `python scripts/detect-circular-deps.py app/modules/<MODULE>/`
- [ ] Result: zero circular dependencies reported

### Clean Boundaries
- [ ] Module never directly imports from sibling modules (e.g., Justice → Health)
- [ ] All cross-module calls use standardized ports at `infrastructure/ports/`
- [ ] Port implementations use X-Road or event bus for resolution

### Removed Obsolete Structures
- [ ] Deleted: `bounded_contexts/` folder (after extraction)
- [ ] Deleted: Old context-specific folders (civil_registry, vital_events, etc.)
- [ ] Verified: No orphaned files or dangling imports

## Functional Conformance

### Extracted Logic Completeness
- [ ] All citizen/document/record logic consolidated in core
- [ ] All service methods present in unified application layer
- [ ] Database queries updated to use new repository paths
- [ ] API routes updated to reference new service locations

### Test Coverage
- [ ] Unit tests for domain entities pass
- [ ] Unit tests for application services pass
- [ ] Integration tests for repositories pass
- [ ] Test discovery includes new module paths: `pytest app/modules/<MODULE>/tests/`

### API & Event Compliance
- [ ] OpenAPI schema updated with new module endpoints
- [ ] Event producers emit to correct event bus topics
- [ ] Event consumers initialized with new service locations
- [ ] No hardcoded old module paths in configuration

## Documentation Conformance

### README & Architecture Docs
- [ ] Module README updated with new hexagonal structure
- [ ] Architecture docs reference module as single unit, not scattered contexts
- [ ] `module.yaml` (if present) reflects consolidated structure
- [ ] Dependency graph shows module as atomic entity

## Audit Report Generated

- [ ] Compliance checklist output (this document, completed)
- [ ] Parallel batch execution log created
- [ ] Pytest results attached to report
- [ ] Visual report generated: `conformance_<MODULE>_<TIMESTAMP>.md`

---

**Sign-off**: All checkboxes ✅ = **Module consolidated and ready for deployment**
