# SPRINT NACIONAL 001 – PLANO DE EXECUÇÃO OPERACIONAL

**Data:** 2026-06-08  
**Executor:** IDE 1  
**Duração:** 4 semanas (28 dias)  
**Objetivo:** 5 processos → OPERATIONAL_VALIDATED

---

## 📋 CHECKLIST POR PROCESSO (7 ITENS OBRIGATÓRIOS)

Processos Alvo:
1. NASCIMENTO_BI_NIF_SS
2. CONSTITUICAO_EMPRESA
3. MATRICULA_PAGAMENTO_CERTIFICADO
4. LICENCIAMENTO_COMERCIAL (expand)
5. BENEFICIO_SOCIAL (expand)

### ✅ Item 1: Workflow Real

**Arquivo:** `apps/backend/app/processes/{processo}/workflow_definition.json`

**Critério:** 4+ estados + 3+ transições + timeout definido

**Template (cópia de TRANSFERENCIA_ESCOLAR):**
```json
{
    "code": "NASCIMENTO_BI_NIF_SS",
    "name": "Registo de Nascimento, BI, NIF e Segurança Social",
    "entity_type": "birth_registration",
    "timeout_hours": 240,
    "states": [
        {"code": "REGISTADO", "name": "Registo Realizado", "is_initial": true},
        {"code": "CERTIDAO_EMITIDA", "name": "Certidão Emitida"},
        {"code": "NIF_ATRIBUIDO", "name": "NIF Atribuído"},
        {"code": "NUMERO_SS_ATRIBUIDO", "name": "Número SS Atribuído", "is_final": true}
    ],
    "transitions": [
        {"code": "TO_CERTIDAO", "name": "Emitir Certidão", "from": "REGISTADO", "to": "CERTIDAO_EMITIDA"},
        {"code": "TO_NIF", "name": "Atribuir NIF", "from": "CERTIDAO_EMITIDA", "to": "NIF_ATRIBUIDO"},
        {"code": "TO_SS", "name": "Atribuir SS", "from": "NIF_ATRIBUIDO", "to": "NUMERO_SS_ATRIBUIDO"}
    ]
}
```

**Validação:**
```bash
# Verificar estrutura JSON
cat apps/backend/app/processes/{processo}/workflow_definition.json | python3 -m json.tool

# Confirmar estados e transições
grep -c '"states":' apps/backend/app/processes/{processo}/workflow_definition.json
```

---

### ✅ Item 2: EventBus Real (Publishers)

**Arquivo:** `apps/backend/app/processes/{processo}/handlers/{processo}_handler.py`

**Critério:** 4+ eventos publicados em publisher + async/await

**Template:**
```python
from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.infrastructure.event_bus.event_bus import EventBus

class NascimentoHandler:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def criar_registo(self, entity_id: str, correlation_id: str, data: dict):
        # Evento 1: Registo criado
        event = DomainEvent(
            correlation_id=correlation_id,
            entity_id=entity_id,
            event_type="RegistoCriado",
            data=data
        )
        await self.event_bus.publish(event)

    async def emitir_certidao(self, entity_id: str, correlation_id: str):
        # Evento 2: Certidão emitida
        event = DomainEvent(
            correlation_id=correlation_id,
            entity_id=entity_id,
            event_type="CertidaoEmitida",
            data={"document_number": "..."}
        )
        await self.event_bus.publish(event)

    async def atribuir_nif(self, entity_id: str, correlation_id: str):
        # Evento 3: NIF atribuído
        event = DomainEvent(
            correlation_id=correlation_id,
            entity_id=entity_id,
            event_type="NIFAtribuido",
            data={"nif": "..."}
        )
        await self.event_bus.publish(event)

    async def atribuir_ss(self, entity_id: str, correlation_id: str):
        # Evento 4: SS atribuído
        event = DomainEvent(
            correlation_id=correlation_id,
            entity_id=entity_id,
            event_type="SSAtribuido",
            data={"ss_number": "..."}
        )
        await self.event_bus.publish(event)
```

