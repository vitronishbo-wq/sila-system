# 📖 Integration Validator - Guia Completo

**Versão:** 1.0.0 **Criado:** 2024 **Status:** Production-Ready ✅

## 🎯 Visão Geral

O **Integration Validator** é um script Python profissional que testa a integração entre
frontend e backend, com suporte a:

- ✅ Retry inteligente com backoff exponencial + jitter
- ✅ Circuit-breaker pattern (evita cascata de falhas)
- ✅ Execução paralela (acelera testes)
- ✅ Validação de CORS com preflight
- ✅ Injeção de token de autenticação
- ✅ Múltiplos formatos de saída (JSON, Markdown, HTML)
- ✅ Configuração via YAML
- ✅ CI/CD ready com exit codes semânticos

---

## ⚙️ Instalação

### 1. Dependências Obrigatórias

```bash
pip install requests
```

### 2. Dependências Opcionais

```bash
# Para suporte a YAML e gráficos
pip install pyyaml matplotlib
```

### 3. Configuração de Permissões

```bash
# Tornar scripts executáveis
chmod +x scripts/validate_frontend_backend_integration.py
chmod +x scripts/get_dev_token.sh
```

---

## 🚀 Uso Básico

### 1. Validação Padrão (sem configuração)

```bash
python scripts/validate_frontend_backend_integration.py
```

**O que faz:**

- Testa 17 endpoints padrão
- Usa `http://localhost:8000` como backend
- Usa `http://localhost:5173` como frontend
- Gera relatório em JSON, Markdown e HTML
- Sai com código 0 (sucesso) ou 2 (falha crítica)

**Output:**

```
[08:30:45] INFO: Starting integration tests...
[08:30:45] INFO: Testing 17 endpoints with 2 workers
[08:30:47] INFO: ✅ All critical endpoints passed
[08:30:47] INFO: Results: 15 PASS, 2 WARN, 0 FAIL
[08:30:47] INFO: Reports generated: integration_results.json, integration_results.md, integration_results.html
```

---

### 2. Com Arquivo de Contexto

```bash
python scripts/validate_frontend_backend_integration.py \
  --context ci/backend_context.yaml
```

**ci/backend_context.yaml:**

```yaml
backend:
  base_url: http://localhost:8000
  timeout: 8
  max_retries: 3

frontend:
  base_url: http://localhost:5173

auth:
  enabled: true
  method: "static" # ou "command"
  token: "eyJ0eXAiOiJKV1QiLCJhbGc..." # ou comando abaixo
  # command: "./scripts/get_dev_token.sh"

cors:
  enabled: true
  allowed_origins:
    - "http://localhost:5173"
    - "http://localhost:3000"
```

---

### 3. Com Arquivo de Endpoints Customizado

```bash
python scripts/validate_frontend_backend_integration.py \
  --endpoints ci/custom_endpoints.yaml
```

**ci/custom_endpoints.yaml:**

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
    expect_status: [200, 401]
    body:
      username: "test@sila.gov.ao"
      password: "TestPassword123!"

  - name: "Get User Profile"
    method: GET
    url: /api/user/me
    critical: true
    auth_required: true
    expect_status: [200, 401]
```

---

### 4. Obter Token de Autenticação

**Opção A: Token estático (não recomendado para produção)**

```bash
TOKEN="seu_token_jwt"
python scripts/validate_frontend_backend_integration.py \
  --auth-token "$TOKEN"
```

**Opção B: Token dinâmico via script**

```bash
# Script shell que retorna o token
./scripts/get_dev_token.sh
# Output: eyJ0eXAiOiJKV1QiLCJhbGc...

# Usar em validation
python scripts/validate_frontend_backend_integration.py \
  --auth-command "./scripts/get_dev_token.sh"
```

**Opção C: Token dinâmico via config**

```yaml
# ci/backend_context.yaml
auth:
  method: "command"
  command: "./scripts/get_dev_token.sh"
```

---

### 5. Modo Dry-Run (teste sem falhar)

```bash
python scripts/validate_frontend_backend_integration.py \
  --dry-run
```

**Comportamento:**

- Executa testes normalmente
- Gera relatórios
- **Não falha** no final (sai com código 0 sempre)
- Útil para verificar problemas sem quebrar CI/CD

---

### 6. Customizar URLs

```bash
python scripts/validate_frontend_backend_integration.py \
  --backend-url "http://api.staging.sila.gov.ao" \
  --frontend-url "http://app.staging.sila.gov.ao" \
  --timeout 15
```

---

### 7. Paralelo com Customizações

```bash
python scripts/validate_frontend_backend_integration.py \
  --context ci/backend_context.yaml \
  --endpoints ci/custom_endpoints.yaml \
  --auth-command "./scripts/get_dev_token.sh" \
  --workers 4 \
  --timeout 12 \
  --output-dir "./test_results" \
  --format json,html
