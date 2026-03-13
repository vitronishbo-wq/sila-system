# Domain Overlap Report

- Generated at: `2026-03-07 13:24:31Z`
- Scope: `apps/backend/app/modules`

## Summary

- Modules scanned: **62**
- Python files parsed: **6976**
- Cross-import edges (total): **145**
- Cross-import edges (distinct): **65**
- Shared entity names detected: **0**
- Shared repository names detected: **28**
- Candidate overlap pairs: **82**

## Candidate Module Merges

| Pair | Score | Name overlap | Concept overlap | Direct cross-imports | Shared entities | Shared repositories |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `saude` + `saude_primaria` | 12.36 | 0.5 | 0.43 | 0 | - | AppointmentRepository, HealthUnitRepository, HealthcareRepository |
| `aguas_saneamento` + `energia` | 6.93 | 0.0 | 0.46 | 0 | - | BaseOutboxRepository, SQLAlchemyConsumoRepository, SQLAlchemyFaturaRepository |
| `educacao` + `emprego` | 6.61 | 0.0 | 0.3 | 0 | - | SQLAlchemyConcursoRepository, SQLAlchemyFormacaoRepository, SQLAlchemyInscricaoRepository |
| `identidade_civil` + `identity` | 6.05 | 0.5 | 0.28 | 0 | - | CitizenRepository |
| `estatistica` + `statistics` | 5.95 | 1.0 | 0.22 | 0 | - | - |
| `aguas_saneamento` + `telecomunicacoes` | 5.23 | 0.0 | 0.36 | 0 | - | SQLAlchemyFaturaRepository, SQLAlchemyInfraestruturaRepository, SQLAlchemyOutboxRepository |
| `educacao` + `juventude` | 4.5 | 0.0 | 0.25 | 3 | - | SQLAlchemyFormacaoRepository, SQLAlchemyWorkflowRepository |
| `emprego` + `juventude` | 4.5 | 0.0 | 0.25 | 3 | - | SQLAlchemyFormacaoRepository, SQLAlchemyWorkflowRepository |
| `financas` + `financas_publicas` | 4.35 | 0.5 | 0.18 | 0 | - | - |
| `financas` + `financas_impostos` | 4.31 | 0.5 | 0.15 | 0 | - | - |
| `financas_impostos` + `taxpayer` | 4.14 | 0.5 | 0.07 | 0 | - | - |
| `aguas_saneamento` + `obras_publicas` | 3.93 | 0.0 | 0.46 | 0 | - | Repository, SQLAlchemyOutboxRepository |
| `financas_impostos` + `financas_publicas` | 3.85 | 0.33 | 0.18 | 0 | - | - |
| `identidade_civil` + `registo_civil` | 3.83 | 0.33 | 0.16 | 0 | - | - |
| `ambiente` + `gestao_fundiaria` | 3.79 | 0.0 | 0.4 | 0 | - | SQLAlchemyImovelRepository, SQLAlchemyProprietarioRepository |
| `portos_logistica` + `transportes_logistica` | 3.68 | 0.33 | 0.09 | 0 | - | - |
| `energia` + `telecomunicacoes` | 3.61 | 0.0 | 0.3 | 0 | - | SQLAlchemyFaturaRepository, SQLAlchemyOutboxRepository |
| `defesa_consumidor` + `emprego` | 3.31 | 0.0 | 0.15 | 0 | - | SQLAlchemyMediacaoRepository, SQLAlchemyReclamacaoRepository |
| `assistencia_social` + `seguranca_social` | 3.17 | 0.33 | 0.33 | 0 | - | SQLAlchemyBeneficiarioRepository |
| `desporto` + `obras_publicas` | 3.11 | 0.0 | 0.3 | 1 | - | SQLAlchemyOutboxRepository |
| `pescas` + `pescas_industriais` | 3.11 | 0.5 | 0.3 | 5 | - | - |
| `desporto` + `educacao` | 3.05 | 0.0 | 0.28 | 1 | - | SQLAlchemyTransferenciaRepository |
| `igualdade` + `migracao` | 2.83 | 0.0 | 0.67 | 0 | - | Repository |
| `igualdade` + `planeamento` | 2.83 | 0.0 | 0.67 | 0 | - | Repository |
| `migracao` + `planeamento` | 2.83 | 0.0 | 0.67 | 0 | - | Repository |

## Conflicting Domain Boundaries

### Cross-import hotspots (outbound)

| Module | Total cross-imports | Distinct targets | Top targets |
| --- | ---: | ---: | --- |
| `statistics` | 19 | 9 | `assistencia_social` (3), `saude` (3), `emprego` (3), `educacao` (2), `identidade_civil` (2) |
| `workflow` | 19 | 5 | `assistencia_social` (5), `educacao` (5), `emprego` (3), `juventude` (3), `saude` (3) |
| `financas_publicas` | 17 | 10 | `assistencia_social` (2), `agricultura` (2), `educacao` (2), `emprego` (2), `juventude` (2) |
| `financas` | 16 | 6 | `educacao` (4), `juventude` (4), `assistencia_social` (2), `emprego` (2), `saude` (2) |
| `service_requests` | 14 | 5 | `juventude` (5), `emprego` (3), `assistencia_social` (2), `educacao` (2), `saude` (2) |
| `identidade_civil` | 12 | 5 | `educacao` (3), `emprego` (3), `assistencia_social` (2), `juventude` (2), `saude` (2) |
| `florestas` | 5 | 5 | `agricultura` (1), `ambiente` (1), `comercio_externo` (1), `energia` (1), `gestao_fundiaria` (1) |