**Validação:**
```bash
# Verificar publishers
grep -c "event_bus.publish" apps/backend/app/processes/{processo}/handlers/{processo}_handler.py
# Deve retornar 4 ou mais

# Verificar correlation_id
grep "correlation_id=" apps/backend/app/processes/{processo}/handlers/{processo}_handler.py | wc -l
# Deve retornar 4 ou mais (um por evento)
```

---

### ✅ Item 3: EventBus Real (Consumers)

**Arquivo:** `apps/backend/app/core/events/event_registry.py` (atualizar)

**Critério:** Mínimo 2 consumers por processo (AuditLogger + TimelineService)

**Template:**
```python
# Registar consumers para NASCIMENTO_BI_NIF_SS
event_registry.register_consumer(
    event_type="RegistoCriado",
    consumer_class=AuditLogger,
    consumer_class2=TimelineService
)

event_registry.register_consumer(
    event_type="CertidaoEmitida",
    consumer_class=AuditLogger,
    consumer_class2=TimelineService
)

event_registry.register_consumer(
    event_type="NIFAtribuido",
    consumer_class=AuditLogger,
    consumer_class2=TimelineService
)

event_registry.register_consumer(
    event_type="SSAtribuido",
    consumer_class=AuditLogger,
    consumer_class2=TimelineService
)
```

**Validação:**
```bash
# Verificar consumers registados
grep -A2 "RegistoCriado" apps/backend/app/core/events/event_registry.py
# Deve conter AuditLogger + TimelineService

# Teste de pub/sub
pytest tests/unit/test_event_bus.py::test_consumer_receives_event -v
```

---

### ✅ Item 4: EventStore Real (Persistência)

**Arquivo:** `apps/backend/app/modules/governance/service_requests/infrastructure/repositories/event_repository.py`

**Critério:** Cada evento publicado → persistido na DB

**Implementação (já existe, validar):**
```python
async def append(self, event: DomainEvent) -> None:
    """Persistir evento no EventStore."""
    model = RequestEventModel(
        request_id=event.entity_id,
        event_type=event.event_type,
        event_data=event.data,
        correlation_id=event.correlation_id,
        created_at=event.created_at
    )
    self.session.add(model)
    await self.session.commit()
```

**Validação:**
```bash
# Verificar tabela existe
psql $DATABASE_URL -c "\d audit_events"

# Contar eventos persistidos por processo
psql $DATABASE_URL -c "SELECT event_type, COUNT(*) FROM audit_events WHERE correlation_id LIKE 'nascimento%' GROUP BY event_type"

# Deve retornar 4 linhas (um por evento)
```

---

### ✅ Item 5: Correlation_id Obrigatório (100%)

**Arquivo:** Todos os handlers de cada processo

**Critério:** 100% dos eventos têm `correlation_id`

**Validação:**
```bash
# Contar eventos SEM correlation_id
psql $DATABASE_URL -c "SELECT COUNT(*) FROM audit_events WHERE correlation_id IS NULL"
# Deve retornar 0

# Contar eventos COM correlation_id por processo
psql $DATABASE_URL -c "SELECT correlation_id, COUNT(*) FROM audit_events WHERE event_type IN ('RegistoCriado', 'CertidaoEmitida', 'NIFAtribuido', 'SSAtribuido') GROUP BY correlation_id ORDER BY COUNT DESC LIMIT 10"

# Cada correlation_id deve ter 4 eventos (um por transição)
```

---

### ✅ Item 6: Timeline (Processo Completo)

**Arquivo:** `reports/process_timelines/{processo}.json`

**Critério:** Início → N eventos → Fim com duração total

**Estrutura:**
```json
{
    "process": "NASCIMENTO_BI_NIF_SS",
    "correlation_id": "nascimento-abc123",
    "entity_id": "birth-12345",
    "started_at": "2026-06-08T10:00:00Z",
    "ended_at": "2026-06-08T10:15:30Z",
    "duration_seconds": 930,
    "states": [
        {
            "state": "REGISTADO",
            "timestamp": "2026-06-08T10:00:00Z",
            "event": "RegistoCriado"
        },
        {
            "state": "CERTIDAO_EMITIDA",
            "timestamp": "2026-06-08T10:05:00Z",
            "event": "CertidaoEmitida"
        },
        {
            "state": "NIF_ATRIBUIDO",
            "timestamp": "2026-06-08T10:10:00Z",
            "event": "NIFAtribuido"
        },
        {
            "state": "NUMERO_SS_ATRIBUIDO",
            "timestamp": "2026-06-08T10:15:30Z",
            "event": "SSAtribuido"
        }
    ],
    "final_status": "SUCCESS"
}
```

**Validação:**
```bash
# Verificar timeline foi criada
cat reports/process_timelines/nascimento_bi_nif_ss.json | jq '.states | length'
# Deve retornar 4 (um por estado)

# Verificar correlation_id em timeline
cat reports/process_timelines/nascimento_bi_nif_ss.json | jq '.correlation_id'
# Deve conter valor
```

---

### ✅ Item 7: E2E (3 Cenários)

**Arquivo:** `tests/e2e/test_{processo}_e2e.py`

**Critério:** 3 testes aprovados: SUCCESS, REJECTION, CANCELLATION

**Template:**
```python
import pytest
from apps.backend.app.processes.nascimento_bi_nif_ss.handlers.nascimento_handler import NascimentoHandler

@pytest.mark.asyncio
async def test_nascimento_cenario_sucesso():
    """E2E: Caminho feliz (REGISTADO → SS)"""
    handler = NascimentoHandler(event_bus_mock)
    
    # Step 1: Criar registo
    await handler.criar_registo("birth-123", "corr-abc", {"nome": "João"})
    # Assert: Evento publicado
    assert event_bus_mock.published_count == 1
    assert event_bus_mock.last_event.event_type == "RegistoCriado"
    assert event_bus_mock.last_event.correlation_id == "corr-abc"
    
    # Step 2: Emitir certidão
    await handler.emitir_certidao("birth-123", "corr-abc")
    assert event_bus_mock.published_count == 2
    
    # Step 3: Atribuir NIF
    await handler.atribuir_nif("birth-123", "corr-abc")
    assert event_bus_mock.published_count == 3
    
    # Step 4: Atribuir SS
    await handler.atribuir_ss("birth-123", "corr-abc")
    assert event_bus_mock.published_count == 4
    
    # Validar timeline
    timeline = await timeline_service.get_timeline("corr-abc")
    assert timeline.final_status == "SUCCESS"
    assert len(timeline.states) == 4

@pytest.mark.asyncio
async def test_nascimento_cenario_rejeicao():
    """E2E: Rejeição na validação"""
    handler = NascimentoHandler(event_bus_mock)
    
    # Step 1: Criar registo com dados inválidos
    with pytest.raises(ValidationError):
        await handler.criar_registo("birth-123", "corr-abc", {"nome": ""})
    
    # Assert: Nenhum evento foi publicado
    assert event_bus_mock.published_count == 0

@pytest.mark.asyncio
async def test_nascimento_cenario_cancelamento():
    """E2E: Cancelamento após inicial"""
    handler = NascimentoHandler(event_bus_mock)
    
    # Step 1: Criar registo
    await handler.criar_registo("birth-123", "corr-abc", {"nome": "João"})
    assert event_bus_mock.published_count == 1
    
    # Step 2: Cancelar (não prosseguir)
    # (implementar cancellation logic)
    # Assert: Apenas 1 evento (RegistoCriado), processo encerra
    assert event_bus_mock.published_count == 1
```

