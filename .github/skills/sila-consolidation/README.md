# SILA Consolidation Skill

**Large-scale service consolidation** for 900+ SILA microservices using hexagonal architecture patterns.

## What This Skill Does

Consolidates fragmented modules (e.g., "justice" with 78 scattered directories) into clean, auditable hexagonal cores by:

1. **Discovering** scattered logic via tree indices (not traversal)
2. **Extracting** domain/application/infrastructure in parallel batches
3. **Unifying** duplicate logic into single source of truth
4. **Replacing** point-to-point adapters with X-Road ports
5. **Auditing** compliance with conformance checklist
6. **Reporting** visual metrics (no prose)

## Key Files

### Core Documentation
- **[SKILL.md](./SKILL.md)** — Main workflow and procedures
- **[Quick Reference](./references/quick-reference.md)** — One-page cheat sheet

### Step-by-Step Guides
- **[Justice Consolidation Example](./references/justice-consolidation.md)** — Detailed walkthrough with code
- **[X-Road Ports Pattern](./references/xroad-ports-pattern.md)** — How to break circular dependencies
- **[Conformance Checklist](./references/conformance-checklist.md)** — Sign-off criteria

### Automated Scripts
- **[consolidate-module.sh](./scripts/consolidate-module.sh)** — Main extraction (6 phases)
- **[audit-consolidation.sh](./scripts/audit-consolidation.sh)** — Compliance audit + reporting
- **[conformance_report.py](./scripts/conformance_report.py)** — Python metrics generator

## The Three Inviolable Rules

1. ⚡ **Discovery via Index** — Use `docs/tree.md` as Ctrl+F index, never traverse
2. 🔄 **Parallel Batch Normalization** — Execute all transforms as single universal operation
3. 📊 **Visual Compliance Output** — Checklist + metrics + tests (no narrative)

## Quick Start

### Consolidate a Module (30 minutes)
```bash
# Extract & unify
./.github/skills/sila-consolidation/scripts/consolidate-module.sh justice

# Audit & report
./.github/skills/sila-consolidation/scripts/audit-consolidation.sh justice

# Output: Conformance report with ✅/❌ status + metrics
```

### In VS Code
Type `/` in chat and select **sila-consolidation** to invoke this skill, or ask:

```
@copilot Consolidate the identity module using sila-consolidation.
Report conformance score and parallel actions executed.
```

## Structure

```
.github/skills/sila-consolidation/
├── SKILL.md                              ← Workflow procedures
├── README.md                             ← This file
├── scripts/
│   ├── consolidate-module.sh            ← Phase 1-4: Extract & unify
│   ├── audit-consolidation.sh           ← Phase 5-6: Audit & report
│   └── conformance_report.py            ← Python metrics generator
└── references/
    ├── quick-reference.md               ← One-page cheat sheet
    ├── justice-consolidation.md         ← Full worked example
    ├── xroad-ports-pattern.md           ← Breaking circular deps
    └── conformance-checklist.md         ← Sign-off template
```

## Use Cases

### Problem: Module Has Too Many Folders
```
Before:  78 directories, 4 citizen implementations, circular imports
After:   1 core, 1 citizen entity, 0 circular imports
Time:    ~30 minutes
Result:  ✅ Audit passing, ready for production
```

### Problem: Circular Dependencies Between Modules
```
Solution: X-Road Ports pattern
- Define abstract ports (interfaces)
- Implement via X-Road adapters
- Break the cycle (A doesn't import B)
```

### Problem: Audit-Ready for Governance
```
Output:
- ✅ Conformance checklist (all components present)
- 📋 Parallel actions log (reproducible execution)
- 🧪 Test results (pytest summary)
- 📊 Conformance score (0-100%)
```

## Workflow at a Glance

| Phase | Duration | Input | Output |
|-------|----------|-------|--------|
| 🔍 Discovery | 2 min | Module name | Scattered logic locations |
| 🏗️ Design | 5 min | Locations | Hexagonal target structure |
| ⚙️ Extract | 10 min | Target design | Consolidated core with imports updated |
| 🧪 Audit | 5 min | Consolidated core | Compliance report + test results |
| 📊 Report | 3 min | Audit results | Visual metrics + checklist |

## Integration with SILA

This skill applies the **three inviolable rules** established for the SILA system:

1. **Massive codebase** (900+ services) → *Use index patterns only*
2. **Global consistency** required → *Parallel batch processing*
3. **Audit-ready output** mandatory → *Visual artifacts, no prose*

Use this skill to consolidate modules systematically while maintaining speed and consistency across the entire SILA platform.

## Next Steps

1. **Read** [Quick Reference](./references/quick-reference.md) (2 minutes)
2. **Review** [Justice Example](./references/justice-consolidation.md) (5 minutes)
3. **Run** `consolidate-module.sh <MODULE>` (10 minutes)
4. **Audit** with `audit-consolidation.sh` (5 minutes)
5. **Sign off** conformance checklist when all ✅

---

**Scope**: Workspace (SILA system)  
**Language**: Python, Bash, YAML  
**Team**: Consolidation & Architecture Review  
**Status**: Production-ready
