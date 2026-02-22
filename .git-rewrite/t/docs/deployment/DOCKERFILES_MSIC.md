# 📦 Organização de Dockerfiles - MSIC

## Metodologia SILA de Intercâmbio de Configurações (MSIC)

### 🎯 Objetivo

Centralizar configurações Docker mantendo performance e simplicidade.

### 📁 Estrutura Atual

```
sila-system/
├── Dockerfile.backend      # ✅ Referência centralizada (backup)
├── Dockerfile.frontend     # ✅ Referência centralizada (backup)
├── .dockerignore          # ✅ Otimização de contexto
├── backend/
│   └── Dockerfile         # 🔥 Dockerfile ativo (contexto otimizado)
└── frontend/
    └── apps/web/
        └── Dockerfile.smart  # 🔥 Dockerfile ativo (contexto otimizado)
```

### 🔄 Abordagem Híbrida

**Por que não centralizamos 100% na raiz?**

1. **Performance**: Contextos específicos são mais rápidos (72MB vs 659MB+)
2. **Cache**: Docker cache funciona melhor com contextos menores
3. **Simplicidade**: Cada serviço tem suas dependências isoladas

**O que centralizamos?**

1. **`.dockerignore`**: Regras globais de exclusão na raiz
2. **`docker-compose.yml`**: Orquestração centralizada
3. **Backups**: `Dockerfile.backend` e `Dockerfile.frontend` como referência

### 📋 Configuração do docker-compose.yml

```yaml
services:
  backend:
    build:
      context: ./backend # Contexto específico
      dockerfile: Dockerfile # Dockerfile local

  frontend:
    build:
      context: ./frontend # Contexto específico
      dockerfile: apps/web/Dockerfile.smart # Dockerfile local
```

### ✅ Vantagens

- ⚡ **Build rápido**: Contextos menores
- 💾 **Cache eficiente**: Menos invalidação
- 🎯 **Isolamento**: Cada serviço independente
- 📦 **Backup centralizado**: Dockerfiles na raiz como referência
- 🔧 **Fácil manutenção**: Mudanças locais não afetam outros serviços

### 🚀 Como Usar

#### Desenvolvimento

```bash
./sila_start.sh dev
```

#### Produção

```bash
docker compose --profile backend --profile frontend up -d
```

#### Rebuild específico

```bash
# Backend
docker compose build backend

# Frontend
docker compose build frontend
```

### 📝 Notas

- Os Dockerfiles na raiz (`Dockerfile.backend`, `Dockerfile.frontend`) servem como
  **backup e referência**
- Para mudanças, edite os Dockerfiles nos diretórios específicos
- O `.dockerignore` na raiz aplica-se a todos os builds
- Esta abordagem segue as melhores práticas Docker mantendo a filosofia MSIC

### 🔄 Sincronização

Se precisar sincronizar os Dockerfiles:

```bash
# Copiar do backend para raiz
cp backend/Dockerfile Dockerfile.backend

# Copiar do frontend para raiz
cp frontend/apps/web/Dockerfile.smart Dockerfile.frontend
```

---

**Última atualização**: 2025-11-07 **Versão MSIC**: 2.0 **Status**: ✅ Implementado e
testado
