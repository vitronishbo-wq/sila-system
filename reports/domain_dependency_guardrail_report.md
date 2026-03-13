# Domain Dependency Guardrail Report

- Generated at: `2026-03-13 12:26:07Z`
- Status: FAILED

## Summary

- Observed edges: **21**
- Declared modules: **8**
- Graph violations: **3**
- Policy violations: **9**
- Manifest violations: **5**
- Core import violations: **0**
- Cycle violations: **0**

## Graph Violations

| Source | Target | Weight |
| --- | --- | ---: |
| `resources` | `energy` | 1 |
| `economy` | `procurement` | 1 |
| `society` | `saude` | 1 |

## Policy Violations

| Source | Target | Source Domain | Target Domain | Weight |
| --- | --- | --- | --- | ---: |
| `infrastructure` | `core` | `infrastructure` | `core` | 15 |
| `logistics` | `core` | `logistics` | `core` | 6 |
| `energy` | `core` | `energy` | `core` | 4 |
| `procurement` | `core` | `procurement` | `core` | 4 |
| `tourism` | `core` | `tourism` | `core` | 3 |
| `saude` | `core` | `saude` | `core` | 2 |
| `resources` | `energy` | `resources` | `energy` | 1 |
| `economy` | `procurement` | `economy` | `procurement` | 1 |
| `society` | `saude` | `society` | `saude` | 1 |

## Manifest Contract Violations

| Source | Target | Rule | Weight |
| --- | --- | --- | ---: |
| `resources` | `energy` | requires.domains_missing_target | 1 |
| `resources` | `energy` | import_not_exposed:app.modules.energy.api.deps | 1 |
| `economy` | `procurement` | import_not_exposed:app.modules.procurement.api.router | 1 |
| `society` | `saude` | requires.domains_missing_target | 1 |
| `society` | `saude` | import_not_exposed:app.modules.saude.api.deps | 1 |

## Core Import Violations

- None.

## Cycle Violations

- None.
