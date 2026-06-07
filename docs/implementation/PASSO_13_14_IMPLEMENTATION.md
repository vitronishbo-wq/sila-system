# PASSO 13 & 14 — Automação Real com DLQ

## 📋 Resumo Executivo

Implementação completa de **automação em tempo real** com suporte a **Dead Letter Queue (DLQ)** para o SILA System.

### ✅ Status: IMPLEMENTADO E PRONTO PARA PRODUÇÃO

| Componente | Status | Arquivo |
|-----------|--------|---------|
| RabbitMQ Bus com DLQ | ✅ | `foundation/automation/message_bus.py` |
| Automation Engine | ✅ | `foundation/automation/automator.py` |
| DLQ Worker | ✅ | `apps/backend/start_dlq_worker.py` |
| Docker Compose | ✅ | `docker-compose.minimal.yml` |
| Documentação | ✅ | `docs/PASSO_13_AUTOMACAO_REAL.md`, `docs/PASSO_14_DLQ_REAL.md` |
| Dependências | ✅ | `requirements/dev.txt`, `requirements/prod.txt` |

## 🎯 O Que Foi Implementado

### PASSO 13: Automação Real com RabbitMQ

**Antes:**
- Enfileiramento local (em memória)
- Sem suporte a broker real
- Sem persistência entre restarts

**Depois:**
- ✅ RabbitMQ real como broker de mensagens
- ✅ 4 eventos de transferência totalmente implementados
- ✅ Retry automático com max_retries configurável
- ✅ Topic exchange com routing patterns
- ✅ Auto-detecção de `RABBITMQ_URL`

### PASSO 14: Dead Letter Queue Real

**Antes:**
- Ficheiro local para armazenar erros
- Sem tratamento automático de falhas
- Sem alertas

**Depois:**
- ✅ Dead Letter Exchange (DLX) automático
- ✅ Dead Letter Queue (DLQ) com durabilidade
- ✅ Worker dedicado para consumir DLQ
- ✅ Logging estruturado de falhas críticas
- ✅ Framework para alertas (Slack, PagerDuty, etc.)
- ✅ Rastreamento completo via auditoria

## 🚀 Iniciar Localmente

### Pré-requisitos
- Docker e Docker Compose
- Python 3.10+
- PostgreSQL (na stack)
- RabbitMQ (na stack)

### Executar Stack Completo

```bash
cd /home/dev03wsl/sila-system

# 1. Iniciar todos os serviços
docker compose -f docker-compose.minimal.yml up -d --build

# 2. Verificar status
docker compose -f docker-compose.minimal.yml ps

# 3. Acompanhar logs em tempo real
docker compose -f docker-compose.minimal.yml logs -f

# 4. Parar
docker compose -f docker-compose.minimal.yml down
```

### Acessar RabbitMQ Management UI

```
URL: http://localhost:15672
Username: guest
Password: guest
```

**O que observar:**
- Exchanges: `sila.automation` (topic), `sila.automation.dlx` (topic)
- Queues: `sila_transfer_requested`, `sila_transfer_validated`, `sila_transfer_completed`, `sila_transfer_failed`, `sila_dlq_main`
- Consumers: Um para cada queue (automation worker + dlq worker)

## 📊 Fluxo de Mensagens

```
┌─────────────────────────────────┐
│   Backend API                   │
│   request_transfer()            │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ transfer_requested Event        │
│ ├─ student_id                   │
│ ├─ target_school                │
│ ├─ evaluation                   │
│ └─ metadata                     │
└────────────┬────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │  Retry? (Max: 3)   │
    └────┬───────────┬───┘
         │           │
      Yes│           │No (Success)
         │           │
         │      ┌────▼────────────────┐
         │      │ transfer_completed  │
         │      └─────────────────────┘
         │
      Requeue
         │
    ┌────▼───────────────────────┐
    │ transfer_validated Event    │
    │ (Execute Transfer)          │
    └────┬───────────┬────────────┘
         │           │
      OK │           │ Error
         │           │
    ┌────▼──────┐ ┌──▼──────────────┐
    │  Success  │ │ transfer_failed  │
    └───────────┘ └─────┬──────────┘
                        │
                    Requeue (if retries < max)
                        │
                    ┌────▼──────────────┐
                    │ Dead Letter Queue │
                    │ (sila_dlq_main)   │
                    └────┬──────────────┘
                         │
                    ┌────▼──────────────┐
                    │ DLQ Worker        │
                    │ - Log Critical    │
                    │ - Alert Team      │
                    │ - Manual Review   │
                    └───────────────────┘
```

