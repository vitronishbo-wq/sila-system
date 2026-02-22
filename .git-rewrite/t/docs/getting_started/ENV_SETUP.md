# 🔧 Configuração de Ambiente - SILA System

## Ficheiros Gerados

Foram criados automaticamente os seguintes ficheiros de configuração:

### Templates (commitados)

- `.env.example` - Template principal com todas as variáveis
- `devops/.env.example` - Template para Docker Compose
- `apps/backend/config/.env.example` - Template específico do backend

### Configurações Geradas (NÃO commitadas)

- `.env.development` - Configuração de desenvolvimento (valores seguros para dev)
- `.env.production` - Configuração de produção (com segredos gerados)
- `apps/backend/config/.env.development` - Backend dev
- `apps/backend/config/.env.production` - Backend prod
- `devops/.env.development` - DevOps dev
- `devops/.env.production` - DevOps prod

## 🚀 Como Usar

### 1. Desenvolvimento

Os ficheiros `.env.development` já têm valores seguros para desenvolvimento local:

- Passwords simples (ex: `dev_password_123`)
- Debug ativado
- Rate limiting desativado
- Monitoring opcional

### 2. Produção

Os ficheiros `.env.production` têm:

- ✅ **Segredos gerados automaticamente** (SECRET*KEY, JWT*\*, passwords)
- ⚠️ **Valores a substituir manualmente** (marcados com `PROD_*_CHANGE_ME`)

**Valores que DEVES substituir em produção:**

```bash
# APIs externas
BNA_API_KEY=PROD_BNA_API_KEY_CHANGE_ME
MUNICIPALITY_ACCOUNT=PROD_MUNICIPALITY_ACCOUNT_CHANGE_ME

# Email
SMTP_USERNAME=PROD_SMTP_USERNAME_CHANGE_ME
SMTP_PASSWORD=PROD_SMTP_PASSWORD_CHANGE_ME

# Domínios
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
VITE_BACKEND_URL=https://api.yourdomain.com

# APIs externas (opcional)
OPENAI_API_KEY=PROD_OPENAI_API_KEY_CHANGE_ME
STRIPE_SECRET_KEY=PROD_STRIPE_SECRET_KEY_CHANGE_ME
SENTRY_DSN=PROD_SENTRY_DSN_CHANGE_ME
```

## 🔄 Regenerar Ficheiros

Use o script de automação:

```bash
# Regenerar todos os ficheiros
./scripts/generate_envs.sh

# Apenas produção (com novos segredos)
./scripts/generate_envs.sh --prod-only

# Apenas desenvolvimento
./scripts/generate_envs.sh --dev-only

# Forçar sobrescrita sem confirmação
./scripts/generate_envs.sh --force
```

## 🔒 Segurança

- ✅ Todos os ficheiros `.env.*` estão no `.gitignore`
- ✅ Segredos de produção são gerados automaticamente
- ✅ Valores sensíveis marcados claramente para substituição
- ⚠️ **NUNCA** comites ficheiros `.env` com credenciais reais

## 📋 Checklist de Deploy

Antes de fazer deploy em produção:

- [ ] Substituir todos os valores `PROD_*_CHANGE_ME`
- [ ] Configurar domínios reais em `ALLOWED_ORIGINS`
- [ ] Testar conectividade com base de dados
- [ ] Verificar credenciais de email/SMTP
- [ ] Configurar certificados SSL se `SSL_ENABLED=true`
- [ ] Testar APIs externas (BNA, etc.)

## 🏗️ Estrutura de Ficheiros

```
sila-system/
├── .env.example              # Template principal
├── .env.development          # Config dev (gerado)
├── .env.production           # Config prod (gerado)
├── devops/
│   ├── .env.example          # Template DevOps
│   ├── .env.development      # DevOps dev (gerado)
│   └── .env.production       # DevOps prod (gerado)
├── apps/backend/config/
│   ├── .env.example          # Template backend
│   ├── .env.development      # Backend dev (gerado)
│   └── .env.production       # Backend prod (gerado)
└── scripts/
    └── generate_envs.sh      # Script de automação
```

---

**Nota:** Este ficheiro foi gerado automaticamente. Os templates foram baseados na
configuração existente e organizados para máxima segurança e facilidade de uso.
