# 🔐 Fluxograma da Fase 3 (Auth) — SILA System

## Diagrama de Fluxo de Autenticação e Migração

```mermaid
graph TD
    A["🌐 Frontend React\n(axios/fetch)"] -->|POST /login| B["📌 Endpoint de Login\nmodules/auth/endpoints.py"]

    B -->|email + password| C["🔍 UserRepository\nmodules/auth/repository.py"]
    C -->|Query DB| D[("🗄️ Database\n(PostgreSQL)")]
    D -->|User ORM| C
    C -->|User object| B

    B -->|user.id| E["🔑 JWT Handler\ncore/auth.py"]
    E -->|create_access_token| F["✅ access_token\n(15 min)"]
    E -->|create_refresh_token| G["✅ refresh_token\n(7 dias)"]

    B -->|access_token +\nrefresh_token| A

    H["💾 Token Storage\n(Frontend localStorage)"] <-->|bearer token| A

    A -->|GET /protected\nAuthorization: Bearer ...| I["🛡️ Auth Middleware\nget_current_active_user"]
    I -->|Decode token| E
    E -->|Validate signature| J{"Token válido?"}
    J -->|✅ Sim| K["🔗 Resolve user.id"]
    K -->|Fetch from DB| D
    D -->|User + scopes| L["👤 User Object\n(com scopes, level)"]
    J -->|❌ Não| M["🚫 HTTP 401\nUnauthorized"]

    L -->|user.scopes| N["📋 Permission Check\nmodules/auth/permissions.py"]
    N -->|requires_scopes\nrequires_level| O{"Permissão OK?"}
    O -->|✅ Sim| P["✅ Request Processado"]
    O -->|❌ Não| Q["🚫 HTTP 403\nForbidden"]

    P -->|Response| A
    Q -->|Error Detail| A
    M -->|Error Detail| A

    %% ================================
    %% PONTOS DE FALHA E MIGRAÇÃO
    %% ================================

    R["⚠️ FASE 3 RISKS"] -.->|1. Escopo tenant:admin| N
    R -.->|2. Level hierarchy| N
    R -.->|3. User object schema| L
    R -.->|4. Token claims| E

    %% Sincronismo com core
    S["🔗 core/auth.py\nInjection Point"] -.->|sync| E
    S -.->|sync| I

    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style E fill:#fce4ec
    style F fill:#c8e6c9
    style G fill:#c8e6c9
    style H fill:#f1f8e9
    style I fill:#ffe0b2
    style J fill:#ffccbc
    style K fill:#bbdefb
    style L fill:#e0bee7
    style N fill:#ffe0b2
    style O fill:#ffccbc
    style P fill:#c8e6c9
    style Q fill:#ffcdd2
    style M fill:#ffcdd2
    style R fill:#ffe082
    style S fill:#b3e5fc
```

---

## 📊 Estados e Transições Críticas

| Fase | Component         | Estado           | Status       | Observação                                |
| ---- | ----------------- | ---------------- | ------------ | ----------------------------------------- |
| 1️⃣   | `endpoints.py`    | Login iniciado   | ✅ OK        | POST /login aceita JSON, form, query      |
| 2️⃣   | `repository.py`   | Fetch user       | ✅ OK        | Query DB por email/password               |
| 3️⃣   | `core/auth.py`    | JWT criação      | ✅ OK        | Tokens com claims básicos                 |
| 4️⃣   | Middleware        | Token decode     | ✅ OK        | Suporta fallback de secrets               |
| 5️⃣   | `user.py` (model) | User object      | ⚠️ VERIFICAR | Faltam campos `scopes`, `role` no ORM     |
| 6️⃣   | `permissions.py`  | Scope validation | ⚠️ FALHA     | `tenant:admin` não aparece em user.scopes |
| 7️⃣   | `permissions.py`  | Level validation | ✅ OK        | Hierarquia `local < provincial < central` |
| 8️⃣   | Response          | Authorized       | ❌ FALHA     | HTTP 403 quando deveria ser 200           |

---

## 🔴 Pontos de Falha Identificados

### **Falha #1: Escopo `tenant:admin` não é populado**

**Localização:** `modules/auth/models/user.py` (ORM) + `modules/auth/repository.py`
(fetch)

**Problema:**

- O modelo ORM `User` não possui campo `scopes` (lista de strings)
- O repositório não extrai/calcula escopos ao retornar usuário

**Manifestação:**

```python
# Em permissions.py:requires_scopes()
user_scopes = getattr(user, "scopes", [])  # Retorna [] sempre!
```

**Solução:** Adicionar campo `scopes` ao modelo `User` ou calcular dinamicamente no
repositório.

---

### **Falha #2: User.level é enum, não string**

**Localização:** `modules/auth/models/user.py` (ORM)

**Problema:**

- Banco de dados armazena como `Enum.value` (string)
- ORM retorna como `Enum` object
- `permissions.py:requires_level()` tenta comparar enum contra string

**Manifestação:**

```python
# Em permissions.py
user_level_str = user_level.value if isinstance(user_level, Enum) else user_level
# Funciona, mas frágil
```

**Solução:** Padronizar sempre retornar como string no DTO (`UserRead`).

---

### **Falha #3: JWT claims não incluem scopes/level**

**Localização:** `core/auth.py` (token creation)

**Problema:**

- `create_access_token()` recebe apenas `subject` (user_id)
- Não inclui `scopes`, `level`, `role` no payload

**Manifestação:**

```python
# Em endpoints.py:login()
access = create_access_token(subject=str(user.id))  # ❌ Sem scopes!
```

**Solução:** Incluir `additional_claims` com scopes/level no token.

---

## 🔄 Fluxo de Migração Esperado (Fase 3 → Completa)

```mermaid
graph LR
    A["Fase 2\n(User auth OK)"] -->|Adicionar scopes/level| B["Fase 3a\n(Enhanced User)"]
    B -->|JWT claims + claims| C["Fase 3b\n(Token enrichment)"]
    C -->|Permission checks| D["Fase 3c\n(Scope + Level OK)"]
    D -->|Testes passam| E["✅ Fase 3\n(COMPLETA)"]

    style A fill:#fff9c4
    style B fill:#ffe082
    style C fill:#ffb74d
    style D fill:#ff8a65
    style E fill:#81c784
```

---

## 📋 Checklist de Validação Rápida

- [ ] `User.scopes` (campo) existe no ORM
- [ ] `UserRead.scopes` (DTO) existe e é `List[str]`
- [ ] `create_access_token()` inclui `scopes` em `additional_claims`
- [ ] `create_access_token()` inclui `level` em `additional_claims`
- [ ] `get_current_active_user()` extrai `scopes` do token decodificado
- [ ] `requires_scopes()` valida contra `user.scopes` (lista)
- [ ] `requires_level()` valida contra `user.level` (string)
- [ ] Testes cobrem `tenant:admin` scope
- [ ] Testes cobrem `central` level
- [ ] `test_auth.py` passa com 100% de cobertura
