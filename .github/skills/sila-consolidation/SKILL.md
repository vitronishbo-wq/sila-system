---
name: sila-governance
description: Execute governance, territorial scope, RBAC, compliance and institutional readiness tasks for SILA System. Prioritize user-visible impact, jurisdiction isolation, administrative hierarchy and safe architectural evolution.
argument-hint: "Specify module, governance problem, territorial rule, permission issue or institutional workflow."
---

# SILA Governance Execution

## Mission

SILA is a governmental platform based on:

- Hexagonal Architecture
- Modular Domain Structure
- X-Road Interoperability
- Compliance-first Governance

Current priority is NOT service consolidation.

Current priority is:

1. RBAC enforcement
2. Territorial isolation
3. Administrative hierarchy
4. Institutional readiness
5. Pilot deployment preparation

---

## Mandatory Bootstrap

Before any analysis:

1. Read AGENT_RULES.md
2. Read docs/tree.json
3. Read docs/modules/tree.modules.json

Fallback:

- docs/tree.md
- docs/modules/tree.modules.txt

If unavailable:

STATUS: BLOQUEADO
MOTIVO: INDEX_UNAVAILABLE

---

## Current Strategic Priorities

### Priority 1

Functional Segregation

Different users must see different systems.

Examples:

Municipal Education
Municipal Health
Provincial Administration
National Administration

Never expose unnecessary modules.

---

### Priority 2

Territorial Scope Enforcement

Every administrative operation must respect:

- territory
- province
- municipality
- institution

Never return administrative data without scope validation.

---

### Priority 3

Administrative Hierarchy

Official hierarchy:

National
→ Province
→ Municipality
→ Institution

Examples of institutions:

- School
- Hospital
- Registry Office
- Social Security Office

Permissions must follow hierarchy.

---

### Priority 4

Integration Maturity

Every external integration must expose status.

Examples:

AGT → Homologation

Multicaixa → Simulated

INSS → Homologation

MINSA → Planned

Users must know when a service is simulated.

---

## Repository Navigation

Use indexes only.

Never:

- scan entire repository
- infer paths
- load large directory trees

Read only files resolved through indexes.

---

## Architectural Rules

Preserve:

- Hexagonal Architecture
- Domain Isolation
- Infrastructure Isolation
- X-Road Boundaries

Never:

- create circular dependencies
- bypass service boundaries
- couple modules directly

---

## Execution Workflow

1. Resolve module through indexes
2. Read relevant files
3. Produce execution plan
4. Implement changes
5. Run validation
6. Update indexes
7. Execute audit

---

## Validation

Required sequence:

make update-indexes

pytest <target>

make daily-audit

---

## Success Criteria

Only declare success when:

- tests passed
- indexes updated
- audit passed
- permissions validated
- territorial scope validated

---

## Output Contract

STATUS:
OK | BLOQUEADO

MODIFICADOS:

ERROS:

CORREÇÕES:

TESTES:

AUDITORIA: