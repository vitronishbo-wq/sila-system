# Validação — Correção do Falso 500 nas Transições do Workflow

**Data:** 2026-06-08  
**Arquivos alterados:**
- `apps/backend/app/modules/governance/workflow/domain/models/workflow_instance.py`
- `apps/backend/app/modules/governance/workflow/application/services/workflow_engine.py`

---

## ANTES

### Erro

```
POST /governance/workflow/workflow/instances/{id}/transitions
→ HTTP 500 Internal Server Error
```

### Stack

```
fastapi/routing.py:377 → serialize_response()
  →  is_overdue property
    →  datetime.now() > self.deadline
      →  TypeError: can't compare offset-naive and offset-aware datetimes
```

### Causa

`datetime.now()` retorna naive (sem timezone). `self.deadline` vem do banco como aware (UTC via TIMESTAMPTZ). Python ≥3.12 proíbe a comparação.

### Raiz

`complete()` e `set_variable()` usam `datetime.now()` para `completed_at`/`updated_at` (naive). O banco devolve `started_at`/`deadline` como aware (UTC). O mismatch é permanente para qualquer instância após a primeira transição.

---

## DEPOIS

### Correção aplicada

**`workflow_instance.py`:**
- Adicionado `from datetime import timezone`
- Helper `_utcnow()` que retorna `datetime.now(timezone.utc)`
- Todas as ocorrências de `datetime.now()` → `_utcnow()`
- `started_at` default factory → `_utcnow`
- `time_in_state`, `is_overdue`, `complete`, `terminate`, `suspend`, `resume`, `set_variable`

**`workflow_engine.py`:**
- Adicionado `timezone` ao import
- `deadline` em `start_workflow`: `datetime.now()` → `datetime.now(timezone.utc)`

### Resultado

```
POST /governance/workflow/workflow/instances/{id}/transitions
→ HTTP 200 OK
→ Payload: { "id": "...", "status": "active", "is_overdue": false, ... }
```

Payload de exemplo retornado:
```json
{
  "id": "f8b8117c-4f53-4ec1-9f58-787565383440",
  "workflow_id": "dd3c91d0-ad8f-4d2c-a80c-c0b7813b7255",
  "current_state_id": "...",
  "entity_type": "birth_record",
  "entity_id": "660e8400-...",
  "citizen_id": "956fb078-...",
  "status": "active",
  "variables": {},
  "started_at": "2026-06-08T23:18:25.123456+00:00",
  "completed_at": null,
  "deadline": "2026-06-15T23:18:25.123456+00:00",
  "is_active": true,
  "is_overdue": false
}
```

---

## WORKFLOWS TESTADOS

### NASCIMENTO_BI_NIF_SS

| Passo | Endpoint | HTTP Antes | HTTP Depois |
|-------|----------|-----------|-------------|
| Start | POST /workflow/start | 200 | 200 |
| TO_CERTIDAO | POST /.../transitions | 500 | **200** |
| TO_NIF | POST /.../transitions | 500 | **200** |
| TO_SS | POST /.../transitions | 500 | **200** |
| Timeline | GET /.../timeline | 200 | 200 |

**Timeline:** 4 entries (WORKFLOW_STARTED → CERTIDAO_EMITIDA → NIF_ATRIBUIDO → SS_ATRIBUIDO)

### BENEFICIO_SOCIAL

| Passo | Endpoint | HTTP Antes | HTTP Depois |
|-------|----------|-----------|-------------|
| Start | POST /workflow/start | 200 | 200 |
| TO_VERIFICACAO_NIF | POST /.../transitions | 500 | **200** |
| TO_VERIFICACAO_SS | POST /.../transitions | 500 | **200** |
| TO_APROVADO | POST /.../transitions | 500 | **200** |
| Timeline | GET /.../timeline | 200 | 200 |

**Timeline:** 4 entries (WORKFLOW_STARTED → VERIFICACAO_NIF → VERIFICACAO_SS → APROVADO)

---

## VERIFICAÇÕES ADICIONAIS

- [x] Transição retorna 200 em vez de 500
- [x] Payload da resposta é JSON válido com todos os campos esperados
- [x] `is_overdue` presente e sem erro
- [x] Timeline íntegra (mesmo número de entradas, mesmos estados)
- [x] Estados finais corretos (SS_ATRIBUIDO, APROVADO)
- [x] Nenhuma alteração em routers, schemas, definitions, EventBus, Registry

---

## RESULTADO

```
┌─────────────────────────────────────────────┐
│              6 / 6  PASS                    │
│                                             │
│  Workflow       │ Transições │ Timeline     │
│ ─────────────── │ ────────── │ ─────────── │
│ NASCIMENTO_BI   │  ✓ 3/3     │  ✓ 4 entradas│
│ BENEFICIO_SOCIAL│  ✓ 3/3     │  ✓ 4 entradas│
└─────────────────────────────────────────────┘
```

**VEREDITO: PASS** — Falso 500 eliminado. Workflow governance operacional.