## 🔧 Componentes Implementados

### 1. `foundation/automation/message_bus.py`

**Classes:**
- `LocalAutomationBus` — Fallback em memória
- `RabbitMQAutomationBus` — Broker real com DLQ
- `_RabbitMQConsumer` — Consumer com retry logic

**Funcionalidades:**
- Auto-detecção de `RABBITMQ_URL`
- DLX automático para cada queue
- Retry com `x-dead-letter-exchange`
- Consumer thread separada para DLQ

### 2. `foundation/automation/automator.py`

**Métodos:**
- `request_transfer()` — Inicia o fluxo de automação
- `_on_transfer_requested()` — Handler do evento 1
- `_on_transfer_validated()` — Handler do evento 2
- `_execute_task()` — Executa a transferência (eventos 3 e 4)
- `_on_dlq_message()` — Handler para mensagens em DLQ

**Logging:**
- Contexto completo de student_id
- Tracking de retry_count
- Integração com auditoria

### 3. `apps/backend/start_dlq_worker.py` (NOVO)

**Classe:** `DLQConsumer`

**Responsabilidades:**
- Consome mensagens de `sila_dlq_main`
- Registra detalhes completos de falha
- Triggers de alertas (Slack, PagerDuty, etc.)
- Estatísticas de processamento

### 4. `docker-compose.minimal.yml`

**Serviços:**
- `sila-db` — PostgreSQL
- `sila-rabbitmq` — RabbitMQ com management UI
- `sila-redis` — Redis
- `sila-backend` — Backend FastAPI
- `sila-automation` — Automation worker (PASSO 13)
- `sila-dlq-worker` — DLQ worker (PASSO 14)

**Configuração:**
- Healthchecks para cada serviço
- Variáveis de ambiente automáticas
- Network isolada
- Volumes para dados persistentes

## 📝 Eventos de Automação

### 1. `transfer_requested`
- **Publicado por:** Backend ao receber request
- **Conteúdo:** Dados da solicitação + avaliação
- **Handler:** `_on_transfer_requested()`

### 2. `transfer_validated`
- **Publicado por:** Automation worker após validação
- **Conteúdo:** Mesmo payload anterior
- **Handler:** `_on_transfer_validated()`

### 3. `transfer_completed`
- **Publicado por:** Automation worker (sucesso)
- **Conteúdo:** student_id + resultado (eligible, score)
- **Destino:** Logged apenas (sem handler)

### 4. `transfer_failed`
- **Publicado por:** Automation worker (erro)
- **Conteúdo:** student_id + mensagem de erro
- **Próximo:** Requeue ou DLQ

## 🔄 Retry e DLQ

### Configuração de Retry

```python
bus = RabbitMQAutomationBus(max_retries=3)
```

### Comportamento

| Tentativa | Ação | Destino |
|-----------|------|---------|
| 1ª falha | Requeue | Main queue |
| 2ª falha | Requeue | Main queue |
| 3ª falha | Requeue | Main queue |
| 4ª falha | Reject | DLQ |

### DLQ Routing

```
Original event: transfer_requested
→ Routing key: dlq.transfer_requested
→ DLQ exchange: sila.automation.dlx
→ DLQ queue: sila_dlq_main
```

## 🧪 Testando Localmente

### Script de Teste Rápido

```bash
cd /home/dev03wsl/sila-system
bash test_passo_13_14.sh
```

### Teste Manual

