# PLANO FINAL — PASSO 13 & 14

**Data:** 2026-05-26  
**Status:** PLANEJAMENTO → EXECUÇÃO  
**Escopo:** Automação Real com RabbitMQ + Dead Letter Queue  

---

## 📊 STATUS ATUAL

### ✅ Implementado (PASSO 13)
- `foundation/automation/message_bus.py` — RabbitMQAutomationBus com auto-detecção
- `foundation/automation/automator.py` — AutomationEngine com 4 eventos
- `docker-compose.minimal.yml` — Stack com DB/RabbitMQ/Redis/Backend/Automation
- `apps/backend/start_automation_worker.py` — Worker consumer
- Dependências: `kombu==5.6.2` em requirements/prod.txt

### ⚠️ Gaps (PASSO 14)
- **start_dlq_worker.py** — Não existe, precisa ser criado
- **DLQ Handler** — Documentado mas não completamente integrado
- **DLQ Exchange/Queue** — Configuração de DLX em RabbitMQAutomationBus incompleta
- **DLQ Service** — Falta adicionar serviço no docker-compose.minimal.yml
- **.env DLQ** — Variáveis de ambiente para configuração DLQ
- **Testes** — Testes unitários e E2E não existem

### 🔍 Dependências Validadas
```
kombu==5.6.2       ✅ (message broker)
amqp==5.3.1        ✅ (protocol)
asyncpg==0.31.0    ✅ (postgres async)
redis==7.3.0       ✅ (cache/result backend)
```

---

## 🎯 IMPLEMENTAÇÃO EM 4 FASES

### FASE 1: Completar RabbitMQ DLX Configuration
**Tempo estimado:** 30 min

#### Tarefa 1.1: Atualizar `foundation/automation/message_bus.py`
- Adicionar classe `DLQMixin` para reutilizar lógica de DLX
- Configurar `x-dead-letter-exchange` em cada queue
- Implementar `_create_dlq_exchange()` e `_create_dlq_queue()`
- Max retries configurável via env var

**Arquivo:** `/home/dev03wsl/sila-system/foundation/automation/message_bus.py`

Mudanças:
1. Adicionar suporte a DLX automático no `__init__`
2. Criar métodos `_setup_dlx()` para cada queue
3. Logging estruturado com context vars

---

### FASE 2: Implementar DLQ Worker
**Tempo estimado:** 45 min

#### Tarefa 2.1: Criar `apps/backend/start_dlq_worker.py`
- Classe `DLQConsumer` que herda de `ConsumerMixin`
- Consome de `sila_dlq_main`
- Logging crítico de falhas
- Estrutura para alertas (Slack, PagerDuty)
- Graceful shutdown

**Arquivo:** `/home/dev03wsl/sila-system/apps/backend/start_dlq_worker.py`

Estrutura:
```python
class DLQConsumer:
    def __init__(self, broker_url, alert_handler=None)
    def on_message(self, payload: dict) -> None
    def log_dlq_event(self, payload: dict) -> None
    def send_alert(self, payload: dict) -> None

def main() -> None:
    consumer = DLQConsumer(
        broker_url=RABBITMQ_URL,
        alert_handler=AlertService()
    )
    consumer.run()
```

---

### FASE 3: Atualizar Infraestrutura
**Tempo estimado:** 30 min

#### Tarefa 3.1: Validar/Completar `docker-compose.minimal.yml`
- Adicionar serviço `dlq-worker`
- Configurar healthcheck
- Variáveis de ambiente: `DLQ_MAX_RETRIES`, `ALERT_WEBHOOK_URL`

#### Tarefa 3.2: Atualizar `apps/backend/.env`
- Adicionar: `RABBITMQ_URL=amqp://guest:guest@localhost:5672/`
- Adicionar: `DLQ_MAX_RETRIES=3`
- Adicionar: `DLQ_ENABLED=true`
- Adicionar: `ALERT_WEBHOOK_URL=` (opcional para Slack)

---

### FASE 4: Testes & Validação
**Tempo estimado:** 60 min

#### Tarefa 4.1: Testes Unitários
- Test: `message_bus.py` — DLX creation, consumer lifecycle
- Test: `automator.py` — Event publishing with DLQ routing
- Test: `start_dlq_worker.py` — Message handling, alert triggering

#### Tarefa 4.2: Testes de Integração (E2E)
1. Start stack: `docker compose -f docker-compose.minimal.yml up -d`
2. Trigger transfer: POST `/api/v1/transfers`
3. Monitorar RabbitMQ UI: `http://localhost:15672`
4. Verificar DLQ messages quando falhas ocorrem
5. Validar logs no worker DLQ

#### Tarefa 4.3: Smoke Tests
- 5 transferências bem-sucedidas
- 5 transferências com falha (simuladas)
- Verificar 0 mensagens em DLQ ao fim dos testes bem-sucedidos
- Verificar N mensagens em DLQ ao fim dos testes com falha

---

## 🔧 DETALHES TÉCNICOS

### Arquitetura de Mensagens

