# Relatório Forense — Falso 500 nas Transições do Workflow

**Data:** 2026-06-08  
**Fonte:** `/tmp/uvicorn_out.log` (linhas 1240–1275, 1960–2520)  
**Preparado por:** IDE 1 — missão "provar causa do falso 500"

---

## ERRO OBSERVADO

```
POST /governance/workflow/workflow/instances/{instance_id}/transitions
↓
HTTP 500 Internal Server Error
```

A transição executa e persiste no banco (timeline mostra `STATUS_CHANGED`),
mas o response HTTP é 500.

---

## STACK TRACE COMPLETO

```
fastapi/routing.py:115 → app()
  │
  ├── fastapi/routing.py:377 → app()
  │   └── content = await serialize_response(...)
  │       └── fastapi/routing.py:215 → serialize_response()
  │           └── raise ResponseValidationError(...)
  │
  └── fastapi.exceptions.ResponseValidationError: 1 validation error:
        {'type': 'get_attribute_error',
         'loc': ('response', 'is_overdue'),
         'msg': "Error extracting attribute: TypeError: can't compare
                 offset-naive and offset-aware datetimes",
         'input': WorkflowInstance(
           deadline=datetime.datetime(2026,6,15,22,22,36,586407,
                                      tzinfo=datetime.timezone.utc),
           completed_at=datetime.datetime(2026,6,8,23,28,30,734331),
           #                             ^^^^^^^^^^^^^^^^^^^^^^^^^^
           #                              NAIVE — sem timezone
           ...
         ),
         'ctx': {'error': "TypeError: can't compare offset-naive
                           and offset-aware datetimes"}}
```

### Arquivos da pilha

| # | Arquivo | Linha | Função |
|---|---------|-------|--------|
| 1 | `starlette/middleware/exceptions.py` | 63 | `__call__` |
| 2 | `starlette/_exception_handler.py` | 53 | `wrapped_app` |
| 3 | `starlette/_exception_handler.py` | 42 | `wrapped_app` |
| 4 | `fastapi/middleware/asyncexitstack.py` | 18 | `__call__` |
| 5 | `starlette/routing.py` | 716 | `__call__` |
| 6 | `starlette/routing.py` | 736 | `app` |
| 7 | `starlette/routing.py` | 290 | `handle` |
| 8 | `fastapi/routing.py` | 115 | `app` |
| 9 | `fastapi/routing.py` | 377 | `app` — **serialize_response** |
| 10 | `fastapi/routing.py` | 215 | `serialize_response` — **raise** |

---

## OBJETO RETORNADO

```python
WorkflowInstance(
  id=UUID('109b87a5-4105-40ea-af73-e13825ed83d3'),
  workflow_id=UUID('dd3c91d0-ad8f-4d2c-a80c-c0b7813b7255'),
  current_state_id=UUID('acf8ffa1-0693-443a-8f0d-d96d85a11562'),
  status=<WorkflowStatus.COMPLETED: 'completed'>,
  started_at=datetime.datetime(2026,6,8,22,22,36,586596,
                                tzinfo=datetime.timezone.utc),    # AWARE
  completed_at=datetime.datetime(2026,6,8,23,28,30,734331),       # NAIVE
  deadline=datetime.datetime(2026,6,15,22,22,36,586407,
                              tzinfo=datetime.timezone.utc),      # AWARE
  updated_at=datetime.datetime(2026,6,8,23,28,30,734340),         # NAIVE
  ...
)
```

---

## SCHEMA ESPERADO

**Arquivo:** `apps/backend/app/modules/governance/workflow/api/schemas/workflow_schema.py`

```python
class WorkflowInstanceResponse(BaseModel):
    # ...
    is_overdue: bool  # ← campo REQUERIDO
    is_active: bool
```

**OpenAPI componente:** `WorkflowInstanceResponse` — `is_overdue: bool (required)`

---

## CAMPO DIVERGENTE

| Campo | Problema |
|-------|----------|
| `is_overdue` | Propriedade avaliada durante serialização falha com `TypeError` |

---

## CAUSA CONFIRMADA

**Arquivo:** `apps/backend/app/modules/governance/workflow/domain/models/workflow_instance.py`

### Linha 47-51 — `is_overdue` property:
```python
@property
def is_overdue(self) -> bool:
    if not self.deadline:
        return False
    return datetime.now() > self.deadline   # ← NAIVE vs AWARE
```

`datetime.now()` retorna **naive** (sem timezone).  
`self.deadline` vem do banco como **aware** (UTC).

Python ≥3.12 proíbe comparação entre naive e aware.

### Raiz do problema — `complete()` (linhas 53-57):
```python
def complete(self):
    self.status = WorkflowStatus.COMPLETED
    self.completed_at = datetime.now()     # ← NAIVE
    self.updated_at = datetime.now()       # ← NAIVE
```

E também na engine (`workflow_engine.py`):
```python
deadline=datetime.now() + timedelta(...)   # ← NAIVE
```

Mas o banco devolve `deadline` como **aware** (porque a coluna é `TIMESTAMPTZ`),
criando o mismatch.

### Cadeia completa

1. `start_workflow()` salva `deadline` como naive (`datetime.now()`)
2. PostgreSQL coluna `TIMESTAMPTZ` converte para UTC na escrita e devolve **aware** na leitura
3. `execute_transition()` → `complete()` → salva `completed_at` como naive (`datetime.now()`)
4. FastAPI tenta serializar: `response_model=WorkflowInstanceResponse` precisa de `is_overdue`
5. `is_overdue` faz `datetime.now() > self.deadline` → **TypeError: naive vs aware**
6. `ResponseValidationError` é elevado, FastAPI retorna 500

---

## CORREÇÃO MÍNIMA NECESSÁRIA

**Arquivo:** `apps/backend/app/modules/governance/workflow/domain/models/workflow_instance.py`

### Linha 49:
```python
# ANTES:
return datetime.now() > self.deadline

# DEPOIS:
return datetime.now(tz=self.deadline.tzinfo) > self.deadline
```

### Linhas 54-57:
```python
# ANTES:
self.completed_at = datetime.now()
self.updated_at = datetime.now()

# DEPOIS:
self.completed_at = datetime.now(datetime.timezone.utc)
self.updated_at = datetime.now(datetime.timezone.utc)
```

### Arquivo: `apps/backend/app/modules/governance/workflow/application/services/workflow_engine.py`
`start_workflow()` usa `datetime.now()` para `deadline` — deve usar `datetime.now(datetime.timezone.utc)`.

---

## EVIDÊNCIA FÍSICA

Log do servidor em `/tmp/uvicorn_out.log`:
- 7 ocorrências do mesmo erro (linhas 1268, 1962, 2096, 2239, 2373, 2516, 2650)
- Todas com o mesmo padrão: `is_overdue` property → naive vs aware datetime
- Reproduzível com qualquer workflow após executar transição
