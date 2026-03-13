# Quick Reference: SILA Consolidation Workflow

**One-page summary of the three inviolable rules and core workflow.**

## The Three Inviolable Rules

### Rule 1: Discovery via Index
```bash
# DO: Use tree as index, search for keywords
grep -n "citizen\|birth_record" docs/tree.md
grep -n "^# justice" docs/modules/tree.txt

# DON'T: Load/traverse entire codebase
find . -type f -name "*.py" -exec cat {} \;  # ❌ Never
```

### Rule 2: Parallel Batch Normalization
```bash
# DO: Organize by specificity + parallel execution
Batch 1: Extract domain/entities (parallel I/O)
Batch 2: Extract application/services (parallel I/O)
Batch 3: Remove adapters, create ports (sequential)

# DON'T: Sequential file-by-file transformations
for file in $(find ...); do mv $file ...; done  # ❌ Slow
```

### Rule 3: Visual Compliance Output Only
```bash
# DO: Automation generates
- ✅ Conformance checklist (components present)
- 📋 Parallel batch actions (what ran)
- 🧪 Test results (pytest summary)
- 📊 Metrics (entity count, score %)

# DON'T: Narrative prose, storytelling, explanations
# ❌ "We discovered the following issues..."
```

---

## Workflow: 6 Phases in ~30 minutes

| Phase | Duration | What | Command |
|-------|----------|------|---------|
| 1️⃣ Discovery | 2 min | Find scattered logic | `grep MODULE docs/tree.md` |
| 2️⃣ Design | 5 min | Define hexagonal target | mkdir -p core/{domain,application,infrastructure} |
| 3️⃣ Extract | 10 min | Move files in parallel batches | `./consolidate-module.sh <MODULE>` |
| 4️⃣ Unify | 5 min | Merge duplicate services | Update imports, consolidate logic |
| 5️⃣ Audit | 5 min | Verify compliance | `./audit-consolidation.sh <MODULE>` |
| 6️⃣ Report | 3 min | Generate visual metrics | `pytest`, conformance checklist |

---

## Example: Consolidate "justice" Module

### Full Command
```bash
# Phase 1-4: Extract & consolidate
./.github/skills/sila-consolidation/scripts/consolidate-module.sh justice

# Phase 5-6: Audit & report
./.github/skills/sila-consolidation/scripts/audit-consolidation.sh justice

# Alternative: Python report generation
python .github/skills/sila-consolidation/scripts/conformance_report.py \
  --module justice --output /tmp/justice_report.md
```

### Expected Output
```
✅ CONSOLIDATION COMPLETE: justice
  Core location: app/modules/justice/core/
  Layers created: domain, application, infrastructure
  Migration log: /tmp/consolidation_justice_1710123456.log
  Conformance checklist: /tmp/conformance_justice_20260312_120000.md

Next steps:
  1. Review /tmp/conformance_justice_20260312_120000.md
  2. Run: pytest app/modules/justice/tests/
  3. Run: ./audit-consolidation.sh justice
```

---

## Core Patterns

### Hexagonal Structure (Always)
```
app/modules/<MODULE>/core/
├── domain/        ← Entities, events, value objects (0 imports from app)
├── application/   ← Services, use cases (imports domain + ports only)
└── infrastructure/← Adapters, repositories, models (implements ports)
    └── ports/     ← Abstract interfaces (no implementation)
```

### Port Pattern (X-Road Boundary)
```python
# Define port (interface)
class BIIssuerPort(ABC):
    @abstractmethod
    async def request_bi(self, citizen_id: str) -> str:
        pass

# Implement via adapter
class XRoadBIAdapter(BIIssuerPort):
    async def request_bi(self, citizen_id: str) -> str:
        response = await httpx.get(f"{self.xroad}/{citizen_id}")
        return response.json()["bi"]

# Inject into service (no direct imports)
citizen_service = CitizenService(bi_port=XRoadBIAdapter(...))
```

### Circular Dependency Check
```bash
# Find problematic imports (should return 0)
find app/modules/justice/core -name "*.py" -exec grep -l \
  "from app.modules.(health|education|finance)" {} \;

# Result: (empty list) = ✅ PASS
```

---

## Checklists

### Before Consolidation
- [ ] Module identified (e.g., "justice" has 78 folders, logic scattered in 4+ places)
- [ ] Target module name chosen
- [ ] `docs/tree.md` confirms structure

### During Consolidation
- [ ] Batch 1 (domain extraction) completed
- [ ] Batch 2 (application services) completed
- [ ] Batch 3 (port creation) completed
- [ ] Imports updated (old paths → core paths)

### After Consolidation
- [ ] Tests pass: `pytest app/modules/<MODULE>/core/tests/`
- [ ] No circular imports: `grep -r "from app.modules.*bounded_contexts" ...` = 0
- [ ] Conformance report generated
- [ ] Checklist reviewed and signed off

---

## Key Files

| File | Purpose |
|------|---------|
| [SKILL.md](./SKILL.md) | Main workflow (this file references it) |
| [justice-consolidation.md](./references/justice-consolidation.md) | Detailed walkthrough example |
| [xroad-ports-pattern.md](./references/xroad-ports-pattern.md) | How to design X-Road boundaries |
| [conformance-checklist.md](./references/conformance-checklist.md) | Sign-off checklist template |
| [consolidate-module.sh](./scripts/consolidate-module.sh) | Main extraction script |
| [audit-consolidation.sh](./scripts/audit-consolidation.sh) | Audit & report script  |
| [conformance_report.py](./scripts/conformance_report.py) | Visual metrics generator |

---

## Invocation

### Via `/` slash command in VS Code
Type `/` in chat and search for **"sila-consolidation"** → loads this skill

### Manual Trigger in Prompt
```
@copilot Consolidate the justice module using the
sila-consolidation skill. Report conformance score
and parallel actions only (no narrative).
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | Confirm `app/modules/<MODULE>/core/` doesn't already exist |
| Tests fail after consolidation | Check import paths updated (old → core) |
| Circular import detected | Remove sibling module imports, use ports instead |
| Audit takes too long | Skip pytest (`--tb=no` flag) if just checking structure |
| Report output is prose | Use `--json` flag or `audit-consolidation.sh` for metrics-only output |

---

## Scaling: 900 Services

For SILA's 900 services:
1. **Batch consolidate** by domain (Justice → Health → Education → ...)
2. **Parallel execution** across independent modules
3. **Unified X-Road layer** prevents circular imports
4. **Automated compliance** ensures every module follows hexagonal pattern
5. **Metrics dashboard** tracks consolidation progress across all modules

Each module takes ~30 minutes. Full system: 450 hours sequential → ~10 hours parallel.