**Validação:**
```bash
# Executar E2Es
pytest tests/e2e/test_nascimento_bi_nif_ss_e2e.py -v
# Deve retornar 3 PASSED

# Contar testes por processo
ls tests/e2e/test_*_e2e.py | wc -l
# Deve retornar 5 (um por processo)
```

---

## 📊 SAÍDA FINAL: TABELA DE STATUS

Ao término da sprint, preencher a tabela em `SPRINT_001_EXECUTION_REPORT.md`:

| Processo | Workflow | EventBus | EventStore | Correlation_id | Timeline | E2E 3x | Status |
|----------|----------|----------|-----------|-----------------|----------|--------|--------|
| NASCIMENTO_BI_NIF_SS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OPERATIONAL_VALIDATED |
| CONSTITUICAO_EMPRESA | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OPERATIONAL_VALIDATED |
| MATRICULA_PAGAMENTO_CERTIFICADO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OPERATIONAL_VALIDATED |
| LICENCIAMENTO_COMERCIAL | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OPERATIONAL_VALIDATED |
| BENEFICIO_SOCIAL | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OPERATIONAL_VALIDATED |

---

## 🚀 TIMELINE SEMANAL

### Semana 1-2: NASCIMENTO_BI_NIF_SS + CONSTITUICAO_EMPRESA

```
Dia 1-2: Setup
├─ Criar workflow_definition.json para ambos (cópia template)
├─ Criar handlers/{processo}_handler.py (4+ eventos)
└─ Criar test_{processo}_e2e.py (skeleton)

Dia 3-4: Implementação
├─ Completar handlers (async/await, correlation_id)
├─ Registar consumers (AuditLogger, TimelineService)
├─ Verificar EventStore persistência

Dia 5-6: Validação
├─ Executar E2Es (SUCCESS, REJECTION, CANCELLATION)
├─ Validar correlation_id (grep + DB)
├─ Gerar timelines

Dia 7-10: Integração
├─ make update-indexes
├─ make daily-audit
├─ Corrigir gaps
└─ Confirmar OPERATIONAL_VALIDATED
```

### Semana 3: MATRICULA_PAGAMENTO_CERTIFICADO + LICENCIAMENTO_COMERCIAL (expand)

Repetir padrão acima

### Semana 4: BENEFICIO_SOCIAL + Consolidação Final

```
Dia 1-10: BENEFICIO_SOCIAL (padrão completo)

Dia 11-14: Consolidação Global
├─ Validar todos 5 processos
├─ Executar make daily-audit (deve passar 100%)
├─ Gerar reports/
│  ├─ process_validation_report.json (5/5 OPERATIONAL_VALIDATED)
│  ├─ operational_dashboard.json (5/5 status=VALIDATED)
│  └─ process_timelines/ (5 arquivos JSON)
├─ Preencher SPRINT_001_EXECUTION_REPORT.md
└─ PR final + merge
```

---

## ✅ CRITÉRIOS DE ENCERRAMENTO SPRINT

**Condição 1: 5/5 Processos OPERATIONAL_VALIDATED**
```bash
cat reports/process_validation_report.json | jq '.[] | select(.status != "OPERATIONAL_VALIDATED") | length'
# Deve retornar 0 (zero processos não validados)
```

**Condição 2: 0 Eventos sem Consumer**
```bash
# Grep eventos orphaned
grep -r "EventType.*[A-Z]" apps/backend/app/processes/*/handlers/*.py | grep -v "AuditLogger\|TimelineService"
# Deve retornar vazio
```

**Condição 3: 0 Eventos sem Correlation_id**
```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM audit_events WHERE correlation_id IS NULL"
# Deve retornar 0
```

**Condição 4: 0 Processos sem Timeline**
```bash
ls -1 reports/process_timelines/ | wc -l
# Deve retornar 5
```

**Condição 5: 0 Processos sem E2E**
```bash
pytest tests/e2e/test_*_e2e.py -v --tb=no | grep -c "PASSED"
# Deve retornar 15 (3 por processo x 5 processos)
```

