# 📖 Guia Completo - SILA NGINX Automation

## Visão Geral

O script `nginx_automation.sh` foi redesenhado para oferecer:

✅ **Compatibilidade total** com a nova estrutura (`apps/backend`, `apps/frontend`) ✅
**Geração dinâmica** de configuração Nginx baseada em serviços detectados ✅
**Documentação dupla** - leigos e técnicos ✅ **Validação inteligente** de configuração
✅ **Deploy automatizado** com segurança

---

## 🚀 Quick Start (Para Leigos)

### Passo 1: Verificar problemas

```bash
bash nginx_automation.sh --diagnose
```

### Passo 2: Configurar automaticamente

```bash
bash nginx_automation.sh --auto
```

Pronto! Seu Nginx deve estar rodando em `http://localhost:80`

### Passo 3 (Opcional): Visualizar configuração

```bash
cat infrastructure/docker/nginx.conf
```

---

## 📋 Referência Completa de Comandos

### Operações Básicas

#### `--help` - Ver todas as opções

```bash
bash nginx_automation.sh --help
```

#### `--diagnose` - Verificar se tudo está ok

```bash
bash nginx_automation.sh --diagnose
```

Verifica:

- Diretórios de backend e frontend
- Arquivo nginx.conf
- Disponibilidade do Docker
- Serviços detectados

#### `--auto` - Configuração completa automatizada

```bash
bash nginx_automation.sh --auto
```

O que faz:

1. Detecta serviços disponíveis
2. Gera nginx.conf dinamicamente
3. Valida a configuração
4. Inicia container Nginx
5. Testa o proxy

**Recomendado para primeiros usos!**

---

### Operações de Geração

#### `--generate` - Gerar apenas nginx.conf

```bash
bash nginx_automation.sh --generate
```

Gera arquivo sem fazer deploy. Bom para revisar antes de aplicar.

#### `--generate --env production` - Gerar para produção

```bash
bash nginx_automation.sh --generate --env production
```

Adaoca configuração para ambiente de produção.

---

### Operações de Validação

#### `--validate-config` - Verificar se nginx.conf é válido

```bash
bash nginx_automation.sh --validate-config
```

Usa Docker para validar sintaxe com nginx:alpine.

#### `--test-proxy` - Testar comunicação

```bash
bash nginx_automation.sh --test-proxy
```

Simula requisições para validar funcionamento.

---

### Operações de Diagnóstico

#### `--list-services` - Ver serviços detectados

```bash
bash nginx_automation.sh --list-services
```

Mostra:

- Backend (FastAPI)
- Frontend (React/Vite)
- API Gateway (se existir)
- Worker (se existir)

#### `--status-report` - Relatório completo do sistema

```bash
bash nginx_automation.sh --status-report
```

---

### Operações Avançadas

#### `--full-deploy --env production` - Deploy completo

```bash
bash nginx_automation.sh --full-deploy --env production
```

Deploy robusto com:

1. Diagnóstico completo
2. Geração de config
3. Validação
4. Inicialização do Nginx

#### `--clean` - Limpeza

```bash
bash nginx_automation.sh --clean
```

Para e remove container Nginx.

---

## 🔧 Variáveis de Ambiente

Configure portas e ambiente via variáveis:

```bash
# Mudar porta do Nginx (padrão: 80)
NGINX_PORT=8080 bash nginx_automation.sh --auto

# Mudar porta do backend (padrão: 8000)
BACKEND_PORT=9000 bash nginx_automation.sh --generate

# Especificar ambiente
ENVIRONMENT=staging bash nginx_automation.sh --auto

# Múltiplas variáveis
NGINX_PORT=8080 ENVIRONMENT=production bash nginx_automation.sh --full-deploy
```

**Variáveis disponíveis:**

- `ENVIRONMENT` - dev, staging, prod (padrão: dev)
- `BACKEND_PORT` - porta backend (padrão: 8000)
- `FRONTEND_PORT` - porta frontend (padrão: 5173)
- `NGINX_PORT` - porta Nginx (padrão: 80)

---

## 📁 Estrutura de Arquivos

```
sila-system/
├── apps/
│   ├── backend/           ← FastAPI
│   ├── frontend/          ← React/Vite
│   ├── api_gateway/       ← (opcional)
│   └── worker/            ← (opcional)
├── infrastructure/
│   └── docker/
│       ├── nginx.conf              ← Gerado automaticamente
│       ├── nginx.conf.backup.*     ← Backups automáticos
│       └── docker-compose.dev.yml
├── nginx_automation.sh             ← Script principal
└── logs/
    └── nginx_automation_*.log      ← Logs detalhados
```

---

## 🔍 Leitura de Logs

### Localização

```bash
# Logs salvos em:
logs/nginx_automation_YYYYMMDD_HHMMSS.log
```

### Exemplos de uso

```bash
# Ver últimos logs
tail -f logs/nginx_automation_*.log

# Ver tudo
cat logs/nginx_automation_*.log | less

# Filtrar erros
grep "❌" logs/nginx_automation_*.log
```

---

## 📝 Nginx.conf Gerado - O que Há Dentro

### 1. Performance (Automática)

```nginx
# Compression - reduz tráfego em ~70%
gzip on;
gzip_comp_level 6;

# Keep-alive - mantém conexões abertas
keepalive_timeout 65;

# Buffering - otimiza memória
proxy_buffering off;
```

### 2. Segurança (Automática)

```nginx
# Headers de segurança
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block

# CSP - Previne XSS
Content-Security-Policy: default-src 'self'; ...

# Rate Limiting - anti-brute-force
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
```

