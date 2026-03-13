# Architecture Index Visual Report

- System: `sila-system`
- Generated at: `2026-03-07 13:24:27Z`

## Artifacts

- `ARCHITECTURE_INDEX.yaml`
- `ARCHITECTURE_DEPENDENCIES.yaml`
- `API_MAP.yaml`
- `AI_ENTRYPOINTS.yaml`
- `docs/architecture/REPOSITORY_MAP.yaml`
- `docs/AI_CONTEXT.md`
- `docs/AI_BOOTSTRAP_PROMPT.md`
- `docs/AI_ARCHITECTURE_GRAPH.yaml`
- `docs/AI_DOMAIN_KERNEL.md`
- `reports/ai_architecture_graph_visual_report.md`
- `reports/ai_domain_kernel_visual_report.md`
- `reports/domain_dependency_guardrail_report.md`
- `docs/architecture/entrypoints/`
- `docs/architecture/domains/**/ARCHITECTURE.md`
- `apps/backend/app/modules/*/ARCHITECTURE.md`

## Summary

- Modules indexed: **62**
- Dependency edges: **65**
- Circular dependency groups: **0**
- API endpoints mapped: **306**

## Dependency Graph (Top 30 Edges)

```mermaid
graph LR
  pescas_industriais -->|5| pescas
  service_requests -->|5| juventude
  workflow -->|5| assistencia_social
  workflow -->|5| educacao
  financas -->|4| educacao
  financas -->|4| juventude
  statistics -->|3| assistencia_social
  statistics -->|3| saude
  statistics -->|3| emprego
  juventude -->|3| educacao
  juventude -->|3| emprego
  identidade_civil -->|3| educacao
  identidade_civil -->|3| emprego
  saude -->|3| educacao
  saude -->|3| emprego
  service_requests -->|3| emprego
  bi -->|3| financas_publicas
  assistencia_social -->|3| educacao
  assistencia_social -->|3| emprego
  assistencia_social -->|3| juventude
  workflow -->|3| emprego
  workflow -->|3| juventude
  workflow -->|3| saude
  statistics -->|2| educacao
  statistics -->|2| identidade_civil
  statistics -->|2| juventude
  statistics -->|2| workflow
  financas_publicas -->|2| assistencia_social
  financas_publicas -->|2| agricultura
  financas_publicas -->|2| educacao
```