---

## 📄 RELATÓRIO FINAL: SPRINT_001_EXECUTION_REPORT.md

Estrutura obrigatória:

```markdown
# SPRINT NACIONAL 001 – RELATÓRIO FINAL DE EXECUÇÃO

**Data de Conclusão:** 2026-06-XX  
**Executor:** IDE 1  
**Status Geral:** ✅ CONCLUÍDO SUCESSO (ou ⚠️ PARCIAL / ❌ FALHADO)

## 1. PROCESSOS CONSOLIDADOS

[Tabela de status acima]

## 2. EVENTOS TOTAIS PUBLICADOS

- NASCIMENTO_BI_NIF_SS: 4 eventos (RegistoCriado, CertidaoEmitida, NIFAtribuido, SSAtribuido)
- CONSTITUICAO_EMPRESA: 4 eventos
- MATRICULA_PAGAMENTO_CERTIFICADO: 3 eventos
- LICENCIAMENTO_COMERCIAL: 3 eventos (após expand)
- BENEFICIO_SOCIAL: 3 eventos (após expand)
- **TOTAL: 17 eventos**

## 3. CONSUMERS IMPLEMENTADOS

- AuditLogger: 5 processos (todos)
- TimelineService: 5 processos (todos)
- Custom handlers: [lista por processo]
- **TOTAL: 10+ consumers**

## 4. TESTES E2E EXECUTADOS

- NASCIMENTO_BI_NIF_SS: 3/3 PASSED
- CONSTITUICAO_EMPRESA: 3/3 PASSED
- MATRICULA_PAGAMENTO_CERTIFICADO: 3/3 PASSED
- LICENCIAMENTO_COMERCIAL: 3/3 PASSED
- BENEFICIO_SOCIAL: 3/3 PASSED
- **TOTAL: 15/15 PASSED**

## 5. DASHBOARDS GERADOS

- ✅ `operational_dashboard.json` (5/5 VALIDATED)
- ✅ `process_validation_report.json` (5/5 OPERATIONAL_VALIDATED)
- ✅ `process_timelines/` (5 arquivos)

## 6. GAPS RESTANTES

[Listar se houver]

## 7. OBSERVAÇÕES E PRÓXIMAS FASES

[Análise de qualidade, recomendações, etc.]
```

---

## 🔧 COMANDOS DE VALIDAÇÃO RÁPIDA

```bash
# Validar tudo em sequência
make update-indexes && make daily-audit && pytest tests/e2e/ -v

# Contar eventos por processo
psql $DATABASE_URL -c "SELECT event_type, COUNT(*) FROM audit_events GROUP BY event_type ORDER BY COUNT DESC"

# Verificar correlation_id coverage
psql $DATABASE_URL -c "SELECT COUNT(*) as total, COUNT(DISTINCT correlation_id) as with_id FROM audit_events"

# Listar timelines geradas
ls -lh reports/process_timelines/

# Validar JSONs
for f in reports/process_timelines/*.json; do echo "=== $f ==="; cat "$f" | jq '.'; done

# Status final
cat reports/operational_dashboard.json | jq '.[] | {process, status}'
```

---

## 🎯 CONDIÇÃO FINAL

**Sprint encerrada quando:**
- [ ] 5/5 processos = OPERATIONAL_VALIDATED
- [ ] 15/15 E2Es = PASSED
- [ ] 0 eventos orphaned
- [ ] 0 eventos sem correlation_id
- [ ] 5/5 timelines geradas
- [ ] SPRINT_001_EXECUTION_REPORT.md preenchido e aprovado

**Após sucesso:** Liberar fase de expansão (Transferência Escolar, Contratação Pública, Saúde, Segurança Pública, Obras Públicas)

---

**Executar Sprint Nacional 001 com rigor. Consolidação vertical = sucesso futuro.**
