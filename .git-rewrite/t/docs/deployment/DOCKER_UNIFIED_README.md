# 🚀 SILA System - Docker Compose Unificado v3.0

Sistema Docker inteligente e unificado para desenvolvimento e produção do SILA System.

## ✨ Recursos

- **🔥 Hot Reload**: Desenvolvimento automático para frontend e backend
- **🏭 Produção**: Build otimizado com Nginx e workers
- **📊 Monitoring**: Servidor de métricas integrado
- **🗄️ PostgreSQL**: Banco persistente com inicialização automática
- **🔄 Redis**: Cache opcional (via profile)
- **🛡️ Segurança**: Configurações separadas dev/prod
- **📱 Monorepo**: Suporte completo ao workspace frontend

## 🎯 Início Rápido

### 1. Desenvolvimento (Hot Reload)

```bash
# Iniciar tudo em modo desenvolvimento
./start_sila.sh dev

# Ou manualmente
export FRONTEND_TARGET=dev
export NODE_ENV=development
docker compose up --build
```

### 2. Produção

```bash
# Iniciar em modo produção (background)
./start_sila.sh prod

# Ou manualmente
export FRONTEND_TARGET=runtime
export NODE_ENV=production
docker compose up --build -d
```

### 3. Com Cache Redis

```bash
# Ativar Redis junto com os serviços
docker compose --profile cache up --build
```

## 🌐 URLs Disponíveis

### Desenvolvimento

- **Frontend (Dev)**: http://localhost:5173
- **Frontend (Prod)**: http://localhost:80
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Metrics**: http://localhost:9111/metrics
- **Database**: localhost:5434

### Produção

- **Frontend**: http://localhost:80
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Metrics**: http://localhost:9111/metrics
- **Database**: localhost:5434

## 📁 Estrutura de Arquivos

```
sila-system/
├── docker-compose.yml          # 🆕 Compose unificado
├── start_sila.sh              # 🆕 Script inteligente
├── backend/
│   ├── Dockerfile             # Backend (existente)
│   ├── entrypoint.sh          # 🔄 Atualizado com hot reload
│   └── scripts/
│       └── init-db.sql        # 🆕 Inicialização automática do DB
└── frontend/
    └── apps/web/
        ├── Dockerfile         # Frontend original
        └── Dockerfile.smart   # 🆕 Multi-target (dev/prod/metrics)
```

## ⚙️ Configuração

### Variáveis de Ambiente Principais

```bash
# Modo
ENVIRONMENT=development|production
NODE_ENV=development|production

# Frontend Target
FRONTEND_TARGET=dev|runtime

# Portas
BACKEND_PORT=8000
FRONTEND_PORT=80
FRONTEND_DEV_PORT=5173
DB_PORT=5434
METRICS_PORT=9111
```

### Copiar Configuração

```bash
cp .env.example .env
# Editar .env conforme necessário
```

## 🛠️ Comandos Úteis

```bash
# Ver status dos containers
docker compose ps

# Ver logs em tempo real
docker compose logs -f

# Logs de serviço específico
docker compose logs -f backend

# Parar tudo
docker compose down

# Reconstruir imagem
docker compose build --no-cache

# Limpar volumes (cuidado!)
docker compose down -v
```

## 🏗️ Dockerfile Targets

### Frontend (Dockerfile.smart)

- **dev**: Servidor Vite com hot reload
- **runtime**: Nginx com build otimizado
- **metrics**: Servidor de métricas Prometheus

### Backend

- **development**: uvicorn com --reload
- **production**: uvicorn com --workers 4

## 📊 Monitoring

O sistema inclui um servidor de métricas que expõe:

- **Requests totais**: Contador de requisições
- **Uptime**: Tempo de funcionamento
- **Memory usage**: Uso de memória

Acesse: http://localhost:9111/metrics

## 🗄️ Banco de Dados

O PostgreSQL é inicializado automaticamente com:

- ✅ Extensões UUID e pg_trgm
- ✅ Schema sila_system
- ✅ Tabelas básicas (users, audit_logs)
- ✅ Usuário admin padrão
- ✅ Índices otimizados
- ✅ Triggers para timestamps

**Acesso padrão:**

- Host: localhost:5434
- Database: sila_db
- User: postgres
- Password: postgres

## 🔧 Troubleshooting

### Portas em uso

```bash
# Verificar portas
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173

# Matar processo em porta
sudo fuser -k 8000/tcp
```

### Permissões (Windows)

```powershell
# Tornar script executável
icacls start_sila.sh /grant:r Everyone:RX
```

### Rebuild completo

```bash
# Limpar tudo e reconstruir
docker compose down -v --remove-orphans
docker system prune -f
./start_sila.sh dev --backup
```

## 🚀 Scripts Automáticos

### start_sila.sh

Script inteligente que:

- 🔍 Detecta modo dev/prod automaticamente
- 📦 Cria backup das configurações
- ✅ Verifica dependências
- 🧹 Limpa containers antigos
- 🚀 Inicia serviços
- 📋 Mostra URLs úteis

```bash
# Auto-detectar modo
./start_sila.sh

# Forçar modo
./start_sila.sh dev
./start_sila.sh prod

# Com backup
./start_sila.sh dev --backup

# Ajuda
./start_sila.sh --help
```

## 🎯 Próximos Passos

1. ✅ Docker compose unificado
2. ✅ Hot reload inteligente
3. ✅ Monitoring integrado
4. ✅ Script de automação
5. 🔄 CI/CD integration
6. 🔄 Kubernetes deployment
7. 🔄 Advanced monitoring

---

**SILA System v3.0** - Docker Compose Unificado e Inteligente 🚀