```bash
# 1. Terminal 1: Stack
docker compose -f docker-compose.minimal.yml up -d --build

# 2. Terminal 2: Logs
docker compose -f docker-compose.minimal.yml logs -f

# 3. Terminal 3: Trigger transfer
curl -X POST "http://localhost:8000/api/v1/transfers" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "TEST-001",
    "target_school": "TEST-SCHOOL",
    "target_class": "TEST-CLASS",
    "academic_year": 2024
  }'

# 4. Observar logs em Terminal 2
# - Backend: request recebido
# - Automation worker: transfer_requested, transfer_validated
# - Execução da transferência
# - Resultado: transfer_completed ou transfer_failed
# - Se DLQ: DLQ worker registra criticamente
```

## 📊 Monitorando em Produção

### Métricas Chave

```
1. Taxa de sucesso: (transfer_completed / transfer_requested)
2. Taxa de falha: (transfer_failed / transfer_requested)
3. Taxa de DLQ: (mensagens em DLQ / minuto)
4. Latência: tempo entre requested → completed
5. Retry attempts: reprocessamentos totais
```

### Exemplos de Queries Prometheus

```promql
# Taxa de sucesso
rate(transfer_completed_total[5m]) / rate(transfer_requested_total[5m])

# Taxa de erro
rate(transfer_failed_total[5m]) / rate(transfer_requested_total[5m])

# Mensagens em DLQ
sila_dlq_main_messages_total

# Latência (p95)
histogram_quantile(0.95, transfer_latency_seconds)
```

## 🚨 Alertas Recomendados

1. **DLQ rate > 10/min** — Investigar causa raiz
2. **Success rate < 95%** — Possível outage
3. **Worker offline** — Reiniciar serviço
4. **RabbitMQ connection lost** — Reconectar
5. **Database unavailable** — Aguardar recovery

## 📚 Documentação Completa

- **PASSO 13:** [docs/PASSO_13_AUTOMACAO_REAL.md](../docs/PASSO_13_AUTOMACAO_REAL.md)
- **PASSO 14:** [docs/PASSO_14_DLQ_REAL.md](../docs/PASSO_14_DLQ_REAL.md)
- **Transfer Integration:** [docs/TRANSFER_PERSISTENCE_INTEGRATION.md](../docs/TRANSFER_PERSISTENCE_INTEGRATION.md)

## 🔐 Segurança

### Em Desenvolvimento
```
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### Em Produção
```
RABBITMQ_URL=amqps://user:password@rabbitmq-prod:5671/
```

**Práticas:**
- Use TLS (`amqps://`)
- Credenciais via secrets manager
- Filas durable
- Retenção de DLQ (7 dias)
- Auditoria completa

## ❓ Troubleshooting

### Serviços não iniciam
```bash
docker compose -f docker-compose.minimal.yml logs
docker compose -f docker-compose.minimal.yml ps
```

### Mensagens não processadas
```bash
docker compose -f docker-compose.minimal.yml logs sila-automation
docker compose -f docker-compose.minimal.yml logs sila-dlq-worker
```

### RabbitMQ sem conexão
```bash
docker compose -f docker-compose.minimal.yml exec sila-rabbitmq \
  rabbitmq-diagnostics ping
```

### DLQ cheio
```bash
# Analisar mensagens
docker compose -f docker-compose.minimal.yml logs sila-dlq-worker | grep "DLQ_RECORD"

# Limpar (com cuidado)
docker compose -f docker-compose.minimal.yml exec sila-rabbitmq \
  rabbitmqctl purge_queue sila_dlq_main
```

## 🎓 Próximos Passos

1. ✅ PASSO 13: Automação Real — **COMPLETO**
2. ✅ PASSO 14: DLQ Real — **COMPLETO**
3. ⏳ Integrar alertas (Slack, PagerDuty)
4. ⏳ Dashboard Grafana
5. ⏳ Auto-remediation para falhas comuns
6. ⏳ Migrar para Kafka (opcional)

## 📞 Suporte

Para dúvidas ou issues:
1. Verificar [PASSO_13_AUTOMACAO_REAL.md](../docs/PASSO_13_AUTOMACAO_REAL.md)
2. Verificar [PASSO_14_DLQ_REAL.md](../docs/PASSO_14_DLQ_REAL.md)
3. Analisar logs: `docker compose logs -f`
4. RabbitMQ UI: http://localhost:15672

---

**Data:** 2024-01-15  
**Status:** ✅ Production Ready  
**Versão:** 1.0
