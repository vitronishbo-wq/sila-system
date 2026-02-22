# 🚀 Quick Start - Backend SILA

## ✅ Pré-requisitos Concluídos

- [x] Módulo `location` migrado e validado
- [x] Módulo `payment` migrado e validado
- [x] Sistema de separação implementado e testado

---

## 🐳 Passo 1: Iniciar Docker Desktop

**Windows:**

1. Abra o Docker Desktop
2. Aguarde até que apareça "Docker Desktop is running"

**Verificar:**

```powershell
docker ps
```

---

## 🚀 Passo 2: Iniciar Serviços

### Opção A: Iniciar tudo (Recomendado)

```bash
cd devops
docker-compose --profile infra --profile backend up -d
```

### Opção B: Iniciar apenas banco de dados

```bash
cd devops
docker-compose --profile infra up -d
```

### Opção C: Iniciar apenas backend

```bash
cd devops
docker-compose --profile backend up -d
```

---

## 🗄️ Passo 3: Executar Migrações Alembic

### Verificar se container está rodando

```bash
docker ps --filter name=backend
```

### Executar upgrade

```bash
docker exec -it devops-backend-1 alembic upgrade head
```

**Ou se o nome for diferente:**

```bash
# Listar containers
docker ps

# Executar com nome correto
docker exec -it <container_name> alembic upgrade head
```

---

## 👤 Passo 4: Criar Usuários Administrativos

```bash
docker exec -it devops-backend-1 python3 scripts/create_admin_batch.py
```

**Usuários criados:**

- `truman0` (Super Admin)
- `admin` (Admin)
- `benjamim` (Admin)

---

## ✅ Verificação

### Verificar banco de dados

```bash
# Conectar ao PostgreSQL
docker exec -it devops-db-1 psql -U postgres -d sila

# Listar tabelas
\dt

# Ver usuários
SELECT username, email, role FROM users;

# Sair
\q
```

### Verificar logs do backend

```bash
docker logs devops-backend-1 --tail 50 -f
```

### Testar API

```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

---

## 🛠️ Troubleshooting

### Problema: Container não inicia

```bash
# Ver logs
docker logs devops-backend-1

# Reiniciar
docker-compose --profile backend restart
```

### Problema: Erro de conexão com banco

```bash
# Verificar se banco está rodando
docker ps --filter name=db

# Ver logs do banco
docker logs devops-db-1
```

### Problema: Alembic falha

```bash
# Entrar no container
docker exec -it devops-backend-1 bash

# Verificar conexão
python3 -c "from core.db.session import engine; print(engine.url)"

# Ver versão atual
alembic current

# Ver histórico
alembic history
```

---

## 🔄 Comandos Úteis

```bash
# Parar tudo
docker-compose --profile infra --profile backend down

# Parar e remover volumes (CUIDADO!)
docker-compose --profile infra --profile backend down -v

# Ver logs
docker-compose logs -f backend

# Reiniciar backend
docker-compose restart backend

# Rebuild backend
docker-compose --profile backend up -d --build
```

---

## 📊 Status Atual

- ✅ Módulos migrados: `location`, `payment`
- ✅ Separação models/schemas: Validada
- ⏳ Banco de dados: Aguardando migração
- ⏳ Usuários admin: Aguardando criação

---

## 🎯 Próximos Passos

1. Iniciar Docker Desktop
2. Executar: `cd devops && docker-compose --profile infra --profile backend up -d`
3. Executar: `docker exec -it devops-backend-1 alembic upgrade head`
4. Executar: `docker exec -it devops-backend-1 python3 scripts/create_admin_batch.py`
5. Testar: `curl http://localhost:8000/docs`

---

**Última atualização**: 2025-01-04