```

---

## 📊 Formatos de Saída

### JSON Report

**Arquivo:** `integration_results.json`

```json
{
  "timestamp": "2024-11-20T08:30:47.123456Z",
  "summary": {
    "total": 17,
    "passed": 15,
    "failed": 2,
    "skipped": 0,
    "critical_passed": 8,
    "critical_failed": 0
  },
  "endpoints": [
    {
      "name": "Health Check",
      "method": "GET",
      "url": "http://localhost:8000/health",
      "status": "PASS",
      "http_code": 200,
      "latency_ms": 12.5,
      "attempts": 1,
      "error": null
    },
    {
      "name": "Login",
      "method": "POST",
      "url": "http://localhost:8000/api/auth/login",
      "status": "FAIL",
      "http_code": 500,
      "latency_ms": 145.3,
      "attempts": 3,
      "error": "Internal Server Error"
    }
  ],
  "performance": {
    "p50_latency_ms": 45.2,
    "p95_latency_ms": 230.1,
    "p99_latency_ms": 450.5,
    "total_duration_ms": 2847
  }
}
```

**Parsing em CI/CD:**

```bash
# Verificar se tudo passou
CRITICAL_FAILED=$(jq '.summary.critical_failed' integration_results.json)
if [ "$CRITICAL_FAILED" -gt 0 ]; then
  echo "Critical failures detected!"
  exit 1
fi
```

---

### Markdown Report

**Arquivo:** `integration_results.md`

```markdown
# Integration Test Results

**Date:** 2024-11-20 08:30:47 **Duration:** 2.8s

## Summary

| Metric          | Value |
| --------------- | ----- |
| Total Endpoints | 17    |
| ✅ Passed       | 15    |
| ❌ Failed       | 2     |
| ⏭️ Skipped      | 0     |

## Critical Endpoints

| Endpoint     | Method | Status  | Latency |
| ------------ | ------ | ------- | ------- |
| Health Check | GET    | ✅ PASS | 12.5ms  |
| Login        | POST   | ❌ FAIL | 145.3ms |
| Get User     | GET    | ✅ PASS | 34.2ms  |

## Performance

- **P50 Latency:** 45.2ms
- **P95 Latency:** 230.1ms
- **P99 Latency:** 450.5ms

## Failures

### 1. Login - POST /api/auth/login

- **Status:** 500 Internal Server Error
- **Latency:** 145.3ms (3 attempts)
- **Error:** `Internal Server Error`

### 2. Create Item - POST /api/items

- **Status:** 403 Forbidden
- **Latency:** 89.5ms
- **Error:** `Permission Denied`
```

---

### HTML Report

**Arquivo:** `integration_results.html`

- ✅ Status visual com cores (verde=pass, vermelho=fail)
- 📊 Gráficos de latência (com matplotlib)
- 📈 P50/P95/P99 latency
- 🔍 Detalhes de cada endpoint
- 📋 Tabelas interativas

---

## 🔐 Autenticação

### Método 1: Token Estático

```python
# Script
python scripts/validate_frontend_backend_integration.py \
  --auth-token "eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Pros:** Simples, rápido **Cons:** Token fixo, menos seguro

---

### Método 2: Comando Dinâmico

```python
# Script shell que retorna token
cat scripts/get_dev_token.sh
```

```bash
#!/bin/bash
RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"test@sila.gov.ao","password":"TestPassword123!"}' \
  http://localhost:8000/api/auth/login)
echo "$RESPONSE" | jq -r '.access_token'
```

**Uso:**

```bash
python scripts/validate_frontend_backend_integration.py \
  --auth-command "./scripts/get_dev_token.sh"
```

**Pros:** Token renovado a cada teste, mais seguro **Cons:** Mais lento (precisa
autenticar primeiro)

---

### Método 3: Via Arquivo de Contexto

```yaml
# ci/backend_context.yaml
auth:
  method: "static" # ou "command"
  token: "eyJ0eXAiOiJKV1QiLCJhbGc..."
  # OU
  command: "./scripts/get_dev_token.sh"
```

---

## 🔌 CORS Validation

O script automaticamente testa CORS fazendo preflight:

```bash
OPTIONS /api/items HTTP/1.1
Origin: http://localhost:5173
Access-Control-Request-Method: POST
```

**Verifica:**

- ✅ Header `Access-Control-Allow-Origin` presente
- ✅ Métodos permitidos incluem GET, POST, PUT, DELETE
- ✅ Headers permitidos incluem Authorization, Content-Type
- ✅ Credentials mode configurado corretamente

---

## 🛡️ Circuit Breaker

Se um endpoint falhar 3 vezes consecutivas:

1. **CIRCUIT TRIPS** → Endpoint marcado como fora de serviço
2. **Skip retries** → Próximas tentativas puladas por 30 segundos
3. **Auto-reset** → Após 30s, tenta novamente

**Log:**

```
[08:30:50] WARNING: CIRCUIT TRIPPED for Login (3 consecutive failures)
[08:31:20] INFO: CIRCUIT RESET for Login after 30s timeout
```

---

## 📈 Retry & Backoff

Cada endpoint tenta até 3 vezes com backoff exponencial:

```
Tentativa 1: Imediato
Tentativa 2: Espera 0.5s + jitter
Tentativa 3: Espera 1.0s + jitter
Tentativa 4: Espera 2.0s + jitter
Máximo: 10s por tentativa
```

