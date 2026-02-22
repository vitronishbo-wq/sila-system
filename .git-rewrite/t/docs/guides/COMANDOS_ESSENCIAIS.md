# 🚀 SILA - Comandos Essenciais

## 📋 **Comandos Principais**

### 🐳 **Docker & Desenvolvimento**

```bash
# Iniciar sistema completo
./start_enterprise.sh --frontend

# Desenvolvimento com hot reload
docker compose up -d

# Parar todos os containers
docker compose down

# Rebuild completo
./start_enterprise.sh --rebuild --frontend

# Ver logs
docker compose logs -f backend
docker compose logs -f frontend
```

### 🔧 **Scripts de Correção**

```bash
# Correção automática completa
./repair_all_simple.sh

# Correção apenas do frontend
./scripts/fix-frontend.sh

# Correção apenas do backend
./scripts/fix-backend.sh

# Gerar tipos TypeScript
./scripts/generate-types.sh
```

### 🗄️ **Banco de Dados**

```bash
# Aplicar migrações
docker exec sila-backend alembic upgrade head

# Criar nova migração
docker exec sila-backend alembic revision --autogenerate -m "descrição"

# Ver histórico de migrações
docker exec sila-backend alembic history
```

### 👤 **Usuários & Admin**

```bash
# Criar usuário admin
docker exec sila-backend python scripts/create_admin.py

# Listar usuários
docker exec sila-backend python -c "
from modules.auth.models import User
from database import get_db
db = next(get_db())
users = db.query(User).all()
for u in users: print(f'{u.id}: {u.email} - {u.role}')
"
```

### 📊 **Monitoramento**

```bash
# Ver métricas
curl http://localhost:9111/metrics

# Health check
curl http://localhost:9111/health

# Status dos containers
docker compose ps

# Uso de recursos
docker stats
```

### 🧪 **Testes**

```bash
# Testes do backend
docker exec sila-backend pytest

# Testes específicos
docker exec sila-backend pytest tests/test_auth.py

# Coverage
docker exec sila-backend pytest --cov=modules
```

### 🌐 **URLs Importantes**

- **Frontend**: http://localhost
- **Frontend Dev**: http://localhost:5173 (com hot reload)
- **Backend API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Métricas**: http://localhost:9111/metrics
- **Health**: http://localhost:9111/health
- **PostgreSQL**: localhost:5434

### 🔍 **Diagnóstico**

```bash
# Verificar se tudo está funcionando
curl -f http://localhost:8000/health
curl -f http://localhost/
curl -f http://localhost:9111/health

# Ver configuração do Docker
docker compose config

# Inspecionar container
docker exec -it sila-backend bash
docker exec -it sila-frontend sh
```

### 📦 **Dependências**

```bash
# Instalar dependências do backend
docker exec sila-backend pip install -r requirements.txt

# Instalar dependências do frontend
docker exec sila-frontend npm install

# Atualizar dependências
docker compose build --no-cache
```

---

## 🎯 **Comandos por Cenário**

### 🚀 **Primeiro Setup**

```bash
1. ./repair_all_simple.sh
2. docker compose up -d
3. ./scripts/generate-types.sh
```

### 🔄 **Desenvolvimento Diário**

```bash
1. docker compose up -d
2. # Desenvolver...
3. docker compose logs -f backend  # Ver logs
```

### 🐛 **Resolução de Problemas**

```bash
1. docker compose down
2. ./repair_all_simple.sh
3. docker compose up -d --build
```

### 🚢 **Deploy Produção**

```bash
1. ./start_enterprise.sh --rebuild --frontend
2. # Verificar saúde dos serviços
3. curl -f http://localhost:8000/health
```

---

**📝 Nota**: Este arquivo substitui todos os comandos antigos e obsoletos.
