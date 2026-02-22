# 🔗 Integration Validator - README

**Status:** ✅ Production Ready **Version:** 1.0.0

> Script profissional para validação de integração frontend-backend com retry,
> circuit-breaker, CORS detection e relatórios em múltiplos formatos.

## 🚀 Quick Start (2 minutos)

```bash
# 1. Instalar
pip install requests pyyaml matplotlib

# 2. Executar
python scripts/validate_frontend_backend_integration.py

# 3. Ver resultados
cat integration_results.md
open integration_results.html
```

## 📦 Arquivos Criados

| Arquivo                                            | Propósito                | Linhas |
| -------------------------------------------------- | ------------------------ | ------ |
| `scripts/validate_frontend_backend_integration.py` | Script principal         | 1,007  |
| `scripts/get_dev_token.sh`                         | Obter token JWT          | 75     |
| `ci/endpoints.yaml`                                | Endpoints para testar    | 98     |
| `ci/backend_context.yaml`                          | Configuração de ambiente | 60     |
| `.github/workflows/integration-tests.yaml`         | CI/CD automation         | 260    |
| `docs/INTEGRATION_VALIDATOR_GUIDE.md`              | Documentação completa    | 425+   |
| `INTEGRATION_VALIDATOR_FINAL_SUMMARY.md`           | Sumário executivo        | 300+   |

## ✨ Features

- ✅ **Retry + Backoff** - Exponencial com jitter (até 10s)
- ✅ **Circuit Breaker** - Trip após 3 falhas, reset em 30s
- ✅ **Paralelo** - Até 8 workers (configurável)
- ✅ **CORS Testing** - Validação automática de preflight
- ✅ **Auth Injection** - Token estático ou dinâmico
- ✅ **Latency Tracking** - P50, P95, P99, gráficos
- ✅ **Multi-format Output** - JSON, Markdown, HTML
- ✅ **CI/CD Ready** - Exit codes semânticos (0=OK, 2=FAIL)
- ✅ **Dry-run Mode** - Teste sem falhar
- ✅ **Configurável** - YAML context + endpoints

## 💡 Exemplos

### Básico

```bash
python scripts/validate_frontend_backend_integration.py
```

### Com Config

```bash
python scripts/validate_frontend_backend_integration.py \
  --context ci/backend_context.yaml \
  --endpoints ci/endpoints.yaml
```

### Com Auth Dinâmica

```bash
python scripts/validate_frontend_backend_integration.py \
  --auth-command "./scripts/get_dev_token.sh"
```

### Staging Environment

```bash
python scripts/validate_frontend_backend_integration.py \
  --backend-url "https://api-staging.sila.gov.ao" \
  --frontend-url "https://app-staging.sila.gov.ao"
```

### Dry-run (teste sem falhar)

```bash
python scripts/validate_frontend_backend_integration.py --dry-run
```

## 📊 Relatórios

### JSON (`integration_results.json`)

Estruturado para parsing automático - use em CI/CD:

```bash
FAILED=$(jq '.summary.critical_failed' integration_results.json)
[ "$FAILED" -eq 0 ] && echo "All good!" || exit 1
```

### Markdown (`integration_results.md`)

Formatado para leitura humana - compartilhe com time.

### HTML (`integration_results.html`)

Visual com gráficos e tabelas interativas - abra no navegador.

## 🔐 Segurança

### Circuit Breaker

```
Falha 1 → Retry
Falha 2 → Retry
Falha 3 → CIRCUIT TRIPPED (30s lockout)
Após 30s → Reset automático
```

### Retry Strategy

```
Tentativa 1: Imediato
Tentativa 2: 0.5s + jitter
Tentativa 3: 1.0s + jitter
Tentativa 4: 2.0s + jitter
Máximo: 10s
```

### Auth Token

- ✅ Token "mascarado" em logs e PRs
- ✅ Suporte a múltiplos métodos (estático/dinâmico)
- ✅ Injeção automática em headers Authorization

## 🔧 GitHub Actions

Workflow já configurado em `.github/workflows/integration-tests.yaml`:

