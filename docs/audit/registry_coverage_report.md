# Registry Coverage Audit — Sila Platform

## 1. RESUMO EXECUTIVO

| Indicador | Cobertura |
|---|---|
| Módulos com diretório no codebase | **85** |
| Registados no `ModuleRegistry` (bootstrap) | **3** (3.5%) |
| Com `governance.py` (integração RBAC/território) | **3** (3.5%) |
| Com `event_catalog.py` (eventos tipados) | **1** (1.2%) |
| Com API completa (health + router + endpoints) | **24** (28%) |
| Sem API nenhuma (0 endpoints) | **50** (59%) |
| Com `module.yaml` | **85** (100%) |

## 2. REGISTRY COVERAGE

### 2.1 Registados no bootstrap (`platform/governance/bootstrap.py`)

Apenas 3 módulos estão realmente registados:

| Módulo | Owner | Territorial Model | Serviços | Eventos Exposed | Eventos Consumed | Status |
|---|---|---|---|---|---|---|
| **educacao** | MINED | nacional-provincial-municipal-unidade | 21 | 3 | 3 | ✅ ACTIVE |
| **saude** | MINSA | nacional-provincial-unidade | 4 | 3 | 3 | ✅ ACTIVE |
| **justica** | MINJUSDH | nacional-provincial-unidade | 4 | 3 | 3 | ✅ ACTIVE |

### 2.2 Não registados (82 módulos sem registry entry)

| Grupo | Módulos | Impacto |
|---|---|---|
| Finanças | financas-impostos, economy.core, economy.financas, economy.taxpayer, economy.public_budget, economy.trade, economy.trade.external, economy.trade.services, economy.apoio_empresarial, economy.industria | NIF, impostos, orçamento — sem registry |
| Sociedade | seguranca-social, trabalho-inspecao, emprego, familia, juventude, igualdade, assistencia-social, cultura, desporto, patrimonio-cultural | Benefícios sociais, pensões — sem registry |
| Infraestrutura | obras-publicas, urbanismo, habitacao, transportes, telecomunicacoes, meteorologia, aviacao-civil, gestao-fundiaria, logistica, portos-logistica | Licenciamentos, obras — sem registry |
| Recursos | agricultura, pecuaria, pescas, pescas-industriais, florestas, ambiente, aguas-saneamento, recursos-minerais, petroleo-gas, seguranca-alimentar, energia | Recursos naturais — sem registry |
| Governo Local | administracao-local, cooperacao-internacional, planeamento, estatistica, protecao-civil | Admin local — sem registry |
| Identidade | identity, integracao-nacional (bi, nif, moradas, verificacao-documental), registo-civil | BI, NIF, registo civil — sem registry |
| Outros | saude, educacao, justica (já registados), payment, governance, intelligence, industry, tourism, logistics, documents, compliance, audit, procurements, notifications, energy, migration_service, operations, public_security, wallet, xroad, civil_protection, marketplace, _scaffold | Payment crítico para workflows |

## 3. EVENT COVERAGE

### 3.1 Eventos expostos (exposed_events)

| Módulo (registado) | Expõe | Consome |
|---|---|---|
| educacao | student_enrolled, student_transferred, certificate_issued | citizen_updated, identity_verified, bi_issued |
| saude | appointment_scheduled, prescription_issued, referral_made | citizen_updated, identity_verified, student_enrolled |
| justica | civil_registration_issued, company_incorporated, notarial_act_signed | citizen_updated, identity_verified, payment_confirmed |

### 3.2 Eventos declarados em module.yaml (sem registry)

| Módulo | events_published |
|---|---|
| payment | PaymentCompleted, PaymentFailed, InvoiceStatusChanged |
| registo-civil | NascimentoRegistado, ObitoRegistado, CasamentoRegistado |
| integracao-nacional/bi | BiVerificado, BiConsultado |
| integracao-nacional/nif | NifVerificado |
| integracao-nacional/verificacao-documental | DocumentoVerificado |
| educacao (module.yaml) | StudentEnrolled, TransferenciaSolicitada, CertificadoEmitido, BolsaCandidaturaSubmetida |