### Bidirectional dependencies

- No bidirectional module dependencies detected.

## Modules Sharing Entities

- No shared entity class names detected.

## Modules Sharing Repositories

| Repository/Class | Modules |
| --- | --- |
| `Repository` | `administracao_local`, `aguas_saneamento`, `apoio_empresarial`, `arquivo_nacional`, `defesa_consumidor`, `gestao_fundiaria`, `igualdade`, `migracao`, `obras_publicas`, `pescas_industriais`, `petroleo_gas`, `planeamento`, `portos_logistica`, `protecao_dados`, `recursos_minerais`, `registo_civil`, `seguranca_alimentar`, `tecnologia_inovacao`, `trabalho_inspecao` |
| `SQLAlchemyOutboxRepository` | `aguas_saneamento`, `desporto`, `energia`, `estatistica`, `obras_publicas`, `telecomunicacoes` |
| `SQLAlchemyWorkflowRepository` | `educacao`, `emprego`, `juventude` |
| `SQLAlchemyReclamacaoRepository` | `defesa_consumidor`, `emprego`, `telecomunicacoes` |
| `SQLAlchemyFormacaoRepository` | `educacao`, `emprego`, `juventude` |
| `SQLAlchemyFaturaRepository` | `aguas_saneamento`, `energia`, `telecomunicacoes` |
| `SQLAlchemyTransferenciaRepository` | `desporto`, `educacao` |
| `SQLAlchemyProprietarioRepository` | `ambiente`, `gestao_fundiaria` |
| `SQLAlchemyMediacaoRepository` | `defesa_consumidor`, `emprego` |
| `SQLAlchemyInscricaoRepository` | `educacao`, `emprego` |
| `SQLAlchemyInfraestruturaRepository` | `aguas_saneamento`, `telecomunicacoes` |
| `SQLAlchemyImovelRepository` | `ambiente`, `gestao_fundiaria` |
| `SQLAlchemyFiscalizacaoRepository` | `ambiente`, `emprego` |
| `SQLAlchemyEditalRepository` | `cultura`, `obras_publicas` |
| `SQLAlchemyDespachoRepository` | `justica`, `protecao_civil` |
| `SQLAlchemyContratoRepository` | `desporto`, `emprego` |
| `SQLAlchemyConsumoRepository` | `aguas_saneamento`, `energia` |
| `SQLAlchemyConcursoRepository` | `educacao`, `emprego` |
| `SQLAlchemyBeneficiarioRepository` | `assistencia_social`, `seguranca_social` |
| `SQLAlchemyAvaliacaoRepository` | `emprego`, `turismo` |
| `SQLAlchemyAtendimentoRepository` | `assistencia_social`, `protecao_civil` |
| `PrescriptionRepository` | `saude`, `saude_primaria` |
| `MedicalRecordRepository` | `saude`, `saude_primaria` |
| `HealthcareRepository` | `saude`, `saude_primaria` |
| `HealthUnitRepository` | `saude`, `saude_primaria` |
| `CitizenRepository` | `identidade_civil`, `identity` |
| `BaseOutboxRepository` | `aguas_saneamento`, `energia` |
| `AppointmentRepository` | `saude`, `saude_primaria` |

## Recommended Domain Groups

### governance

`administracao_local`, `arquivo_nacional`, `bi`, `cooperacao_internacional`, `identidade_civil`, `identity`, `justica`, `migracao`, `planeamento`, `protecao_dados`, `registo_civil`

### economy

`agricultura`, `apoio_empresarial`, `comercio_externo`, `comercio_servicos`, `financas`, `financas_impostos`, `financas_publicas`, `industria`, `pecuaria`, `pescas`, `pescas_industriais`, `taxpayer`, `turismo`

### social

`assistencia_social`, `ciencia_pesquisa`, `cultura`, `desporto`, `educacao`, `emprego`, `familia`, `igualdade`, `juventude`, `saude`, `saude_primaria`, `seguranca_social`, `tecnologia_inovacao`, `trabalho_inspecao`

### infrastructure

`aguas_saneamento`, `aviacao_civil`, `energia`, `gestao_fundiaria`, `obras_publicas`, `portos_logistica`, `telecomunicacoes`, `transportes_logistica`, `urbanismo_habitacao`

### environment

`ambiente`, `florestas`, `meteorologia`, `patrimonio_cultural`, `petroleo_gas`, `recursos_minerais`

### security

`defesa_consumidor`, `protecao_civil`, `seguranca_alimentar`, `seguranca_publica`

### platform

`estatistica`, `operations`, `service_requests`, `statistics`, `workflow`

## Notes

- This report is static analysis only (naming, imports, class signatures).
- Merge recommendations should be validated with business ownership and API contracts.
- Suggested next step: create a staged migration map (`domains/<group>/modules/<module>`).
