# ⚡ SILA NGINX - Cheat Sheet (Referência Rápida)

## 🚀 Commandos Essenciais (Copy & Paste)

### Para Leigos - Primeiros Passos

```bash
# 1. Verificar se tudo está ok
bash nginx_automation.sh --diagnose

# 2. Configurar (escolha UMA opção)
# Opção A: Automático (RECOMENDADO)
bash nginx_automation.sh --auto

# Opção B: Apenas gerar config (para revisar)
bash nginx_automation.sh --generate

# 3. Verificar resultado
bash nginx_automation.sh --status-report

# 4. Testar
curl http://localhost/health
```

---

### Para Técnicos - Operações Comuns

```bash
# Ver todos os serviços detectados
bash nginx_automation.sh --list-services

# Validar nginx.conf
bash nginx_automation.sh --validate-config

# Testar proxy para backend
bash nginx_automation.sh --test-proxy

# Diagnóstico verboso
bash nginx_automation.sh --diagnose --verbose

# Ver relatório completo
bash nginx_automation.sh --status-report

# Deploy completo
bash nginx_automation.sh --full-deploy --env production

# Limpeza (parar/remover container)
bash nginx_automation.sh --clean

# Ver configuração gerada
cat infrastructure/docker/nginx.conf

# Ver últimos logs
tail -50 logs/nginx_automation_*.log
```

---

## 🔧 Variáveis de Ambiente (Atalhos)

```bash
# Mudar porta do Nginx
NGINX_PORT=8080 bash nginx_automation.sh --auto

# Mudar para produção
ENVIRONMENT=production bash nginx_automation.sh --auto

# Múltiplas (separadas por espaço)
NGINX_PORT=8080 ENVIRONMENT=staging bash nginx_automation.sh --full-deploy

# Consulta de variáveis suportadas
ENVIRONMENT=dev         # dev, staging, prod (padrão: dev)
BACKEND_PORT=8000       # porta backend (padrão: 8000)
FRONTEND_PORT=5173      # porta frontend (padrão: 5173)
NGINX_PORT=80           # porta nginx (padrão: 80)
```

---

## 📁 Arquivos Chave

```
infrastructure/docker/nginx.conf              # Config gerada
infrastructure/docker/nginx.conf.backup.*     # Backups automáticos
logs/nginx_automation_YYYYMMDD_HHMMSS.log    # Logs detalhados
NGINX_AUTOMATION_GUIDE.md                     # Documentação completa
```

---

## 🐳 Docker - Comandos Relacionados

```bash
# Ver se nginx está rodando
docker ps | grep nginx

# Ver logs do nginx
docker logs sila-nginx

# Parar nginx
docker stop sila-nginx

# Remover nginx
docker rm sila-nginx

# Ver logs em tempo real
docker logs -f sila-nginx

# Acessar shell do container (debug)
docker exec -it sila-nginx sh
```

---

## 🔍 Health Checks

```bash
# Nginx está saudável?
curl http://localhost/health
# Esperado: "healthy"

# JSON (dev mode)
curl http://localhost/health/nginx
# Esperado: {"status": "healthy", ...}

# Backend através do proxy?
curl http://localhost/api/health
```

---

## 🐛 Quick Fixes

| Problema          | Comando                                                                              |
| ----------------- | ------------------------------------------------------------------------------------ |
| Nginx não inicia  | `bash nginx_automation.sh --clean && bash nginx_automation.sh --auto`                |
| Config inválida   | `bash nginx_automation.sh --validate-config`                                         |
| Ver erros         | `tail -100 logs/nginx_automation_*.log \| grep "❌"`                                 |
| Backup anterior   | `ls infrastructure/docker/nginx.conf.backup.*`                                       |
| Restaurar backup  | `cp infrastructure/docker/nginx.conf.backup.NUMERO infrastructure/docker/nginx.conf` |
| Logs do container | `docker logs sila-nginx \| tail -50`                                                 |
| Teste de proxy    | `bash nginx_automation.sh --test-proxy`                                              |

---

## 📊 Estrutura de Diretórios (Automaticamente Detectada)

```
✅ Backend detectado em:     apps/backend/
✅ Frontend detectado em:    apps/frontend/
✅ API Gateway (opcional):   apps/api_gateway/
✅ Worker (opcional):        apps/worker/
```

---

## 🎯 Fluxo Recomendado

```
1. bash nginx_automation.sh --diagnose
   ↓
2. bash nginx_automation.sh --auto
   ↓
3. curl http://localhost/health
   ↓
4. Sucesso! 🎉
```

---

## 📝 O que é Gerado Automaticamente

```nginx
✅ Compression (gzip)           - Reduz tráfego 70%
✅ Cache inteligente            - 1 ano para assets versionados
✅ Security headers             - XSS, Clickjacking, etc
✅ Rate limiting                - Anti brute-force no login
✅ Proxy para /api/             - Conecta ao backend
✅ SPA fallback                 - Rotas vão para index.html
✅ Health check endpoints       - /health, /health/nginx
```

---

## 🚨 Modo Debug

```bash
# Ver tudo que o script faz
bash nginx_automation.sh --diagnose --verbose

# Ver mais detalhes nos logs
grep -E "(✅|⚠️|❌)" logs/nginx_automation_*.log

# Debug do container
docker exec -it sila-nginx nginx -T
```

---

## 📞 Resumo Rápido

| O que fazer             | Comando                                                   |
| ----------------------- | --------------------------------------------------------- |
| **Setup inicial**       | `bash nginx_automation.sh --auto`                         |
| **Apenas gerar config** | `bash nginx_automation.sh --generate`                     |
| **Verificar tudo**      | `bash nginx_automation.sh --diagnose`                     |
| **Ver status**          | `bash nginx_automation.sh --status-report`                |
| **Validar config**      | `bash nginx_automation.sh --validate-config`              |
| **Ver serviços**        | `bash nginx_automation.sh --list-services`                |
| **Deploy prod**         | `bash nginx_automation.sh --full-deploy --env production` |
| **Parar nginx**         | `bash nginx_automation.sh --clean`                        |
| **Ver ajuda**           | `bash nginx_automation.sh --help`                         |

---

**Última atualização**: Novembro 2025 | **Versão**: 2.0