```
┌─────────────┐
│   Backend   │
│ request_    │
│ transfer()  │
└──────┬──────┘
       │
       ▼
   transfer_requested
       │
       ├─ Topic Exchange: sila.automation
       ├─ Routing Key: transfer_requested
       └─ Queue: sila_transfer_requested
               │
               ├─ Consumer: automation-worker
               │
               ▼
           _on_transfer_requested()
               │
               ▼
           transfer_validated (publish)
               │
               └─ Queue: sila_transfer_validated
                   │
                   ▼
               _on_transfer_validated()
                   │
                   ▼
           execute_transfer()
               │
           ┌───┴────────┐
           │            │
        SUCCESS      FAILURE
           │            │
           ▼            ▼
    transfer_      transfer_
    completed      failed
           │            │
           └──┬─────────┘
              │
         Check retries
              │
         ┌────┴────┐
    Retries    Retries
      < 3         >= 3
         │            │
        REQUEUE    REJECT
         │            │
         └──┬──────────┘
            │
            ▼
    Dead Letter Queue
    (sila_dlq_main)
            │
            ▼
        dlq-worker
        (Consumer)
            │
      ┌─────┴────────┐
      │              │
    LOG           ALERT
      │              │
    Slack/      PagerDuty/
   PagerDuty    Slack
```

### Configuração RabbitMQ

```yaml
Exchanges:
  - sila.automation (topic, durable)
  - sila.automation.dlx (topic, durable) [DLX]

Queues (Principais):
  - sila_transfer_requested
    - x-dead-letter-exchange: sila.automation.dlx
    - x-dead-letter-routing-key: dlq.transfer_requested
  - sila_transfer_validated
    - x-dead-letter-exchange: sila.automation.dlx
    - x-dead-letter-routing-key: dlq.transfer_validated
  - sila_transfer_completed
    - x-dead-letter-exchange: sila.automation.dlx
    - x-dead-letter-routing-key: dlq.transfer_completed
  - sila_transfer_failed
    - x-dead-letter-exchange: sila.automation.dlx
    - x-dead-letter-routing-key: dlq.transfer_failed

Queues (DLQ):
  - sila_dlq_main
    - Exchange: sila.automation.dlx
    - Routing Keys: dlq.* (all dead letters)
```

---

## 📋 CHECKLIST EXECUTIVO

### FASE 1 — RabbitMQ DLX
- [ ] Completar `RabbitMQAutomationBus.__init__()` com DLX setup
- [ ] Implementar `_create_dlx_exchanges()`
- [ ] Implementar `_create_dlq_queue()`
- [ ] Adicionar logging estruturado com student_id context
- [ ] Validar syntax Python

### FASE 2 — DLQ Worker
- [ ] Criar `start_dlq_worker.py` com `DLQConsumer`
- [ ] Implementar `on_message()` handler com logging
- [ ] Implementar `send_alert()` framework
- [ ] Adicionar graceful shutdown
- [ ] Validar syntax Python

### FASE 3 — Infraestrutura
- [ ] Adicionar serviço `dlq-worker` em docker-compose.minimal.yml
- [ ] Adicionar variáveis de ambiente no `.env`
- [ ] Validar docker-compose syntax
- [ ] Testar `docker compose config`

### FASE 4 — Testes
- [ ] Criar `tests/test_message_bus_dlq.py`
- [ ] Criar `tests/test_dlq_worker.py`
- [ ] Criar `tests/test_automation_e2e.py`
- [ ] Executar: `pytest tests/test_*.py -v`
- [ ] Testes E2E com docker-compose
- [ ] Validação compliance com `make clean-audit`

---

## 🚀 EXECUÇÃO PASSO-A-PASSO

```bash
# 1. Verificar status
cd /home/dev03wsl/sila-system
git status
make clean-audit

# 2. FASE 1: Completar RabbitMQ DLX
# (Editar foundation/automation/message_bus.py)

# 3. FASE 2: Implementar DLQ Worker
# (Criar apps/backend/start_dlq_worker.py)

# 4. FASE 3: Atualizar docker-compose
# (Editar docker-compose.minimal.yml e .env)

# 5. Validar configuração
docker compose -f docker-compose.minimal.yml config
docker compose -f docker-compose.minimal.yml up -d --build

# 6. FASE 4: Executar testes
pytest tests/ -v --tb=short

# 7. Validação compliance
make daily-audit
cat reports/daily_audit.md

# 8. Cleanup
docker compose -f docker-compose.minimal.yml down
```

---

## 📝 PRÓXIMOS PASSOS

1. **Confirmação de GO/NO-GO** — Validar plano com equipe
2. **Implementação** — Executar 4 fases em paralelo se possível
3. **Code Review** — Revisar ANTES de merge
4. **Deployment** — Staging → Produção
5. **Monitoramento** — Alertas e métricas
6. **Documentação Operacional** — Runbooks para on-call

---

## 🔐 SEGURANÇA

- [ ] Não committar senhas em repo — usar `.env` apenas
- [ ] Validar credenciais RabbitMQ em produção
- [ ] Implementar TLS para conexão RabbitMQ (produção)
- [ ] Audit trail completo de DLQ processamento
- [ ] Permissões RBAC no PostgreSQL para logs DLQ

---

## 📞 CONTATO

**Responsável:** TrumanAgent  
**Workspace:** `/home/dev03wsl/sila-system`  
**Critério de Sucesso:** 4/4 fases completadas + testes verdes + compliance OK