```yaml
# Triggers
- push para main/develop/staging
- pull requests
- schedule: a cada hora

# O que faz
- Setup Python + dependencies
- Iniciar DB (PostgreSQL)
- Iniciar backend (uvicorn)
- Iniciar frontend (Node.js dev server)
- Executar validação
- Comentar resultado no PR
- Upload de artifacts
- Falhar se críticos falharem
```

**Para ativar:**

```bash
git push origin main  # Workflow executa automaticamente
```

## 📖 Documentação

| Documento                                | Conteúdo                    |
| ---------------------------------------- | --------------------------- |
| `docs/INTEGRATION_VALIDATOR_GUIDE.md`    | Guia completo com 14 seções |
| `INTEGRATION_VALIDATOR_FINAL_SUMMARY.md` | Sumário executivo           |
| `ci/endpoints.yaml`                      | Exemplo de endpoints        |
| `ci/backend_context.yaml`                | Exemplo de context          |

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# Backend
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
TIMEOUT=8

# Auth
TEST_EMAIL=test@sila.gov.ao
TEST_PASSWORD=TestPassword123!

# Logging
DEBUG=true
```

### Arquivo de Contexto (YAML)

```yaml
backend:
  base_url: http://localhost:8000
  timeout: 8
  max_retries: 3

frontend:
  base_url: http://localhost:5173

auth:
  enabled: true
  method: "command" # ou "static"
  command: "./scripts/get_dev_token.sh"

cors:
  enabled: true
  allowed_origins:
    - "http://localhost:5173"
```

### Arquivo de Endpoints (YAML)

```yaml
endpoints:
  - name: "Health Check"
    method: GET
    url: /health
    critical: true
    expect_status: [200]

  - name: "Login"
    method: POST
    url: /api/auth/login
    critical: true
    auth_required: false
    body:
      username: "test@sila.gov.ao"
      password: "TestPassword123!"
```

## 🛠️ Troubleshooting

| Problema                  | Solução                                                                |
| ------------------------- | ---------------------------------------------------------------------- |
| "Connection refused"      | Verificar se backend está rodando: `curl http://localhost:8000/health` |
| "401 Unauthorized"        | Token inválido: `./scripts/get_dev_token.sh`                           |
| "CORS error"              | CORS misconfigured: verificar headers com curl                         |
| "Circuit breaker tripped" | Esperar 30s ou usar `--no-circuit-breaker`                             |
| "Timeout"                 | Aumentar timeout: `--timeout 15`                                       |

## 📈 SLA Típico

| Métrica            | Target      |
| ------------------ | ----------- |
| P95 Latency        | < 250ms     |
| P99 Latency        | < 500ms     |
| Critical Endpoints | 100% uptime |
| Failed Endpoints   | < 5%        |

## 🎯 Próximos Passos

- [ ] Revisar `ci/endpoints.yaml` para seus endpoints reais
- [ ] Testar localmente: `python scripts/validate_frontend_backend_integration.py`
- [ ] Configurar `.github/workflows/integration-tests.yaml` (já criado)
- [ ] Ativar webhook do Slack (opcional)
- [ ] Estender com OpenAPI schema validation (future)

## 📞 Help

```bash
# Ver todas as opções
python scripts/validate_frontend_backend_integration.py --help

# Ver versão
python scripts/validate_frontend_backend_integration.py --version
```

## 🏆 O Que Você Ganhou

1. ✅ **Testes automáticos** de integração frontend-backend
2. ✅ **Detecção rápida** de problemas (CORS, timeout, 5xx)
3. ✅ **Feedback instant** em PRs (comentários automáticos)
4. ✅ **SLA monitoring** (latência, uptime)
5. ✅ **Resiliência** built-in (retry, circuit-breaker)
6. ✅ **Relatórios completos** (JSON, Markdown, HTML)
7. ✅ **CI/CD ready** (GitHub Actions, exit codes)

---

**Começar agora:**

```bash
python scripts/validate_frontend_backend_integration.py
```

**Para detalhes:** Consulte `docs/INTEGRATION_VALIDATOR_GUIDE.md`

✅ **PRONTO PARA USAR!**