**Log:**

```
[08:30:50] INFO: Test endpoint "Login" (attempt 1/3)
[08:30:51] WARNING: Attempt 1 failed with HTTP 500, retrying in 0.6s...
[08:30:51] INFO: Test endpoint "Login" (attempt 2/3)
[08:30:52] WARNING: Attempt 2 failed with HTTP 500, retrying in 1.2s...
[08:30:53] INFO: Test endpoint "Login" (attempt 3/3)
[08:30:53] ERROR: All 3 attempts failed for Login
```

---

## 🔧 GitHub Actions Integration

### Configuração CI/CD

**`.github/workflows/integration-tests.yaml`:**

```yaml
name: Integration Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: "0 * * * *" # A cada hora

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests pyyaml matplotlib

      - name: Get dev token
        id: auth
        run: |
          TOKEN=$(./scripts/get_dev_token.sh)
          echo "::add-mask::$TOKEN"
          echo "token=$TOKEN" >> $GITHUB_OUTPUT
        env:
          BACKEND_URL: http://localhost:8000

      - name: Run integration tests
        run:
          python scripts/validate_frontend_backend_integration.py \ --backend-url
          http://localhost:8000 \ --auth-token "${{ steps.auth.outputs.token }}" \
          --output-dir ./test_results

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: integration-results
          path: test_results/

      - name: Comment PR
        if: github.event_name == 'pull_request' && always()
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('./test_results/integration_results.json', 'utf8'));
            const comment = `## Integration Test Results\n
            - **Total:** ${results.summary.total}
            - **Passed:** ${results.summary.passed}
            - **Failed:** ${results.summary.failed}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

## 📋 Checklist de Deploy

- [ ] Instalar `requests` (obrigatório)
- [ ] Instalar `pyyaml` e `matplotlib` (opcional)
- [ ] Revisar `ci/endpoints.yaml` para seus endpoints reais
- [ ] Configurar `ci/backend_context.yaml` com seus URLs
- [ ] Preparar autenticação (token ou script)
- [ ] Testar localmente: `python scripts/validate_frontend_backend_integration.py`
- [ ] Criar GitHub Actions workflow
- [ ] Testar workflow no repository
- [ ] Configurar Slack/Discord webhook para alertas (opcional)
- [ ] Documentar endpoints customizados para sua equipe

---

## 🐛 Troubleshooting

### Problema: "Connection refused"

```
ERROR: Failed to connect to http://localhost:8000
```

**Solução:**

```bash
# Verificar se backend está rodando
curl -i http://localhost:8000/health

# Se não estiver, iniciar backend
cd apps/backend
python -m uvicorn main:app --reload
```

---

### Problema: "401 Unauthorized"

```
ERROR: Authentication failed for /api/user/me (HTTP 401)
```

**Solução:**

```bash
# Verificar token
./scripts/get_dev_token.sh

# Testar com token manualmente
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/user/me
```

---

### Problema: "CORS error"

```
ERROR: CORS preflight failed for /api/items (HTTP 403)
```

**Solução:**

```bash
# Verificar CORS headers no backend
curl -i -X OPTIONS \
  -H "Origin: http://localhost:5173" \
  http://localhost:8000/api/items

# Deve retornar Access-Control-Allow-* headers
```

---

### Problema: "Circuit breaker tripped"

```
WARNING: CIRCUIT TRIPPED for Login (3 consecutive failures)
```

**Solução:**

```bash
# Esperar 30 segundos ou resetar manualmente:
python scripts/validate_frontend_backend_integration.py --no-circuit-breaker
```

---

## 📚 Referência Rápida

| Comando                                                   | Descrição                      |
| --------------------------------------------------------- | ------------------------------ |
| `python scripts/validate_frontend_backend_integration.py` | Teste padrão                   |
| `... --context ci/backend_context.yaml`                   | Com arquivo de contexto        |
| `... --endpoints ci/custom_endpoints.yaml`                | Com endpoints customizados     |
| `... --auth-token "$TOKEN"`                               | Com token estático             |
| `... --auth-command "./get_token.sh"`                     | Com token dinâmico             |
| `... --workers 4`                                         | 4 workers paralelos            |
| `... --timeout 15`                                        | Timeout de 15s por endpoint    |
| `... --dry-run`                                           | Teste sem falhar               |
| `... --format json,html`                                  | Apenas JSON e HTML             |
| `... --output-dir ./results`                              | Diretório de saída customizado |

---

## 🎯 Próximos Passos

1. ✅ Executar validação padrão
2. ✅ Revisar relatórios (JSON/Markdown/HTML)
3. ✅ Customizar endpoints para seu projeto
4. ✅ Configurar autenticação
5. ✅ Integrar com GitHub Actions
6. ✅ Configurar alertas em Slack
7. ✅ Estender com testes OpenAPI schema

---

**Dúvidas?** Consulte os arquivos de exemplo:

- `ci/endpoints.yaml` - Endpoints
- `ci/backend_context.yaml` - Configuração
- `scripts/validate_frontend_backend_integration.py` - Script principal
- `scripts/get_dev_token.sh` - Script de autenticação
