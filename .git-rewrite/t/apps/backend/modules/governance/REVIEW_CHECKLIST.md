# ✅ Revisão do Módulo Governance - Checklist

## 📋 Status da Implementação

### ✅ 1. Schemas Pydantic (`schemas/api_schemas.py`)

- [x] `InstitutionCreate`, `InstitutionUpdate`, `InstitutionResponse`,
      `InstitutionsListResponse`
- [x] `MandateCreate`, `MandateUpdate`, `MandateResponse`, `MandatesListResponse`
- [x] `DecisionCreate`, `DecisionUpdate`, `DecisionResponse`, `DecisionsListResponse`
- [x] `CouncilMeetingCreate`, `CouncilMeetingUpdate`, `CouncilMeetingResponse`,
      `CouncilMeetingsListResponse`
- [x] Todos os schemas usam `BaseSchema` do módulo comum
- [x] Validações e tipos corretos (UUID, datetime, Optional, etc.)

### ✅ 2. Models ORM

- [x] **Institution** (`models/institution.py`)

  - UUID como primary key
  - `created_at`, `updated_at`, `deleted_at` (soft delete)
  - Relacionamento com Mandates

- [x] **Mandate** (`models/mandate.py`)

  - UUID como primary key
  - Timestamps e soft delete
  - FK para Institution (UUID)

- [x] **Decision** (`models/decision.py`)

  - UUID como primary key
  - Timestamps e soft delete
  - FK para CouncilMeeting (UUID)

- [x] **CouncilMeeting** (`models/council_meeting.py`)
  - UUID como primary key
  - Timestamps e soft delete
  - Relacionamento com Decisions

### ✅ 3. Repository (`repository.py`)

- [x] Todos os métodos usam UUID em vez de int
- [x] Soft delete implementado em todos os métodos de listagem e busca
- [x] Métodos `delete_*` implementam soft delete (definem `deleted_at`)
- [x] Filtros e paginação funcionando
- [x] Uso de `datetime.now(timezone.utc)` em vez de `datetime.utcnow()` (deprecated)

### ✅ 4. Service (`service.py`)

- [x] Usa `GovernanceRepository` para acesso a dados
- [x] Conversão de models ORM para schemas Pydantic
- [x] CRUD completo para todas as entidades
- [x] Métodos de listagem retornam `ListResponse` com `items` e `total`

### ✅ 5. Controller (`controller.py`)

- [x] Router exportado corretamente
- [x] Endpoints CRUD para todas as entidades:
  - Institutions: POST, GET (list), GET (by id), PUT, DELETE
  - Mandates: POST, GET (list), GET (by id), PUT, DELETE
  - Decisions: POST, GET (list), GET (by id), PUT, DELETE
  - Council Meetings: POST, GET (list), GET (by id), PUT, DELETE
- [x] Filtros de query params implementados
- [x] Documentação OpenAPI completa (summary, description, tags)
- [x] Tratamento de erros HTTP (404, etc.)
- [x] Endpoint `/ping` para health check

### ✅ 6. Integração

- [x] `endpoints.py` importa router de `controller.py` (compatibilidade com
      auto-discovery)
- [x] Sem erros de lint
- [x] Imports corretos e sem dependências circulares

---

## 🧪 Teste Manual Rápido

### Pré-requisitos

1. Servidor FastAPI rodando: `uvicorn main:app --reload`
2. Banco de dados configurado e migrações aplicadas
3. Token JWT válido (para endpoints protegidos)

### Teste 1: Health Check (sem autenticação)

```bash
curl -X GET "http://localhost:8000/api/v1/governance/ping"
```

**Esperado:**

```json
{
  "message": "pong",
  "timestamp": "2025-01-XX..."
}
```

### Teste 2: Listar Instituições (sem autenticação)

```bash
curl -X GET "http://localhost:8000/api/v1/governance/institutions"
```

**Esperado:**

```json
{
  "items": [],
  "total": 0
}
```

### Teste 3: Criar Instituição (com autenticação)

```bash
curl -X POST "http://localhost:8000/api/v1/governance/institutions" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ministério da Saúde",
    "acronym": "MINSA",
    "institution_type": "ministry",
    "jurisdiction": "Angola"
  }'
```

**Esperado:** Status 201 com `InstitutionResponse` completo

### Teste 4: Buscar Instituição por ID

```bash
curl -X GET "http://localhost:8000/api/v1/governance/institutions/{INSTITUTION_ID}"
```

**Esperado:** `InstitutionResponse` ou 404 se não encontrado

### Teste 5: Swagger UI

Acesse: `http://localhost:8000/docs`

Verifique:

- [ ] Seção "Governance" aparece
- [ ] Subseções: "Governance - Institutions", "Governance - Mandates", etc.
- [ ] Endpoints `/ping`, `/institutions`, `/mandates`, `/decisions`, `/council-meetings`
- [ ] Schemas Pydantic aparecem corretamente

---

## 🔍 Verificações Importantes

### ✅ Verificar Importações

```python
# Testar importação do router
from modules.governance.controller import router
assert len(router.routes) > 0  # Deve ter várias rotas
```

### ✅ Verificar Relacionamentos

- Institution → Mandates (1:N)
- CouncilMeeting → Decisions (1:N)
- Relacionamentos devem funcionar com UUID

### ✅ Verificar Soft Delete

- Listagens não devem retornar registros com `deleted_at != None`
- Busca por ID não deve encontrar registros deletados
- Delete deve apenas marcar `deleted_at`, não remover fisicamente

---

## ⚠️ Pontos de Atenção

1. **UUID vs String**: Certifique-se de que UUIDs são convertidos corretamente entre
   string e UUID
2. **Timezone**: Timestamps usam `timezone=True` no SQLAlchemy
3. **Relacionamentos**: Verificar se `back_populates` está correto em ambos os lados
4. **Filtros**: Query params opcionais devem funcionar corretamente

---

## 📝 Próximos Passos

- [ ] Criar Seed Data (`seed_data.py`)
- [ ] Criar Testes Unitários (`tests/test_repository.py`, `tests/test_service.py`)
- [ ] Criar Testes de Integração (`tests/test_integration.py`)
- [ ] Documentar exemplos de uso no README

---

**Status Geral:** ✅ **Pronto para testes manuais e seed data**
