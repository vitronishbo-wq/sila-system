# SILA – SPRINT NACIONAL 001: CONSOLIDAÇÃO OPERACIONAL
**Data:** 2026-06-08  
**Executor:** IDE 1 (National Process Factory)  
**Estratégia:** Consolidação Vertical (Operational Validated) antes de Expansão Horizontal

---

> **PIVÔ ESTRATÉGICO:** Não criar novos processos. Consolidar os 5 prioritários existentes até OPERATIONAL_VALIDATED.

---

## 1. PROCESSOS OPERACIONAIS

Processos já mapeados com workflow_definition.json e handlers implementados:

| Processo | Workflow | Eventos Publicados | Eventos Consumidos | E2E | Status Operacional |
|----------|----------|-------------------|-------------------|-----|-------------------|
| **TRANSFERENCIA_ESCOLAR** | `TRANSFERENCIA_ESCOLAR` | 4+ | Sim (AuditLogger) | ✓ | **OPERACIONAL** |
| **APOSENTACAO** | `APOSENTACAO` | 3+ | Parcial | ⟳ | **PARCIAL** |
| **BENEFICIO_SOCIAL** | `BENEFICIO_SOCIAL` | 3+ | Parcial | ⟳ | **PARCIAL** |
| **LICENCIAMENTO_COMERCIAL** | `LICENCIAMENTO_COMERCIAL` | 3+ | Parcial | ⟳ | **PARCIAL** |
| **CONTRATACAO_PUBLICA** | `CONTRATACAO_PUBLICA` | 3+ | Parcial | ⟳ | **PARCIAL** |

### Detalhes de Eventos:

#### TRANSFERENCIA_ESCOLAR ✓
- **Estados:** PEDIDO → VALIDACAO_ORIGEM → VALIDACAO_DESTINO → MATRICULA_TRANSFERIDA
- **Eventos Publicados:** StudentTransferRequested, TransferValidatedByOrigin, TransferValidatedByDestination, TransferCompleted
- **Consumidores:** AuditLogger, WorkflowTimeline
- **Timeline:** Sim (com correlation_id)
- **Timeout:** 72h
- **Validação:** 3 E2Es (workflow completo, cancelamento, validação de actor)

#### APOSENTACAO
- **Estados:** PEDIDO_APOSENTACAO → TEMPO_SERVICO_VALIDADO → BENEFICIO_CALCULADO → APOSENTACAO_CONCEDIDA
- **Eventos:** RetirementRequested, ServiceTimeValidated, BenefitCalculated, RetirementGranted
- **Timeline:** Parcial (sem timeline confirmada)
- **Timeout:** 168h
- **E2E:** Não encontrada

#### BENEFICIO_SOCIAL
- **Estados:** PEDIDO → VERIFICACAO_NIF → VERIFICACAO_SS → APROVADO
- **Eventos:** BenefitRequested, NIFVerified, SSVerified, BenefitApproved
- **Timeline:** Parcial
- **Timeout:** 72h
- **E2E:** Sim (test_endpoint_listar_beneficios_retorna_lista)

#### LICENCIAMENTO_COMERCIAL
- **Estados:** SUBMETIDO → VALIDACAO_FISCAL → VALIDACAO_LOCAL → LICENCA_EMITIDA
- **Eventos:** LicenseRequested, FiscalValidated, LocalValidated, LicenseIssued
- **Timeline:** Parcial
- **Timeout:** 72h
- **E2E:** Sim (test_licenciamento_service_fluxo_requerer_deferir)

#### CONTRATACAO_PUBLICA
- **Estados:** PUBLICADO → PROPOSTA_SUBMETIDA → AVALIACAO_CONCLUIDA → ADJUDICACAO_EMITIDA
- **Eventos:** ProcurementPublished, ProposalSubmitted, EvaluationCompleted, AdjudicationIssued
- **Timeline:** Parcial
- **Timeout:** 168h
- **E2E:** Não confirmada

---

## 2. PROCESSOS OPERACIONAIS INCOMPLETOS

Processos com estrutura de diretório mas **SEM workflow definido:**

