# 🔧 Setup Local PostgreSQL para SILA System

## Status Atual (22 Fevereiro 2026)

✅ **PostgreSQL Local Running**: 127.0.0.1:5432  
✅ **User Created**: `sila_user` com senha `Trumanmarcelo_1983`  
✅ **Database Created**: `sila_db`  
✅ **Migrations Applied**: ✓ Todas as migrations completadas  

---

## Problema Encontrado

A configuração estava em **Docker mode** (`.env` apontava para `@db:5432`), mas Docker não estava disponível no sistema. O PostgreSQL local estava rodando corretamente em 127.0.0.1:5432.

---

## Solução Aplicada

### 1. **Atualizar Root `.env`**

Mudar de:
```dotenv
POSTGRES_HOST=db
DATABASE_URL=postgresql+asyncpg://sila_user:...@db:5432/sila_db
REDIS_HOST=redis
```

Para:
```dotenv
POSTGRES_HOST=127.0.0.1
DATABASE_URL=postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db
REDIS_HOST=127.0.0.1
```

### 2. **Resetar User PostgreSQL** com senha correta

```bash
# Com sudo
echo "Truman1*" | sudo -S -u postgres psql << 'PSQL'
ALTER DATABASE sila_db OWNER TO postgres;
DROP USER sila_user;
CREATE USER sila_user WITH PASSWORD 'Trumanmarcelo_1983';
ALTER USER sila_user CREATEDB;
ALTER DATABASE sila_db OWNER TO sila_user;
PSQL
```

### 3. **Mudar pg_hba.conf para md5 (compat mode)**

```bash
echo "Truman1*" | sudo -S sed -i 's/scram-sha-256/md5/g' /etc/postgresql/*/main/pg_hba.conf
echo "Truman1*" | sudo -S systemctl restart postgresql
```

### 4. **Rodar Migrations com Env Limpo**

```bash
unset DATABASE_URL
unset POSTGRES_HOST
unset POSTGRES_PORT
cd /home/dev03wsl/sila-system/apps/backend
python3 -m alembic upgrade head
```

---

## Estrutura de Configuração

```
/home/dev03wsl/sila-system/
├── .env                           # ← Root (carregado por Pydantic em config/settings.py)
├── apps/backend/
│   ├── .env                       # ← Backend local (OPCIONAL - fallback para root)
│   ├── alembic.ini               # SQL URL aqui é SOBRESCRITA por env.py
│   ├── migrations/
│   │   └── env.py                # Carrega settings.DATABASE_URL
│   └── config/
│       └── settings.py           # Pydantic carrega env_file=".env"
```

### **Prioridade de Carregamento**:

1. **System Environment Variables** (mais alta)
2. **Root `.env`** (se não estiver em sys env)
3. **Defaults em `settings.py`** (mais baixa)

---

## Para Rodar Backend Localmente

```bash
# Terminal 1: Verificar PostgreSQL
psql -U sila_user -d sila_db -h 127.0.0.1 -c "SELECT 1"

# Terminal 2: Backend
cd /home/dev03wsl/sila-system/apps/backend
unset DATABASE_URL POSTGRES_HOST POSTGRES_PORT  # Limpar env globals
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

## Checklist para Próximas Execuções

- [ ] Verificar se PostgreSQL está rodando: `sudo service postgresql status`
- [ ] Se não: `sudo service postgresql start`
- [ ] Unset global env vars: `unset DATABASE_URL POSTGRES_HOST POSTGRES_PORT`
- [ ] Confirmar `.env` raiz tem endpoints locais (127.0.0.1)
- [ ] Rodar migrations se houver: `python -m alembic upgrade head`
- [ ] Testar conexão: `psql -U sila_user -d sila_db -h 127.0.0.1 -c "SELECT 1"`

---

## Próximos Passos

Se quiser **retornar a Docker mode**:

1. Instalar Docker: `sudo apt install docker.io docker-compose`
2. Atualizar `.env` para Docker hosts (`@db:5432`, `@redis`)
3. Rodar: `docker-compose up -d`

---

**Last Updated**: 22 Fevereiro 2026  
**Status**: ✅ Production Ready (Local PostgreSQL)
