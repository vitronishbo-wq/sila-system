# ⚡ Integration Validator - Quick Start Checklist

**Tempo Total:** ~5 minutos para ficar operacional **Dificuldade:** Fácil ✅

---

## ✅ Checklist de Setup

### 1️⃣ Instalação (1 minuto)

```bash
# Navegar ao projeto
cd ~/dev/sila-system

# Instalar dependências Python
pip install requests pyyaml matplotlib

# Verificar instalação
pip list | grep -E "requests|yaml|matplotlib"
```

**Status:** ⬜ → ✅ (Quando vir pacotes listados)

---

### 2️⃣ Primeiro Teste (2 minutos)

```bash
# Executar validação padrão
python scripts/validate_frontend_backend_integration.py

# Aguardar conclusão (deve levar ~2-3 segundos)
# Vai gerar:
# - integration_results.json
# - integration_results.md
# - integration_results.html
```

**Esperado:**

```
[timestamp] INFO: Starting integration tests...
[timestamp] INFO: Testing 17 endpoints with 2 workers
[timestamp] INFO: ✅ All critical endpoints passed
[timestamp] INFO: Results: X PASS, Y FAIL, Z WARN
```

**Status:** ⬜ → ✅ (Quando vir "Reports generated")

---

### 3️⃣ Revisar Resultados (1 minuto)

```bash
# Opção A: JSON (para parsing)
cat integration_results.json | head -20

# Opção B: Markdown (human-readable)
cat integration_results.md

# Opção C: HTML (visual - abrir no browser)
open integration_results.html  # macOS
# ou
xdg-open integration_results.html  # Linux
# ou
start integration_results.html  # Windows
```

**Status:** ⬜ → ✅ (Quando conseguir visualizar relatório)

---

### 4️⃣ Configurar com Context (1 minuto)

```bash
# Revisar arquivo de contexto (já criado em ci/backend_context.yaml)
cat ci/backend_context.yaml

# Se precisar customizar URLs:
# Editar ci/backend_context.yaml e mudar:
#   backend.base_url: seu_backend_url
#   frontend.base_url: seu_frontend_url

# Reexecutar com config
python scripts/validate_frontend_backend_integration.py \
  --context ci/backend_context.yaml \
  --endpoints ci/endpoints.yaml
```

**Status:** ⬜ → ✅ (Quando testes rodarem com suas URLs)

---

### 5️⃣ Configurar GitHub Actions (1 minuto)

```bash
# Workflow já está criado em .github/workflows/integration-tests.yaml
# Apenas fazer push para ativar:

git add .github/workflows/integration-tests.yaml
git commit -m "feat: add integration test workflow"
git push origin main

# Verificar execução em: GitHub → Actions → Integration Tests
```

**Status:** ⬜ → ✅ (Quando workflow executar e aparecer em Actions)

---

## 🎯 Próximas Ações

### A - Ajustar Endpoints

```bash
# Editar endpoints para seus casos de uso
nano ci/endpoints.yaml

# Adicionar seus endpoints reais:
# - /api/seu-endpoint
# - /api/outro-endpoint
# etc

# Reexecutar
python scripts/validate_frontend_backend_integration.py --endpoints ci/endpoints.yaml
```

### B - Setup de Autenticação

```bash
# Opção 1: Token estático (rápido, menos seguro)
TOKEN="seu_token_jwt"
python scripts/validate_frontend_backend_integration.py --auth-token "$TOKEN"

# Opção 2: Token dinâmico (mais seguro, um pouco mais lento)
# Editar ./scripts/get_dev_token.sh com suas credenciais
# Reexecutar:
python scripts/validate_frontend_backend_integration.py \
  --auth-command "./scripts/get_dev_token.sh"

# Opção 3: Via arquivo de config (recomendado)
# Editar ci/backend_context.yaml:
#   auth:
#     method: "command"
#     command: "./scripts/get_dev_token.sh"
# Reexecutar:
python scripts/validate_frontend_backend_integration.py \
  --context ci/backend_context.yaml
```

### C - Setup Slack Notifications (optional)

```bash
# No GitHub repository:
# 1. Ir em Settings → Secrets and Variables → Actions
# 2. Adicionar novo secret: SLACK_WEBHOOK_URL
# 3. Valor: seu webhook URL do Slack
# 4. Workflow agora notificará automaticamente
```

---

## 🔍 Troubleshooting Rápido

### ❌ "Connection refused"

```bash
# Verificar se backend está rodando
curl -i http://localhost:8000/health

# Se não estiver:
# Abrir outro terminal e iniciar backend
cd apps/backend
python -m uvicorn main:app --reload
```

### ❌ "401 Unauthorized"

```bash
# Verificar token
./scripts/get_dev_token.sh

# Editar ci/backend_context.yaml com token válido
# ou testar com token específico:
python scripts/validate_frontend_backend_integration.py \
  --auth-token "seu_token_válido"
```