| Processo | Status | Arquivo | Ação Necessária |
|----------|--------|---------|-----------------|
| NASCIMENTO_BI_NIF_SS | 🔴 Vazio | `apps/backend/app/processes/nascimento_bi_nif_ss/` | Criar workflow_definition.json + handlers |
| CONSTITUICAO_EMPRESA | 🔴 Vazio | `apps/backend/app/processes/constituicao_empresa/` | Criar workflow_definition.json + handlers |
| MATRICULA_PAGAMENTO_CERTIFICADO | 🔴 Vazio | `apps/backend/app/processes/matricula_pagamento_certificado/` | Criar workflow_definition.json + handlers |
| CONTRACTS | 🟡 Mínimo | `apps/backend/app/processes/contracts/` | Expandir handlers + workflow |

---

## 3. PROCESSOS ALVO DA SPRINT NACIONAL 001

Consolidação operacional de **5 processos prioritários** que já existem mas estão incompletos:

| Processo | Situação | Objetivo Sprint |
|----------|----------|-----------------|
| 🔴 **NASCIMENTO_BI_NIF_SS** | Vazio | OPERATIONAL_VALIDATED |
| 🔴 **CONSTITUICAO_EMPRESA** | Vazio | OPERATIONAL_VALIDATED |
| 🔴 **MATRICULA_PAGAMENTO_CERTIFICADO** | Vazio | OPERATIONAL_VALIDATED |
| 🟡 **LICENCIAMENTO_COMERCIAL** | Parcial | OPERATIONAL_VALIDATED |
| 🟡 **BENEFICIO_SOCIAL** | Parcial | OPERATIONAL_VALIDATED |

### O Que NÃO Fazer Nesta Sprint

❌ Criar novos processos  
❌ Alterar frontend, portais, React  
❌ Modificar OrganizationTree, RBAC, dashboards  
❌ Expandir observabilidade ou auditorias  

**Escopo exclusivo:** `apps/backend/app/processes/` e seus handlers

---

## 4. OBJETIVO DA SPRINT

```
ANTES (Status Atual - 2026-06-08):
├─ Processos com workflow_definition.json: 5
├─ Processos OPERATIONAL_VALIDATED: 0
├─ Timeline completa: 0
├─ Correlation_id obrigatório: 0
├─ E2E aprovado: 1 (Transferência Escolar)
└─ Coverage: 10%

DEPOIS (Alvo Sprint Nacional 001):
├─ Processos OPERATIONAL_VALIDATED: 5
├─ Timeline completa: 5/5 (100%)
├─ Correlation_id obrigatório: 5/5 (100%)
├─ E2E aprovado: 5/5 (100%)
├─ EventStore persistência: 5/5
├─ EventBus publishers: 5/5
├─ EventBus consumers reais: 5/5
└─ Coverage: 100%
```

**Critério de Sucesso:**
- Cada processo aparece em `process_validation_report.json` como **OPERATIONAL_VALIDATED**
- Cada processo aparece em `operational_dashboard.json` como **VALIDATED**
- Nenhum gap tecnológico remanescente

---

## 5. ENTREGA OBRIGATÓRIA POR PROCESSO

Cada um dos 5 processos alvo deve cumprir **todos** os 14 itens abaixo para ser considerado **OPERATIONAL_VALIDATED**:

### CHECKLIST TÉCNICO POR PROCESSO

#### 1️⃣ NASCIMENTO_BI_NIF_SS
- [ ] `workflow_definition.json` criado (4+ estados)
- [ ] `handlers/nascimento_handler.py` implementado
- [ ] Tests locais passam (`pytest tests/modules/registos/`)
- [ ] EventBus publishers (RegistrationRequested, CertificateIssued, NIFAssigned, SSNumberAssigned)
- [ ] EventBus consumers (AuditLogger, TimelineService)
- [ ] EventStore persistência (evento → DB)
- [ ] Correlation_id em cada evento
- [ ] Timeline início-meio-fim (4 transições)
- [ ] E2E sucesso (registro → certificado → NIF → SS)
- [ ] E2E rejeição (registro invalido)
- [ ] E2E cancelamento (após início)
- [ ] Validação: `make daily-audit` passa
- [ ] Documentação em `docs/modules/nascimento/`
- [ ] Aparece em `process_validation_report.json` como OPERATIONAL_VALIDATED