### 3.3 Eventos tipados em Python (event_catalog.py)

Apenas **educacao** tem eventos tipados (14 eventos):

```
seat_reserved, seat_confirmed, seat_expired, seat_cancelled,
enrollment_created, enrollment_completed,
transfer_started, transfer_completed, transfer_failed,
identity_created, identity_resolved, identity_duplicate_detected,
identity_merge_requested, identity_merged
```

**Nenhum outro módulo** tem event_catalog.py.

## 4. WORKFLOW COVERAGE

### 4.1 Cross-sector workflows (`platform/interoperability/workflows.py`)

| Workflow | Steps (módulos envolvidos) | Estado |
|---|---|---|
| constituir_empresa | justica → financas → admin-local → seg-social → payment | Definido |
| nascimento_cidadao | registo-civil → identity → saude → educacao | Definido |
| transferencia_escolar | educacao → educacao → admin-local | Definido |

Nenhum workflow adicional definido para os restantes 82 módulos.

### 4.2 Workflows internos por módulo

Nenhum módulo (exceto educacao) tem workflows internos definidos no registry.

## 5. GOVERNANCE INTEGRATION

Módulos com `governance.py` (ponte para platform/governance):

| Módulo | Roles RBAC | Território | Workflows |
|---|---|---|---|
| educacao | RoleEducacao (5 níveis) | ✅ | MatriculaWorkflow, TransferenciaWorkflow |
| saude | RoleSaude (5 níveis) | ✅ | Não definidos |
| justica | RoleJustica (5 níveis) | ✅ | Não definidos |

**79 módulos sem governance.py.**

## 6. PRIORIDADES PARA FASE 3.5 — Registry Coverage

### Críticos (bloqueiam workflows transversais)

| Prioridade | Módulo | Motivo |
|---|---|---|
| P0 | **identity** | Evento `citizen_updated` é consumido por todos. Sem registry, ninguém recebe. |
| P0 | **payment** | Workflow constituir_empresa depende de `pagamento_taxas`. |
| P0 | **registo-civil** | Workflow nascimento_cidadao começa aqui. |
| P0 | **financas-impostos** | Workflow constituir_empresa precisa de `emitir_nif`. |
| P1 | **administracao-local** | Workflows constituir_empresa + transferencia_escolar dependem. |
| P1 | **seguranca-social** | Workflow constituir_empresa precisa de `registo_empregador`. |

### Segundo escalão (eventos importantes)

| Prioridade | Módulo | Motivo |
|---|---|---|
| P1 | **integracao-nacional/bi** | Emite `bi_issued` — consumido por educacao. |
| P1 | **integracao-nacional/nif** | Emite `nif_verified`. |
| P2 | **saude** | Já registado, mas sem governance.py e event_catalog.py. |
| P2 | **justica** | Já registado, mas sem event_catalog.py. |
| P2 | **economy.taxpayer** | Consumiria eventos de identity. |
| P2 | **society.assistencia_social** | Benefícios sociais transversais. |

## 7. MÉTRICAS DE MATURIDADE (NOVO MODELO)

Substituir o modelo anterior (models/services/router/health) por:

```
registry_coverage: 3/85  (3.5%)
event_exposed_coverage: 3/85 (3.5%)
event_consumed_coverage: 3/85 (3.5%)
workflow_coverage: 3 workflows / 85 módulos
governance_integration: 3/85 (3.5%)
```

## 8. ACÇÃO RECOMENDADA

1. **Registar todos os módulos no bootstrap** com owner_ministry e territorial_model
2. **Criar event_catalog.py para identity, payment, registo-civil, financas-impostos**
3. **Completar governance.py para os 4 módulos P0**
4. **Alinhar module.yaml com os eventos reais do event_catalog.py**
5. **Expandir workflows cross-sector para incluir licenciamento comercial, benefícios sociais, passaporte**
