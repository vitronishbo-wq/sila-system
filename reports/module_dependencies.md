# Module Dependencies Report

- Generated at: `2026-03-18 19:44:18Z`
- Scope: `apps/backend/app/modules`

## Summary

- Modules scanned: **29**
- Python files parsed: **8283**
- Dependency edges (distinct): **2**
- Circular dependency groups: **0**

## Top Dependency Edges

| Source | Target | Import count |
| --- | --- | ---: |
| `economy` | `core` | 2 |
| `identity` | `core` | 1 |

## Hotspots

### Outbound

| Module | Outbound imports | Distinct targets |
| --- | ---: | ---: |
| `economy` | 2 | 1 |
| `identity` | 1 | 1 |
| `industry` | 0 | 0 |
| `educacao` | 0 | 0 |
| `logistics` | 0 | 0 |
| `saude` | 0 | 0 |
| `governance` | 0 | 0 |
| `compliance` | 0 | 0 |
| `procurement` | 0 | 0 |
| `xroad` | 0 | 0 |
| `payment` | 0 | 0 |
| `operations` | 0 | 0 |
| `infrastructure_sector` | 0 | 0 |
| `resources` | 0 | 0 |
| `energy` | 0 | 0 |
| `civil_protection` | 0 | 0 |
| `justice` | 0 | 0 |
| `notifications` | 0 | 0 |
| `wallet` | 0 | 0 |
| `society` | 0 | 0 |
| `intelligence` | 0 | 0 |
| `documents` | 0 | 0 |
| `tourism` | 0 | 0 |
| `audit` | 0 | 0 |
| `tests` | 0 | 0 |
| `public_security` | 0 | 0 |
| `api` | 0 | 0 |
| `infrastructure` | 0 | 0 |
| `migration_service` | 0 | 0 |

### Inbound

| Module | Inbound imports |
| --- | ---: |
| `core` | 3 |

## Circular Dependencies

- No circular dependency groups detected.

## Dependency Graph (Mermaid)

```mermaid
graph LR
  economy -->|2| core
  identity -->|1| core
```

## Evidence Samples

### `economy` -> `core`

- `economy/infrastructure/models/payment_model.py:7 from app.core.db import Base`
- `economy/infrastructure/models/invoice_model.py:7 from app.core.db import Base`

### `identity` -> `core`

- `identity/infrastructure/repositories/citizen_repository.py:1 from app.core.bridges.citizen_repository_bridge import CitizenRepository as CanonicalCitizenRepository`
