# Module Federation Plan

## Objective
Consolidate bounded contexts safely without breaking runtime, contracts, or migrations.

Current baseline:
- Modules: 62
- Target domains: 8 (`governance`, `economy`, `social`, `infrastructure`, `environment`, `security`, `identity`, `core_system`)

Execution order (mandatory):
1. scan overlap
2. generate federation plan
3. validate dependencies
4. prepare migrations
5. execute gradual merges

## Cluster 1 - Health

Modules:
- `saude`
- `saude_primaria`

Action:
- Merge into: `healthcare` (or keep `saude` as canonical name and fold `saude_primaria`).

Risk:
- Low

Preconditions:
- align repository ports (`AppointmentRepository`, `MedicalRecordRepository`, `PrescriptionRepository`)
- freeze API routes with compatibility adapters

---

## Cluster 2 - Identity

Modules:
- `identity`
- `identidade_civil`
- `registo_civil`

Action:
- Consolidate into canonical `identity` domain namespace.

Risk:
- Medium

Preconditions:
- preserve current BI/atestados/validacao routes under compatibility prefixes
- validate citizen/document aggregates before model merge

---

## Cluster 3 - Statistics

Modules:
- `statistics`
- `estatistica`

Action:
- Merge into canonical `statistics`.

Risk:
- Low

Preconditions:
- preserve dashboards endpoints and historical metrics contracts
- unify outbox readers and projection jobs

---

## Cluster 4 - Public Finance and Taxation

Modules:
- `financas`
- `financas_publicas`
- `financas_impostos`
- `taxpayer`

Action:
- Federate into `public_finance` domain with subcontexts:
  - `treasury`
  - `budgeting`
  - `taxation`

Risk:
- High

Preconditions:
- complete dependency map validation (`financas -> taxpayer`, integration adapters)
- define anti-corruption layer for external AGT-like boundaries
- execute migration by subcontext, not as big-bang

---

## Cluster 5 - Transport and Ports

Modules:
- `transportes_logistica`
- `portos_logistica`

Action:
- Consolidate into `transport_system`.

Risk:
- Medium

Preconditions:
- align route taxonomy and logistics event model
- preserve operational KPIs for ports and multi-modal transport

---

## Domain Federation Target

- `governance`
- `economy`
- `social`
- `infrastructure`
- `environment`
- `security`
- `identity`
- `core_system`

Recommended namespace direction:
- from: `app.modules.<module>`
- to: `app.domains.<domain>.modules.<module>`

## Migration Guardrails

- Never merge clusters directly after overlap scan.
- Dependency report must show no unresolved cycles for the cluster.
- Keep compatibility routes during at least one release cycle.
- Each cluster merge must include:
  - migration script(s)
  - rollback notes
  - contract test updates
  - report regeneration (`architecture-report`)

## Required Outputs Per Iteration

- `reports/domain_overlap_report.md`
- `reports/module_dependencies.md`
- `reports/architecture_map.md`
- `reports/module_health_report.md`
