# SILA System - Próximos Passos (2026-02-22)

## 🎯 Objetivo

Continuar o desenvolvimento com base sólida, sem duplicatas, erros de import ou misalinhamentos BD/ORM.

## 📌 Status Atual

✅ **Saneamento completo** - Veja `SANEAMENTO_COMPLETO.md`

- Codebase limpo (duplicatas removidas)
- Imports corrigidos (33 arquivos)
- ORM sincronizado com BD
- 5 users de teste criados

## 🚀 Roteiro Imediato

### 1. Validar Sistema (15 min)

```bash
cd /home/dev03wsl/sila-system/apps/backend

# Ativar venv
source .venv/bin/activate

# Teste 1: Verificar users criados
PYTHONPATH=$(pwd):$PYTHONPATH python -c "
from sqlalchemy import select, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from modules.identity.models.user import User
import asyncio
import os

async def test():
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        print(f'✅ Found {len(users)} users')
        for u in users:
            print(f'   - {u.email} ({u.administrative_level})')

asyncio.run(test())
"
```

### 2. Executar Testes (30 min)

```bash
# Testes unitários
pytest tests/unit/ -v

# Testes de integração (se houver)
pytest tests/integration/ -v

# Coverage
pytest tests/ --cov=app --cov=modules --cov-report=html
```

### 3. Iniciar Servidor de Desenvolvimento (5 min)

```bash
# Terminal 1: Backend API
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Teste de acesso
curl http://localhost:8000/docs
```

### 4. Testar Autenticação (10 min)

```bash
# Teste de login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "central@sila.gov.ao",
    "password": "Test1234"
  }'
```

## 📋 Tarefas Pendentes

### A. Corrigir Senhas de Produção

**Problema:** Seed usa senha simples (`Test1234`) e hash de teste

**Solução:**
1. Criar migration para adicionar coluna hash mais seguro
2. Implementar `get_password_hash()` corrigido (bcrypt version issue)
3. Atualizar seed com senhas reais
4. Executar:
   ```bash
   python -m alembic upgrade head
   python seeds/core/seed_founding_users_sql.py
   ```

### B. Testes de Permissão

**Verificar RBAC:**
- User ADMIN_CENTRAL pode acessar tudo
- User ADMIN_PROVINCIAL vê apenas Huambo
- User CITIZEN tem acesso limitado

```bash
pytest tests/rbac/ -v
```

### C. Validar Foreign Keys

**Verificar integridade referencial:**
```bash
psql -h 127.0.0.1 -U sila_user -d sila_db << 'SQL'
-- Verificar FKs para locations
SELECT 
  constraint_name,
  table_name,
  column_name,
  foreign_table_name
FROM information_schema.key_column_usage
WHERE foreign_table_name IS NOT NULL
ORDER BY table_name;
SQL
```

### D. Atualizar Documentação

- [ ] README.md com instruções de setup
- [ ] Architecture.md com diagrama de modelos
- [ ] API.md com endpoints atualizados

## 🔐 Segurança - ANTES DE IR PARA STAGING

1. **Remover senhas hardcoded:**
   ```bash
   # Verificar secrets
   grep -r "password\|PASSWORD\|secret\|SECRET" \
     --include="*.py" \
     --include=".env*" \
     apps/backend | grep -v ".venv" | grep -v "docstring"
   ```

2. **Atualizar .env.prod:**
   ```
   DATABASE_URL=postgresql+asyncpg://[USER]:[SECURE_PASS]@[HOST]:[PORT]/[DB]
   SECRET_KEY=[NOVO_SECRET_ALEATORIO]
   ```

3. **Regenerar senhas de users:**
   - Usar random password generator
   - Armazenar em password manager
   - Distribuir aos admins

## 📊 Verificações Finais

```bash
# Sintaxe Python
python -m py_compile apps/backend/**/*.py

# Imports
python -c "from modules.identity.models.user import User; print('✅ Imports OK')"

# BD Connection
PYTHONPATH=apps/backend:$PYTHONPATH python -c "
import asyncio
from app.core.database import AsyncSessionLocal

async def test():
    async with AsyncSessionLocal() as db:
        await db.connection()
        print('✅ BD Connected')

asyncio.run(test())
"

# Migrate
cd apps/backend
python -m alembic -c alembic_core/alembic.ini current
```

## 🎓 Referências

- Instruções originais: `ROOT_CAUSE_AND_FIX_PLAN.md`
- Resultado do saneamento: `SANEAMENTO_COMPLETO.md`
- Configuração local: `comandos_dia_dia.md`

## 💬 Contato

Se houver problemas:
1. Verificar `SANEAMENTO_COMPLETO.md` para contexto
2. Consultar logs: `alembic_core/alembic.ini`
3. Rodar seed novamente se necessário

---

**Próximo Passo:** Executar seção "Validar Sistema" acima ⬆️