#### 2️⃣ CONSTITUICAO_EMPRESA
- [ ] `workflow_definition.json` criado (4+ estados)
- [ ] `handlers/constituicao_handler.py` implementado
- [ ] Tests locais passam (`pytest tests/modules/negocio/`)
- [ ] EventBus publishers (CompanyRegistrationRequested, CompanyValidated, CompanyApproved, CompanyRegistered)
- [ ] EventBus consumers
- [ ] EventStore persistência
- [ ] Correlation_id obrigatório
- [ ] Timeline 4+ etapas
- [ ] E2E sucesso
- [ ] E2E rejeição
- [ ] E2E cancelamento
- [ ] `make daily-audit` passa
- [ ] Documentação
- [ ] `process_validation_report.json` ✓

#### 3️⃣ MATRICULA_PAGAMENTO_CERTIFICADO
- [ ] `workflow_definition.json` criado
- [ ] `handlers/matricula_handler.py` implementado
- [ ] Tests locais passam
- [ ] EventBus publishers (EnrollmentRequested, PaymentProcessed, CertificateIssued)
- [ ] EventBus consumers
- [ ] EventStore persistência
- [ ] Correlation_id obrigatório
- [ ] Timeline 4+ etapas
- [ ] E2E sucesso
- [ ] E2E rejeição
- [ ] E2E cancelamento
- [ ] `make daily-audit` passa
- [ ] Documentação
- [ ] `process_validation_report.json` ✓

#### 4️⃣ LICENCIAMENTO_COMERCIAL (Completo)
- [ ] Expand workflow_definition.json (adicionar transitions em falta)
- [ ] Consolidar `handlers/licenciamento_handler.py`
- [ ] Adicionar timeline (atualmente parcial)
- [ ] Adicionar correlation_id em todos os eventos
- [ ] E2E sucesso (completo até LICENCA_EMITIDA)
- [ ] E2E rejeição (fiscal)
- [ ] E2E cancelamento (após validacao_fiscal)
- [ ] Tests coverage 100%
- [ ] EventStore: todos os eventos persistidos
- [ ] EventBus: consumers confirmados
- [ ] `make daily-audit` passa
- [ ] Documentação completa
- [ ] `process_validation_report.json` ✓

#### 5️⃣ BENEFICIO_SOCIAL (Completo)
- [ ] Expand workflow_definition.json
- [ ] Consolidar `handlers/beneficio_handler.py`
- [ ] Timeline (atualmente parcial)
- [ ] Correlation_id em todos os eventos
- [ ] E2E sucesso (PEDIDO → APROVADO)
- [ ] E2E rejeição (verificacao_nif falha)
- [ ] E2E cancelamento (após PEDIDO)
- [ ] Tests coverage 100%
- [ ] EventStore persistência
- [ ] EventBus consumers reais
- [ ] `make daily-audit` passa
- [ ] Documentação
- [ ] `process_validation_report.json` ✓

---

## 6. PLANO DE EXECUÇÃO – SPRINT NACIONAL 001

**Duração:** 4 semanas (Sprint de 2 semanas x 2 iterações)

### Semana 1-2: NASCIMENTO_BI_NIF_SS + CONSTITUICAO_EMPRESA
```
Dia 1-2:
├─ Criar workflow_definition.json (template: TRANSFERENCIA_ESCOLAR)
├─ Implementar handlers.py
└─ Setup local tests

Dia 3-5:
├─ Implementar EventBus publishers
├─ Implementar EventBus consumers
├─ EventStore integration
├─ Correlation_id em eventos

Dia 6-10:
├─ Implementar 3 E2Es por processo
├─ Tests coverage 100%
├─ Timeline início-fim
├─ make daily-audit passar
├─ Documentar em docs/modules/
└─ Commit + PR

Dia 11-14:
├─ Code review + fixes
├─ Validação em process_validation_report.json
└─ Processos → OPERATIONAL_VALIDATED
```

### Semana 3: MATRICULA_PAGAMENTO_CERTIFICADO + expand LICENCIAMENTO_COMERCIAL
```
Semana inteira: Repetir padrão acima
├─ MATRICULA (novo): dias 1-10
└─ LICENCIAMENTO (expand): dias 4-14
```

### Semana 4: BENEFICIO_SOCIAL + Consolidação Final
```
Dia 1-10:
├─ BENEFICIO_SOCIAL (novo): aplicar padrão completo
└─ Timeline + E2E + EventStore

Dia 11-14:
├─ Validação global de todos 5 processos
├─ Gerar process_validation_report.json
├─ Gerar operational_dashboard.json
├─ Executar make daily-audit
└─ PR final + merge
```

---

## 7. RECOMENDAÇÕES EXECUTIVAS

