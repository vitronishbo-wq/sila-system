# DEMO RUNBOOK — Nascimento BI NIF SS

## Pré-requisitos

- Python >=3.11, <4
- Poetry
- Docker + docker-compose
- PostgreSQL 15+ (local ou Docker)
- Redis 7+ (local ou Docker)
- `.env` na raiz com variáveis resolvidas

## 1. Activar ambiente virtual

```bash
cd /opt/sila-system
source .venv/bin/activate
```

## 2. Arrancar infra-estrutura

```bash
make infra-up
```

Verificar:
- `pg_isready -h localhost -p 5432`
- `redis-cli -h localhost ping` → `PONG`

## 3. Arrancar Celery (worker separado)

```bash
# Terminal 1 — worker
.venv/bin/celery -A apps.backend.app.core.celery_app worker --loglevel=info
```

## 4. Bootstrap do banco

```bash
make db-migrate       # Alembic migrations (upgrade head)
make update-indexes   # Sincronizar índices do projecto
```

## 5. Carregar workflows no PostgreSQL

```bash
python scripts/load_process_workflows.py
```

Esperado:
```
Loaded apps/backend/app/processes/nascimento_bi_nif_ss/workflow_definition.json
Loaded apps/backend/app/processes/beneficio_social/workflow_definition.json
Loaded apps/backend/app/processes/licenciamento_comercial/workflow_definition.json
```

## 6. Executar fluxo nascimento (3 cenários)

```bash
python -m pytest apps/backend/app/processes/nascimento_bi_nif_ss/tests/e2e/ -v
```

### Fluxos validados

| Teste | Descrição | Estado |
|---|---|---|
| `test_nascimento_success_e2e` | Nascimento → Certidão → NIF → SS | ✅ |
| `test_nascimento_cancel_e2e` | Cancelamento a meio do fluxo | ✅ |
| `test_nascimento_reject_e2e` | Certidão inválida → sem NIF/SS | ✅ |

## 7. Validação final

```bash
make daily-audit
```

## Resumo de health checks

```bash
# Infra
pg_isready -h localhost -p 5432          # PostgreSQL
redis-cli -h localhost ping               # Redis

# Import crítico
python -c "from apps.backend.app.api.deps import get_identity_context; print('OK')"

# Loader
python scripts/load_process_workflows.py

# Testes
python -m pytest apps/backend/app/processes/nascimento_bi_nif_ss/tests/e2e/ -v --tb=short
```

## Erros conhecidos (não bloqueantes)

- `core/dependencies/__init__.py:5` — import residual `from core.security import IAMClient` falha fora do contexto uvicorn. Não afecta os fluxos de nascimento.
- 54 falhas/24 erros no resto do test suite (DLQ, orquestração, race-conditions). Nenhum relacionado ao módulo nascimento_bi_nif_ss.