### 3. Caching Inteligente (Automática)

```nginx
# Assets versionados (main.abc123.js) - cache 1 ano
location ~* \.(js|css|png|jpg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# HTML - cache 1 hora (permite updates)
location ~* \.html$ {
    expires 1h;
}
```

### 4. Proxy para Backend (Automática)

```nginx
location /api/ {
    proxy_pass http://backend:8000/;

    # Headers necessários
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 5. SPA Fallback (Automática)

```nginx
# Todas as rotas conhecidas vão para index.html
location / {
    try_files $uri $uri/ /index.html;
}
```

---

## 🐳 Integração Docker

### Dockerfile esperado

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY dist /usr/share/nginx/html
EXPOSE 80
```

### Docker Compose

O script cria container automaticamente:

```bash
docker run -d \
  --name sila-nginx \
  -p 80:80 \
  -v nginx.conf:/etc/nginx/nginx.conf:ro \
  -v apps/frontend/dist:/usr/share/nginx/html:ro \
  --network sila-network \
  nginx:alpine
```

---

## 🐛 Troubleshooting

### Problema: "nginx.conf é inválido"

```bash
# Verificar erros
docker run --rm -v $(pwd)/infrastructure/docker/nginx.conf:/etc/nginx/nginx.conf nginx:alpine nginx -t

# Ver arquivo
cat infrastructure/docker/nginx.conf
```

### Problema: Container não inicia

```bash
# Verificar logs do container
docker logs sila-nginx

# Parar e reiniciar
bash nginx_automation.sh --clean
bash nginx_automation.sh --auto
```

### Problema: Backend não responde em /api/

```bash
# 1. Verificar se backend está rodando
docker ps | grep backend

# 2. Testar conexão
curl http://localhost:8000/health

# 3. Ver logs do nginx
docker logs sila-nginx | tail -50
```

### Problema: Página em branco no navegador

```bash
# 1. Verificar se frontend está servido
curl http://localhost/
```

# 2. Verificar console do navegador para erros

# 3. Limpar cache: Ctrl+Shift+Delete

````

---

## 🔐 Segurança

### Rate Limiting automático

```nginx
# API - 10 requisições/segundo
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

# Login - 5 requisições/minuto (anti brute-force)
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
````

### Headers de Segurança

```nginx
X-Frame-Options: SAMEORIGIN          # Evita clickjacking
X-Content-Type-Options: nosniff       # Evita MIME sniffing
X-XSS-Protection: 1; mode=block       # XSS Protection
Content-Security-Policy: ...          # CSP contra XSS
```

---

## 📊 Monitoramento

### Health Check endpoints

```bash
# Verificar Nginx está saudável
curl http://localhost/health
# Resposta: "healthy"

# Para JSON (dev)
curl http://localhost/health/nginx
# Resposta: {"status": "healthy", "service": "nginx", ...}
```

### Ver configuração (Dev)

```bash
# Verificar se config foi carregada corretamente
curl http://localhost:9999/nginx-config
```

---

## 🚀 Exemplos de Uso Completo

### Exemplo 1: Setup Inicial

```bash
cd /caminho/para/sila-system

# 1. Verificar se tudo está ok
bash nginx_automation.sh --diagnose

# 2. Se ok, fazer setup automático
bash nginx_automation.sh --auto

# 3. Verificar se está rodando
curl http://localhost/
```

### Exemplo 2: Deploy em Produção

```bash
# Setup com variáveis de produção
ENVIRONMENT=production NGINX_PORT=443 bash nginx_automation.sh --full-deploy

# Validar
bash nginx_automation.sh --validate-config

# Ver status
bash nginx_automation.sh --status-report
```

### Exemplo 3: Apenas Gerar Config (Revisar antes)

```bash
# Gerar arquivo
bash nginx_automation.sh --generate --env staging

# Revisar
cat infrastructure/docker/nginx.conf | less

# Validar
bash nginx_automation.sh --validate-config

# Se ok, fazer deploy
bash nginx_automation.sh --auto
```

---

## 📝 Backups Automáticos

Cada vez que o script gera um novo `nginx.conf`, o anterior é salvo:

```bash
# Ver backups
ls -la infrastructure/docker/nginx.conf.backup.*

# Restaurar um backup
cp infrastructure/docker/nginx.conf.backup.1234567890 infrastructure/docker/nginx.conf

# Fazer deploy com backup
bash nginx_automation.sh --auto
```

---

## 🎯 Próximas Etapas

1. **Setup Inicial**: Rode `bash nginx_automation.sh --auto`
2. **Teste**: Acesse `http://localhost` no navegador
3. **Monitore**: Verifique logs: `tail -f logs/nginx_automation_*.log`
4. **Customize**: Edite `infrastructure/docker/nginx.conf` conforme necessário
5. **Redeploy**: Execute `bash nginx_automation.sh --auto` novamente

---

## 📞 Suporte

### Documentação

- Arquivo: `NGINX_AUTOMATION_GUIDE.md` (este arquivo)
- Script: `nginx_automation.sh --help`

### Logs

- Detalhados em: `logs/nginx_automation_*.log`
- Busque por ✅ (sucesso) ou ❌ (erro)

### Teste rápido

```bash
# Diagnóstico completo
bash nginx_automation.sh --diagnose

# Relatório de status
bash nginx_automation.sh --status-report
```

---

**Última atualização**: Novembro 2025 **Versão**: 2.0 (Otimizado para nova estrutura)
**Compatibilidade**: Linux/WSL, macOS