### 🎯 AÇÕES IMEDIATAS

#### 1. **Usar TRANSFERENCIA_ESCOLAR como Template Universal**
O único processo completo e validado. Cada novo processo copia:
```
TRANSFERENCIA_ESCOLAR/
├── workflow_definition.json    ← TEMPLATE (4 estados + 3 transições)
├── handlers.py                 ← PADRÃO (AuditLogger + TimelineService)
└── tests/e2e/test_*_e2e.py    ← PADRÃO (3 E2Es: sucesso, rejeição, cancelamento)
```

**Aplicar ao:** NASCIMENTO, CONSTITUICAO, MATRICULA, LICENCIAMENTO (expand), BENEFICIO (expand)

#### 2. **Correlation_id Obrigatório em Cada Evento**
Padrão implementado:
```python
# Sempre que publicar evento:
event = DomainEvent(
    correlation_id=request.correlation_id,  # ← OBRIGATÓRIO
    entity_id=entity_id,
    event_type="EntityCreated",
    data={...}
)
await event_bus.publish(event)
await event_store.append(event)
```

**Verificar:** `apps/backend/app/core/events/domain_event.py`

#### 3. **Timeline: Início, Meio, Fim**
Padrão implementado em TRANSFERENCIA:
```python
# Início
timeline.create(
    correlation_id=event.correlation_id,
    process_type="NASCIMENTO_BI_NIF_SS",
    entity_id=entity_id,
    status="REGISTADO"
)

# Meio (cada transição)
timeline.add_event(
    correlation_id=event.correlation_id,
    status="CERTIDAO_EMITIDA",
    timestamp=now()
)

# Fim
timeline.close(
    correlation_id=event.correlation_id,
    status="NUMERO_SS_ATRIBUIDO",
    result="SUCCESS"
)
```

**Consultar:** `apps/backend/app/modules/governance/service_requests/application/services/timeline_service.py`

#### 4. **EventStore: Persistência Obrigatória**
Cada evento publicado **DEVE** ser persistido:
```python
await event_store.append(event)  # Após cada publish
```

**Verificar:** `apps/backend/app/modules/governance/service_requests/infrastructure/repositories/event_repository.py`

#### 5. **EventBus: Publishers + Consumers Validados**
Cada processo precisa de:
- ✅ **Publisher:** Evento publicado quando algo acontece
- ✅ **Consumer:** Pelo menos um subscriber que reage ao evento

**Padrão:** Se evento não tem consumer, adicionar AuditLogger como fallback

#### 6. **E2Es: 3 Cenários Obrigatórios por Processo**

```
test_nascimento_e2e.py
├── test_nascimento_sucesso()          # Happy path (REGISTADO → SS)
├── test_nascimento_rejeicao()         # Rejeição em CERTIDAO
└── test_nascimento_cancelamento()     # Cancelamento após REGISTADO
```

**Padrão:** Copiar de `tests/e2e/test_02_transferencia_e2e.py`

#### 7. **Validação: process_validation_report.json**
Ao terminar cada processo:
```bash
make daily-audit
```

Verificar saída em `reports/process_validation_report.json`:
```json
{
  "process": "NASCIMENTO_BI_NIF_SS",
  "status": "OPERATIONAL_VALIDATED",
  "timeline_coverage": 100,
  "correlation_id_coverage": 100,
  "e2e_count": 3,
  "event_store_count": 4,
  "last_updated": "2026-06-15"
}
```

### 🔄 WORKFLOW DA SPRINT

1. **Checkout nova branch:** `feature/sprint-nacional-001-consolidacao`
2. **Implementar 5 processos** (em paralelo ou sequencial)
3. **Cada processo:** Checklist 14 itens
4. **Validação:** `make daily-audit` passa
5. **PR com entrega:** `OPERATIONAL_VALIDATED` confirmado
6. **Merge:** Quando todos 5 forem validados

### 📋 DOCUMENTAÇÃO POR PROCESSO

Criar `docs/modules/{processo}/` com:
- `workflow_definition.md` (descrição dos estados)
- `events.md` (lista de eventos publicados)
- `handlers.md` (lista de consumers)
- `timeline.md` (diagrama da timeline)
- `e2e.md` (cenários de teste)

---

## 8. ENTREGA FINAL DA SPRINT NACIONAL 001

Ao término das 4 semanas, a IDE 1 entregará um relatório contendo:

