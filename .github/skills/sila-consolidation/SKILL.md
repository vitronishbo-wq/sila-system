---
name: sila-consolidation
description: 'Consolidate 900+ SILA services using hexagonal architecture. Use for: unifying scattered domain logic, replacing point-to-point adapters with X-Road ports, eliminating circular dependencies, generating compliance audits. Applies the three inviolable rules: tree-index discovery, parallel batch normalization, and visual compliance reporting.'
argument-hint: 'Specify module to consolidate (e.g., "justice", "identity", "health") or describe the structural problem'
---

# SILA Consolidation Pattern

Large-scale service unification for the SILA system, consolidating 900+ microservices into clean, auditable hexagonal modules.

## Three Inviolable Rules

1. **Context Extraction via Index, Not Traversal**
   - Use `docs/tree.md` and `docs/modules/tree.txt` as indices only (simulate Ctrl+F)
   - Extract with `Get-ChildItem`, `find`, `grep`, `Select-String` — never load full project
   - Avoids context bloat; guarantees speed and objectivity for massive codebases

2. **Parallel Batch Normalization as Universal Operation**
   - After confirming context, organize actions by specificity (health, router, exceptions, BaseRepository, infrastructure, etc.)
   - Apply all transformations in disciplined parallel execution
   - Treat scattered changes as a single normalization instruction ensuring global consistency

3. **Visual Compliance-Only Output**
   - Consolidated conformance checklist (required components present)
   - List of all actions applied in parallel batches
   - Final audit via `pytest` and validation suite
   - No prose narration — visual artifacts and metrics only

## When to Use

- Reducing circular dependencies (e.g., Module A imports B, B imports A)
- Consolidating replicated logic spread across N bounded contexts
- Replacing point-to-point adapters with standardized interop ports
- Eliminating empty, obsolete, or fragmented directories
- Auditing module compliance before deployment
- Scaling from 900 services to manageable core + adapters

## The Consolidation Workflow

### Phase 1: Index-Based Discovery

**Goal**: Map the structural problem without reading the whole codebase

1. Query `docs/tree.md` for the target module
   ```bash
   grep -n "^# <MODULE>" docs/tree.md
   grep -A 50 "## <MODULE>" docs/modules/tree.txt
   ```

2. Identify scattered logic using keyword search
   ```bash
   grep -r "citizen\|birth_record\|bilhete" docs/tree.md
   # Locate all files touching the domain entity across contexts
   ```

3. Document the **structural fragmentation** (example: citizen logic in 4 places)
   ```
   Scattered logic found in:
   - bounded_contexts/application/services/
   - bounded_contexts/civil_registry_core/
   - civil_registry/application/
   - vital_events/application/
   ```

### Phase 2: Hexagonal Core Design

**Goal**: Define the unified target structure

Target structure (always):
```
app/modules/<MODULE>/core/
├── domain/
│   ├── entities/
│   ├── events/
│   └── value_objects/
├── application/
│   ├── ports/
│   └── services/
└── infrastructure/
    ├── models/
    ├── repositories/
    └── adapters/
```

### Phase 3: Batch Extraction & Migration

**Goal**: Pull all scattered logic into core using parallel operations

Using [consolidation script](./scripts/consolidate-module.sh):

```bash
# Prepare target structure
mkdir -p app/modules/<MODULE>/core/{domain,application,infrastructure}

# Extract domain entities (parallel batch 1)
mv bounded_contexts/<BC1>/domain/entities/* app/modules/<MODULE>/core/domain/ 2>/dev/null
mv bounded_contexts/<BC2>/domain/entities/* app/modules/<MODULE>/core/domain/ 2>/dev/null

# Extract application services (parallel batch 2)
mv bounded_contexts/application/services/*.py app/modules/<MODULE>/core/application/ 2>/dev/null
mv <MODULE>/application/services/*.py app/modules/<MODULE>/core/application/ 2>/dev/null

# Replace adapters with X-Road ports (parallel batch 3)
rm -rf bounded_contexts/infrastructure/adapters/*
# Create new ports at app/modules/<MODULE>/core/infrastructure/ports/
```

### Phase 4: Purge Obsolete Contexts

**Goal**: Remove redundant folder structures after extraction

```bash
# After verifying extraction succeeded
rm -rf app/modules/<MODULE>/bounded_contexts
rm -rf app/modules/<MODULE>/<old_context_1>
rm -rf app/modules/<MODULE>/<old_context_2>
```

### Phase 5: Apply Circular Dependency Rule

**Goal**: Prevent coupling spirals (A→B, B→A)

After consolidation:
- Module never imports from sibling modules (e.g., Justice doesn't import Health)
- All cross-module calls via standardized **Ports** → X-Road resolution
- Document in [conformance checklist](./references/conformance-checklist.md)

### Phase 6: Audit & Report

**Goal**: Generate compliance artifacts

Using [audit script](./scripts/audit-consolidation.sh):

```bash
# Run compliance checks
pytest tests/conftest_consolidation.py -v --tb=short

# Generate visual reports
python scripts/conformance_report.py --module=<MODULE> --output=report.md
```

**Output artifacts**:
- ✅ Compliance checklist (all required components present)
- 📋 Actions applied (sorted by execution batch)
- 🧪 Test results (pytest summary))

## Example: Consolidating Justice Module

See [justice-consolidation.md](./references/justice-consolidation.md) for a detailed walkthrough.

## Batch Execution Strategy

Commands organized by execution order (sequential) + parallelism within each batch:

**Batch 1** (Discovery & Design): Sequential
```
- Tree search
- Context mapping
- Design hexagonal target
```

**Batch 2** (Extraction): Parallel (file I/O independent)
```bash
# Run in parallel:
task1: mv domain/entities/* → core/domain/
task2: mv application/services/* → core/application/
task3: copy infrastructure/models/* → core/infrastructure/
```

**Batch 3** (Purge & Audit): Sequential (depends on Batch 2)
```
- Remove old contexts (after extraction verified)
- Run tests
- Generate reports
```

## Anti-Patterns to Avoid

- ❌ Reading entire codebase before consolidation
- ❌ Moving files without understanding dependency chains
- ❌ Leaving adapters that create circular imports
- ❌ Purging before audit passes
- ❌ Prose-heavy reports instead of visual metrics
- ❌ Consolidating without X-Road port layer for interop

## Supporting Resources

- [Conformance Checklist](./references/conformance-checklist.md) — Required components per module
- [Justice Consolidation Example](./references/justice-consolidation.md) — Step-by-step example
- [X-Road Ports Pattern](./references/xroad-ports-pattern.md) — How to define interop boundaries

## Scripts

- [consolidate-module.sh](./scripts/consolidate-module.sh) — Main extraction script
- [audit-consolidation.sh](./scripts/audit-consolidation.sh) — Compliance & reporting
- [conformance_report.py](./scripts/conformance_report.py) — Visual compliance generation

## Mandatory Safety Constraints

- Never delete modules before audit passes
- Never overwrite domain entities without backup
- Always preserve git traceability
- Always generate migration summary before purge
- All destructive operations require verification checkpoint