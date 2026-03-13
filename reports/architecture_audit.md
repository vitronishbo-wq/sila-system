# SILA ARCHITECTURE AUDIT (E2E)

## Summary
- modules: 56
- circular_import_risk: 0
- domain_importing_infra: 2
- domain_importing_session: 0
- missing_health: 0
- missing_router: 0
- parse_errors: 0
- critical_lt_40: 0

## Compliance By Module
| Module | Score | Domain | Application | Infrastructure | Router | Health | Issues |
|---|---:|:---:|:---:|:---:|:---:|:---:|---|
| justice._deprecated | 70 | Y | Y | Y | Y | Y | domain_importing_infrastructure, domain_importing_platform |
| audit.state_audit | 100 | Y | Y | Y | Y | Y | none |
| economy.apoio_empresarial | 100 | Y | Y | Y | Y | Y | none |
| economy.core | 100 | Y | Y | Y | Y | Y | none |
| economy.public_budget | 100 | Y | Y | Y | Y | Y | none |
| economy.taxpayer | 100 | Y | Y | Y | Y | Y | none |
| economy.trade | 100 | Y | Y | Y | Y | Y | none |
| economy.trade.external | 100 | Y | Y | Y | Y | Y | none |
| economy.trade.services | 100 | Y | Y | Y | Y | Y | none |
| educacao.core | 100 | Y | Y | Y | Y | Y | none |
| governance.administracao_local | 100 | Y | Y | Y | Y | Y | none |
| governance.cooperacao_internacional | 100 | Y | Y | Y | Y | Y | none |
| governance.planeamento | 100 | Y | Y | Y | Y | Y | none |
| governance.service_requests | 100 | Y | Y | Y | Y | Y | none |
| governance.statistics | 100 | Y | Y | Y | Y | Y | none |
| governance.workflow | 100 | Y | Y | Y | Y | Y | none |
| industry.core | 100 | Y | Y | Y | Y | Y | none |
| infrastructure.core.domain | 100 | Y | Y | Y | Y | Y | none |
| infrastructure_sector.aviacao_civil | 100 | Y | Y | Y | Y | Y | none |
| infrastructure_sector.gestao_fundiaria | 100 | Y | Y | Y | Y | Y | none |
| infrastructure_sector.logistica | 100 | Y | Y | Y | Y | Y | none |
| infrastructure_sector.logistica.ports | 100 | Y | Y | Y | Y | Y | none |
| infrastructure_sector.meteorologia | 100 | Y | Y | Y | Y | Y | none |
| infrastructure_sector.telecomunicacoes | 100 | Y | Y | Y | Y | Y | none |
| infrastructure_sector.urbanismo_habitacao | 100 | Y | Y | Y | Y | Y | none |
| intelligence.arquivo_nacional | 100 | Y | Y | Y | Y | Y | none |
| intelligence.bi | 100 | Y | Y | Y | Y | Y | none |
| intelligence.ciencia_pesquisa | 100 | Y | Y | Y | Y | Y | none |
| intelligence.defesa_consumidor | 100 | Y | Y | Y | Y | Y | none |
| intelligence.operations | 100 | Y | Y | Y | Y | Y | none |
| intelligence.tecnologia_inovacao | 100 | Y | Y | Y | Y | Y | none |
| justice.core | 100 | Y | Y | Y | Y | Y | none |
| justice.events | 100 | Y | Y | Y | Y | Y | none |
| logistics.core.domain | 100 | Y | Y | Y | Y | Y | none |
| resources.agricultura | 100 | Y | Y | Y | Y | Y | none |
| resources.aguas_saneamento | 100 | Y | Y | Y | Y | Y | none |
| resources.ambiente | 100 | Y | Y | Y | Y | Y | none |
| resources.florestas | 100 | Y | Y | Y | Y | Y | none |
| resources.pecuaria | 100 | Y | Y | Y | Y | Y | none |
| resources.pescas | 100 | Y | Y | Y | Y | Y | none |
| resources.pescas.industrial | 100 | Y | Y | Y | Y | Y | none |
| resources.petroleo_gas | 100 | Y | Y | Y | Y | Y | none |
| resources.recursos_minerais | 100 | Y | Y | Y | Y | Y | none |
| resources.seguranca_alimentar | 100 | Y | Y | Y | Y | Y | none |
| saude.core | 100 | Y | Y | Y | Y | Y | none |
| society.assistencia_social | 100 | Y | Y | Y | Y | Y | none |
| society.cultura | 100 | Y | Y | Y | Y | Y | none |
| society.desporto | 100 | Y | Y | Y | Y | Y | none |
| society.emprego | 100 | Y | Y | Y | Y | Y | none |
| society.familia | 100 | Y | Y | Y | Y | Y | none |
| society.igualdade | 100 | Y | Y | Y | Y | Y | none |
| society.juventude | 100 | Y | Y | Y | Y | Y | none |
| society.patrimonio_cultural | 100 | Y | Y | Y | Y | Y | none |
| society.seguranca_social | 100 | Y | Y | Y | Y | Y | none |
| society.trabalho_inspecao | 100 | Y | Y | Y | Y | Y | none |
| tourism.core | 100 | Y | Y | Y | Y | Y | none |

## Critical (<40)
- none

## Violations
### circular_import_risk
- none

### domain_importing_infra
- apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/domain/aggregates/citizen_aggregate.py
- apps/backend/app/modules/justice/_deprecated/civil_registry/domain/models/document.py

### domain_importing_session
- none

### missing_health
- none

### missing_router
- none

### parse_errors
- none