### ❌ "Connection timeout"

```bash
# Aumentar timeout
python scripts/validate_frontend_backend_integration.py --timeout 15
```

### ❌ "CORS error"

```bash
# Verificar headers CORS no backend
curl -i -X OPTIONS \
  -H "Origin: http://localhost:5173" \
  http://localhost:8000/api/items

# Se falhar, configurar CORS no backend
```

---

## 📊 Interpretar Resultados

### JSON Report

```json
{
  "summary": {
    "total": 17,
    "passed": 16,
    "failed": 1,
    "critical_failed": 0  ← Importante!
  },
  "performance": {
    "p95_latency_ms": 230.1  ← Compare com SLA
  }
}
```

**Checklist:**

- ✅ `critical_failed == 0` → Produção OK
- ✅ `p95_latency_ms < 250` → Performance OK
- ✅ `failed < 2` → Sistema OK

### Markdown Report

```markdown
| Endpoint | Method | Status  | Latency |
| -------- | ------ | ------- | ------- |
| Health   | GET    | ✅ PASS | 12.5ms  |
| Login    | POST   | ❌ FAIL | 145.3ms |

### Failures

- **Login**: 500 Internal Server Error
```

**O que fazer se FAIL:**

1. Verificar error message
2. Testar endpoint manualmente: `curl -X POST http://localhost:8000/api/auth/login`
3. Verificar logs do backend
4. Corrigir e reexecutar

---

## 🚀 Fluxo Completo (5 minutos)

```
1. pip install requests pyyaml matplotlib  (1 min)
                    ↓
2. python scripts/validate_frontend_backend_integration.py  (2 min)
                    ↓
3. cat integration_results.md  (1 min)
                    ↓
4. git push (ativa GitHub Actions)  (1 min)
                    ↓
✅ PRONTO!
```

---

## 💡 Dicas

### Executar Periodicamente

```bash
# Cron job (Linux/macOS)
# Adicionar ao crontab:
# */30 * * * * cd ~/dev/sila-system && python scripts/validate_frontend_backend_integration.py >> /tmp/integration_tests.log 2>&1

# Ou usar GitHub Actions schedule (já configurado)
# Workflow executa a cada hora automaticamente
```

### Integrar com seu CI/CD

```bash
# Exit code para scripting
if python scripts/validate_frontend_backend_integration.py; then
  echo "✅ All tests passed!"
else
  echo "❌ Tests failed!"
  exit 1
fi
```

### Debug Mode

```bash
python scripts/validate_frontend_backend_integration.py \
  --dry-run \
  --format json,markdown \
  --workers 1  # Desabilitar paralelo para debug
```

---

## 📚 Referências Rápidas

| Tarefa         | Comando                                                               |
| -------------- | --------------------------------------------------------------------- |
| Teste básico   | `python scripts/validate_frontend_backend_integration.py`             |
| Com config     | `... --context ci/backend_context.yaml --endpoints ci/endpoints.yaml` |
| Com auth       | `... --auth-command "./scripts/get_dev_token.sh"`                     |
| Apenas JSON    | `... --format json`                                                   |
| Dry-run        | `... --dry-run`                                                       |
| Custom timeout | `... --timeout 15`                                                    |
| Custom workers | `... --workers 8`                                                     |
| Help           | `... --help`                                                          |

---

## ✅ Final Checklist

- [ ] Dependências instaladas (pip install requests pyyaml matplotlib)
- [ ] Primeiro teste executado com sucesso
- [ ] Relatórios visualizados (JSON/Markdown/HTML)
- [ ] Endpoints customizados em ci/endpoints.yaml
- [ ] Autenticação configurada em ci/backend_context.yaml
- [ ] GitHub Actions workflow ativado (git push)
- [ ] Testes passando com exit code 0
- [ ] Prontos para monitoramento contínuo ✅

---

## 🎉 Sucesso!

Você está pronto para:

- ✅ Testar integração frontend-backend automaticamente
- ✅ Receber feedback em PRs
- ✅ Monitorar SLA/performance
- ✅ Detectar problemas rapidamente
- ✅ Ter relatórios profissionais em múltiplos formatos

**Próximo passo:** Execute o teste e veja a magia acontecer! 🚀

```bash
python scripts/validate_frontend_backend_integration.py
```

---

**Dúvidas?** Consulte:

- `docs/INTEGRATION_VALIDATOR_GUIDE.md` - Guia completo
- `INTEGRATION_VALIDATOR_ARCHITECTURE.md` - Como funciona internamente
- `README_INTEGRATION_VALIDATOR.md` - Overview
- `INTEGRATION_VALIDATOR_FINAL_SUMMARY.md` - Sumário executivo