### 📊 Relatório de Consolidação (process_consolidation_report_sprint_001.md)

```markdown
# SPRINT NACIONAL 001 – RELATÓRIO FINAL
Data: 2026-06-29

## 1. PROCESSOS CONSOLIDADOS

| Processo | Status | Timeline | Correlation_id | E2E | EventStore | EventBus |
|----------|--------|----------|-----------------|-----|-----------|----------|
| NASCIMENTO_BI_NIF_SS | ✓ VALIDATED | ✓ | ✓ | 3/3 | ✓ | ✓ |
| CONSTITUICAO_EMPRESA | ✓ VALIDATED | ✓ | ✓ | 3/3 | ✓ | ✓ |
| MATRICULA_PAGAMENTO_CERTIFICADO | ✓ VALIDATED | ✓ | ✓ | 3/3 | ✓ | ✓ |
| LICENCIAMENTO_COMERCIAL | ✓ VALIDATED | ✓ | ✓ | 3/3 | ✓ | ✓ |
| BENEFICIO_SOCIAL | ✓ VALIDATED | ✓ | ✓ | 3/3 | ✓ | ✓ |

## 2. MÉTRICAS DE SUCESSO

- [x] 5/5 processos OPERATIONAL_VALIDATED
- [x] 100% timeline coverage
- [x] 100% correlation_id obrigatório
- [x] 100% E2E approved (15 testes totais)
- [x] 100% EventStore persistência
- [x] 100% EventBus pub/sub validado
- [x] 0 gaps tecnológicos

## 3. EVENTOS PUBLICADOS TOTAIS

- NASCIMENTO: 4 eventos
- CONSTITUICAO: 4 eventos
- MATRICULA: 3 eventos
- LICENCIAMENTO: 3 eventos
- BENEFICIO: 3 eventos
- **TOTAL: 17 eventos**

## 4. CONSUMERS IMPLEMENTADOS

- AuditLogger: 5 (todos os processos)
- TimelineService: 5 (todos os processos)
- Custom handlers: [lista específica por processo]

## 5. GAPS RESTANTES

[A preencher pela IDE 1 se houver algum]

## 6. PRÓXIMOS 5 PROCESSOS RECOMENDADOS

[Proposição baseada em impacto, apenas após aprovação do relatório]
```

### ✅ Critérios de Aceitação Finais

Antes de considerar a sprint concluída:
- [ ] PR aberto com todos 5 processos
- [ ] `make daily-audit` passa 100%
- [ ] `operational_dashboard.json` mostra 5/5 VALIDATED
- [ ] `process_validation_report.json` confirma 5/5 OPERATIONAL_VALIDATED
- [ ] Documentação em `docs/modules/` para cada processo
- [ ] Teste de stress (100 requisições simultâneas por processo)
- [ ] Correlação visual em `reports/module_architecture_docs_visual_report.md`
- [ ] Relatório final aprovado

---

## 9. REFERÊNCIA RÁPIDA

**Começar um novo processo:**
```bash
# 1. Copiar template
cp -r apps/backend/app/modules/educacao/workflows/transferencia_workflow.py \
      apps/backend/app/processes/{NOVO_PROCESSO}/workflow.py

# 2. Copiar E2E template
cp tests/e2e/test_02_transferencia_e2e.py \
   tests/e2e/test_{novo_processo}_e2e.py

# 3. Criar handlers
mkdir -p apps/backend/app/processes/{NOVO_PROCESSO}/handlers
touch apps/backend/app/processes/{NOVO_PROCESSO}/handlers/{novo_processo}_handler.py

# 4. Validar
make update-indexes
make daily-audit

# 5. Testar
pytest tests/e2e/test_{novo_processo}_e2e.py -v
```

**Validar cobertura:**
```bash
# Ver todos os processos e status
cat reports/process_validation_report.json | jq '.[] | {process, status, timeline_coverage, e2e_count}'

# Ver se correlation_id obrigatório
grep -r "correlation_id" apps/backend/app/core/events/

# Verificar EventStore
grep -r "event_store.append" apps/backend/app/processes/
```

---

**Status Final:** 🎯 **SPRINT NACIONAL 001 – CONSOLIDAÇÃO VERTICAL ANTES DE EXPANSÃO HORIZONTAL**

Próximo passo: Executar a sprint. Após sucesso, será liberada a fase de Expansão (Saúde, Segurança Pública, Obras Públicas, etc.).
