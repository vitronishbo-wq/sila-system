# 🔍 Diagnóstico: Erro `socket.gaierror` no Alembic

## Causa-Raiz Identificada

**Erro**: `socket.gaierror: [Errno -3] Temporary failure in name resolution`  
**Origem**: Alembic tenta conectar ao PostgreSQL no host `db` (via Docker network), mas:

✅ **.env não existia** → Variáveis de ambiente vazias  
❌ **PostgreSQL não está rodando** → Docker container não iniciado  
❌ **Host `db` não resolvível** → Ao fora de um container/docker-compose, não consegue encontrar DNS

---

## Stack do Erro

```
alembic upgrade head
  ↓
migrations/env.py:56 (run_migrations_online)
  ↓
async_engine_from_config() carrega DATABASE_URL
  ↓
asyncpg tenta conectar a "db:5432"
  ↓
DNS falha (socket.gaierror)
```

---

## Soluções Disponíveis

### Opção 1: Usar Docker Compose (Recomendado)
```bash
# Terminal 1: Inicie os containers
cd /home/dev03wsl/sila-system
docker-compose up -d

# Terminal 2: Execute migrations dentro do container
docker-compose exec backend python -m alembic upgrade head
```

### Opção 2: PostgreSQL Local (Desenv Manual)
```bash
# 1. Instale PostgreSQL localmente
sudo apt install postgresql postgresql-contrib

# 2. Inicie o serviço
sudo service postgresql start

# 3. Crie usuário e banco
sudo -u postgres createuser -P sila_user
sudo -u postgres createdb -O sila_user sila_db

# 4. Atualize .env com host local
DATABASE_URL=postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db

# 5. Execute migrations
cd /home/dev03wsl/sila-system/apps/backend
python -m alembic upgrade head
```

### Opção 3: SQLite para Desenvolvimento (Mais Rápido)
```bash
# Atualize .env
DATABASE_URL=sqlite+aiosqlite:///./test.db

# Execute migrations
python -m alembic upgrade head
```

---

## Checklist de Resolução

- [x] ✓ `.env` criado (estava faltando)
- [ ] **TODO**: Inicie PostgreSQL (Docker ou Local)
- [ ] **TODO**: Configure DATABASE_URL correto
- [ ] **TODO**: Execute `alembic upgrade head` novamente

---

## Avisos de Importação (Não-Críticos)

```
Aviso: Falha ao importar módulos de pagamento/notificações/audit/citizenship: 
       No module named 'sse_starlette'
```

Isso é apenas um warning. Será resolvido quando:
```bash
cd apps/backend
pip install -r requirements.txt  # Instala sse-starlette
```

---

## Próximos Passos

1. **Escolha uma opção** (recomendo Docker Compose)
2. **Inicie o banco de dados**
3. **Rode**: `python -m alembic upgrade head`
4. **Se passar**: Migrations estão OK
5. **Se falhar novamente**: Verifique credenciais e `socket.gaierror` desaparece

---

**Data**: 22 de Fevereiro de 2026  
**Status**: 🔴 Não Pronto → 🟢 Pronto (após seguir solução acima)
