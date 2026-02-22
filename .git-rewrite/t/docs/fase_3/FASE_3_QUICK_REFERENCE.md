# ⚡ FASE 3 — QUICK REFERENCE (Cheat Sheet)

**Print e cole na parede! 👇**

---

## 🎯 Os 3 Problemas Críticos

| #   | Problema              | Arquivo          | Fix                                                 |
| --- | --------------------- | ---------------- | --------------------------------------------------- |
| 1️⃣  | User ORM sem `scopes` | `models/user.py` | Adicionar: `scopes = Column(JSON, default=[])`      |
| 2️⃣  | User ORM sem `role`   | `models/user.py` | Adicionar: `role = Column(String(50))`              |
| 3️⃣  | JWT sem scopes/level  | `endpoints.py`   | Usar `additional_claims` em `create_access_token()` |

---

## 🔧 Correção Rápida (Copy-Paste)

### 1️⃣ SQL Migration (Execute AGORA!)

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS scopes JSON NOT NULL DEFAULT '[]';
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) NULL;
```

### 2️⃣ models/user.py (Add após `level`)

```python
# Adicionar após: level = Column(PgEnum(...))
scopes = Column(JSON, nullable=False, default=lambda: [])
role = Column(String(50), nullable=True)
```

### 3️⃣ models/user.py (Atualizar DTO)

```python
# Adicionar em UserRead
class UserRead(UserBase):
    # ... existing fields ...
    scopes: List[str] = []
    role: Optional[str] = None
```

### 4️⃣ endpoints.py (Atualizar login)

```python
# Adicionar ANTES de create_access_token
additional_claims = {
    "scopes": user.scopes or [],
    "level": user.level.value if user.level else "local",
    "role": user.role or "",
}

# Atualizar chamada
access = create_access_token(
    subject=str(user.id),
    additional_claims=additional_claims  # ← Adicionar isso
)
```

---

## ✅ Validação Rápida

```bash
# Executar validador
python3 validate_phase_3.py --report

# Esperado após fix: ✅ PASSED

# Executar testes
pytest apps/backend/tests/test_auth.py::test_admin_scope_access -v

# Esperado: PASSED ✓
```

---

## 📊 Status Atual

| Componente     | Status        | Ação             |
| -------------- | ------------- | ---------------- |
| permissions.py | ✅ OK         | Nenhuma          |
| endpoints.py   | ⚠️ Incompleto | Adicionar claims |
| models/user.py | ❌ CRÍTICO    | Adicionar campos |
| core/auth.py   | ✅ OK         | Nenhuma          |
| security.py    | ⚠️ Review     | Verificar        |

---

## 🚀 Timeline

- **Now:** Executar SQL + Código fixes (30 min)
- **+30min:** Re-validar com script
- **+45min:** Testes passarem
- **+60min:** Fase 3 COMPLETA ✅

---

## 🔍 Debugging Rápido

**Erro: "test_admin_scope_access FAILED"**

```bash
# Verificar que scopes está no token
python3 -c "
import jwt
token = 'eyJ...'  # Cole aqui
print(jwt.decode(token, options={'verify_signature': False}))
# Deve mostrar: 'scopes': ['tenant:admin']
"
```

**Erro: "AttributeError: no attribute 'scopes'"**

```bash
# Verificar coluna no DB
psql sila_db -c "SELECT scopes FROM users LIMIT 1;"
# Se falha: executar SQL migration acima
```

---

## 📝 Documentação Completa

```
FASE_3_FLUXOGRAMA.md              ← Entender arquitetura
FASE_3_CHECKLIST_AUDITORIA.md     ← Todos os critérios
FASE_3_VALIDACAO_RESUMO.md        ← Análise de problemas
FASE_3_GUIA_IMPLEMENTACAO.md      ← Código completo + debug
validate_phase_3.py               ← Script automático
phase_3_validation_report.json    ← Relatório último run
```

---

## ⏱️ Tempos

| Atividade     | Tempo      |
| ------------- | ---------- |
| Ler Quick Ref | 2 min      |
| Aplicar Fixes | 30 min     |
| Rodar Testes  | 5 min      |
| Validar       | 2 min      |
| **TOTAL**     | **39 min** |

---

## 🎓 Conceitos-Chave

```
scopes  = ["tenant:admin", "read", "write"]  ← Permissões
level   = "central"                          ← Hierarquia
role    = "admin"                            ← Cargo
JWT     = {sub, scopes, level, role, exp}   ← Token
```

---

**Print agora! ↓↓↓**
