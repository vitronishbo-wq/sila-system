# 🚀 Scripts de Orquestração do SILA System

Sistema profissional de gerenciamento e orquestração do SILA System com logging
estruturado, healthcheck inteligente e automação completa.

## 📋 Visão Geral

Este kit de ferramentas fornece quatro scripts principais para gerenciar o ciclo de vida
completo do SILA System:

1. **`sila_start.sh`** - Script mestre de inicialização (refatorado)
2. **`scripts/build_frontend.sh`** - Build e preparação do frontend
3. **`sila_stop.sh`** - Encerramento seguro da stack
4. **`status_sila.sh`** - Status e diagnóstico do sistema

## 🎯 Características Principais

### ✨ Melhorias no `sila_start.sh`

- **Logging Estruturado**: Timestamps em todas as mensagens com níveis (INFO, SUCCESS,
  WARN, ERROR, FATAL)
- **Verificação de Dependências**: Valida Docker, Docker Compose e Curl antes de iniciar
- **Healthcheck Inteligente**: Polling ativo com retry automático (60s máximo, intervalo
  de 5s)
- **Tratamento de Interrupção**: Trap para Ctrl+C com limpeza automática dos containers
- **Carregamento de Ambiente**: Exportação automática de variáveis do `.env.{mode}`
- **Integração com Scripts Auxiliares**: Chama automaticamente o build do frontend em
  modo dev

### 🏗️ Script de Build do Frontend

- Gerencia instalação de dependências Node.js
- Suporta builds de desenvolvimento e produção
- Logging estruturado consistente
- Validação de diretórios e arquivos

### 🛑 Script de Encerramento Seguro

- Verifica containers ativos antes de derrubar
- Timeout configurável (10s)
- Remove containers órfãos automaticamente
- Preserva volumes por padrão (dados persistentes)

### 🔍 Script de Status e Healthcheck

- Lista status de todos os containers
- Executa healthcheck HTTP no backend
- Verifica disponibilidade de métricas
- Testa portas de acesso (5173, 8000, 9111, 5434)
- Diagnóstico completo do sistema

## 🚀 Uso Rápido

### Iniciar o Sistema

```bash
# Modo desenvolvimento (padrão)
./sila_start.sh dev

# Modo produção
./sila_start.sh prod

# Com limpeza completa (remove volumes)
./sila_start.sh dev --clean
```

### Verificar Status

```bash
./status_sila.sh
```

### Parar o Sistema

```bash
./sila_stop.sh
```

### Build Manual do Frontend

```bash
# Desenvolvimento
bash scripts/build_frontend.sh dev

# Produção
bash scripts/build_frontend.sh prod
```

## 📊 Fluxo de Execução do `sila_start.sh`

```
1. Verificar dependências (Docker, Docker Compose, Curl)
2. Verificar arquivos essenciais (docker-compose.yml, Dockerfile, etc.)
3. Configurar ambiente (.env.{mode})
4. Garantir permissões de execução (scripts/*.sh)
5. Limpar containers antigos (opcional: --clean remove volumes)
6. Preparar frontend (apenas em dev, via scripts/build_frontend.sh)
7. Subir stack Docker Compose (--profile backend --profile frontend)
8. Healthcheck inteligente (polling HTTP com retry)
9. Validar métricas (endpoint /metrics)
10. Exibir URLs e comandos úteis
```

## 🔧 Configuração

### Variáveis de Ambiente

O sistema utiliza arquivos `.env.{mode}` para configuração:

- `.env.development` - Desenvolvimento
- `.env.production` - Produção
- `.env.staging` - Staging

### Endpoints de Healthcheck

Configurados no início do `sila_start.sh`:

```bash
SERVICE_HEALTHCHECK_URL="http://localhost:9111/health"
SERVICE_METRICS_URL="http://localhost:9111/metrics"
MAX_WAIT_SECONDS=60
WAIT_INTERVAL=5
```

## 📦 URLs de Acesso

Após inicialização bem-sucedida:

| Serviço     | URL                           | Descrição            |
| ----------- | ----------------------------- | -------------------- |
| Frontend    | http://localhost:5173         | Interface web (dev)  |
| Backend API | http://localhost:8000         | API REST             |
| API Docs    | http://localhost:8000/docs    | Documentação Swagger |
| Healthcheck | http://localhost:9111/health  | Status do backend    |
| Métricas    | http://localhost:9111/metrics | Métricas Prometheus  |
| PostgreSQL  | localhost:5434                | Banco de dados       |

## 🛡️ Tratamento de Erros

### Interrupção (Ctrl+C)

O sistema captura SIGINT/SIGTERM e executa limpeza automática:

```bash
trap cleanup_on_interrupt SIGINT SIGTERM
```

### Falha no Healthcheck

Se o backend não responder em 60 segundos:

1. Exibe logs do container backend
2. Executa `sila_stop.sh` para limpeza
3. Sai com código de erro

### Dependências Faltando

Verifica e reporta dependências ausentes:

- Docker
- Docker Compose
- Curl

## 📝 Logs Estruturados

Formato padrão de log:

```
[YYYY-MM-DD HH:MM:SS] [LEVEL] Mensagem
```

Níveis disponíveis:

- **INFO** - Informações gerais
- **SUCCESS** - Operações bem-sucedidas
- **WARN** - Avisos não críticos
- **ERROR** - Erros recuperáveis
- **FATAL** - Erros críticos (encerra execução)

## 🔄 Comandos Úteis

```bash
# Ver logs em tempo real
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f backend
docker compose logs -f frontend

# Listar containers ativos
docker compose ps

# Acessar shell do backend
docker compose exec backend bash

# Rebuild completo
./sila_start.sh dev --clean
```

## 🎨 Personalização

### Ajustar Timeout do Healthcheck

Edite as variáveis no início do `sila_start.sh`:

```bash
MAX_WAIT_SECONDS=120  # Aumentar para 2 minutos
WAIT_INTERVAL=10      # Verificar a cada 10 segundos
```

### Adicionar Novos Healthchecks

Modifique a função `check_services_health()`:

```bash
# Adicionar verificação de outro serviço
wait_for_service "http://localhost:3000/health" 60 5
```

## 🐛 Troubleshooting

### Containers não iniciam

```bash
# Ver logs detalhados
docker compose logs

# Verificar status
./status_sila.sh

# Rebuild completo
./sila_start.sh dev --clean
```

### Healthcheck falha

```bash
# Verificar se o backend está rodando
docker compose ps backend

# Ver logs do backend
docker compose logs backend

# Testar healthcheck manualmente
curl http://localhost:9111/health
```

### Permissões negadas

```bash
# Reaplicar permissões (no WSL)
wsl chmod +x sila_start.sh sila_stop.sh status_sila.sh scripts/build_frontend.sh
```

## 📚 Arquitetura

```
sila-system/
├── sila_start.sh              # Script mestre de inicialização
├── sila_stop.sh               # Encerramento seguro
├── status_sila.sh             # Status e diagnóstico
├── scripts/
│   └── build_frontend.sh      # Build do frontend
├── .env.development           # Config desenvolvimento
├── .env.production            # Config produção
└── docker-compose.yml         # Orquestração Docker
```

## 🎓 Boas Práticas

1. **Sempre use o script mestre**: `./sila_start.sh` ao invés de `docker compose up`
2. **Verifique o status regularmente**: `./status_sila.sh` para diagnóstico
3. **Use `--clean` com cautela**: Remove volumes e dados persistentes
4. **Monitore os logs**: `docker compose logs -f` durante desenvolvimento
5. **Teste healthchecks**: Valide endpoints antes de deploy

## 🔐 Segurança

- Arquivos `.env.*` devem estar no `.gitignore`
- Nunca commitar credenciais em `.env.template`
- Usar variáveis de ambiente para secrets
- Validar permissões de execução dos scripts

## 📈 Próximos Passos

- [ ] Adicionar suporte a múltiplos ambientes (staging, qa)
- [ ] Implementar backup automático antes de `--clean`
- [ ] Adicionar métricas de performance no status
- [ ] Criar script de rollback automático
- [ ] Integrar com CI/CD pipelines

---

**Versão**: 4.0 **Última Atualização**: 2025-01-05 **Autor**: SILA System Team
