# 🛡️ Sistema de Teste de Saúde de Módulos (Module Health Check)

Este documento descreve o sistema inteligente de verificação de saúde dos módulos do
SILA System, implementado para garantir a **integridade funcional** e **comunicação
perfeita** entre os módulos do sistema.

## 🎯 Objetivo

O sistema vai além da simples existência de código, simulando o fluxo de dados do
frontend para verificar se cada módulo está devidamente "encaixado" e operacional. Ele
valida:

- ✅ **Presença e funcionalidade** de cada módulo
- ✅ **Integração entre módulos** críticos
- ✅ **Autenticação e autorização** funcionando
- ✅ **Tempo de resposta** aceitável
- ✅ **Rotas principais** acessíveis

## 📁 Estrutura de Arquivos

```
backend/tests/
├── module_health_check.py      # Sistema principal de health check
├── conftest_health.py          # Configurações específicas para pytest
└── README_HEALTH_CHECK.md      # Esta documentação

backend/scripts/
├── run_health_check.py         # Script Python standalone
└── run_health_check.sh         # Script Bash com validações
```

## 🚀 Como Executar

### Opção 1: Script Bash (Recomendado)

```bash
# Execução básica
./backend/scripts/run_health_check.sh

# Com opções personalizadas
./backend/scripts/run_health_check.sh \
    --url http://localhost:8000 \
    --format html \
    --output relatorio.html \
    --verbose

# Testar apenas módulos específicos
./backend/scripts/run_health_check.sh --modules "auth,health,reports"
```

### Opção 2: Script Python

```bash
# Execução básica
python backend/scripts/run_health_check.py

# Com opções
python backend/scripts/run_health_check.py \
    --url http://localhost:8000 \
    --timeout 15 \
    --format json \
    --output health_report.json
```

### Opção 3: Pytest (Para CI/CD)

```bash
# Todos os testes de saúde
pytest backend/tests/module_health_check.py -v

# Teste específico
pytest backend/tests/module_health_check.py::test_module_health -v

# Com cobertura
pytest backend/tests/module_health_check.py --cov=backend.tests.module_health_check
```

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# Configurações do servidor
export API_BASE_URL="http://localhost:8000"
export TEST_TIMEOUT="10"

# Credenciais de teste
export TEST_USERNAME="admin"
export TEST_PASSWORD="Truman1*Marcelo1*"
```

### Módulos Testados

O sistema testa automaticamente os seguintes módulos críticos:

- `auth` - Autenticação e autorização
- `citizenship` - Gestão de cidadãos
- `commercial` - Licenciamento comercial
- `health` - Serviços de saúde
- `reports` - Relatórios e dashboards
- `finance` - Gestão financeira
- `urbanism` - Urbanismo e licenciamento
- `governance` - Governança e políticas
- `education` - Serviços educacionais
- `justice` - Serviços jurídicos
- `documents` - Gestão de documentos
- `notifications` - Sistema de notificações
- `monitoring` - Monitoramento do sistema
- `integration` - Integrações externas

## 📊 Formatos de Relatório

### 1. Texto (TXT) - Padrão

```
🛡️ RELATÓRIO DE SAÚDE DOS MÓDULOS - SILA SYSTEM
============================================================

📊 RESUMO GERAL:
   • Módulos saudáveis: 12/14 (85.7%)
   • Data/Hora: 27/01/2025 14:30:15
   • Base URL: http://127.0.0.1:8000

📋 DETALHES POR MÓDULO:
✅ AUTH: SAUDÁVEL
   • Status: 200
   • Tempo: 0.15s
   • Endpoint: /auth/login/access-token
```

### 2. JSON - Para Integração

```json
{
  "timestamp": "2025-01-27T14:30:15",
  "summary": {
    "total_modules": 14,
    "healthy_modules": 12,
    "health_percentage": 85.7
  },
  "modules": {
    "auth": {
      "is_healthy": true,
      "status_code": 200,
      "response_time": 0.15,
      "endpoint_tested": "/auth/login/access-token"
    }
  }
}
```

### 3. HTML - Para Visualização

Relatório HTML interativo com:

- Dashboard visual da saúde do sistema
- Métricas coloridas por status
- Detalhes expandíveis por módulo
- Timestamp e configurações

## 🔧 Funcionalidades Avançadas

### Autenticação Automática

O sistema:

1. Tenta autenticar usando TestClient (se disponível)
2. Fallback para requisição HTTP direta
3. Usa token JWT para testes protegidos
4. Continua sem autenticação se falhar (com avisos)

### Testes de Integração

Verifica comunicação crítica entre módulos:

- `reports` ↔ `finance` (relatórios financeiros)
- `citizenship` ↔ `documents` (documentos de cidadãos)
- `commercial` ↔ `urbanism` (verificação de zoneamento)
- `health` ↔ `notifications` (alertas de emergência)

### Execução Paralela

- Testes executados em paralelo para performance
- Timeout configurável por requisição
- Feedback em tempo real durante execução

### Validações Inteligentes

- **404 = Módulo não encaixado** (falha crítica)
- **200/204 = Sucesso** (módulo funcionando)
- **401 = Não autorizado** (problema de auth)
- **403 = Proibido** (problema de permissão)
- **500+ = Erro interno** (problema no servidor)

## 🎯 Critérios de Sucesso

### ✅ Sistema Saudável (≥80%)

- Módulos respondem corretamente
- Integrações funcionando
- Tempo de resposta aceitável
- Autenticação operacional

### ⚠️ Sistema com Problemas (<80%)

- Módulos não encontrados (404)
- Falhas de integração
- Timeouts frequentes
- Problemas de autenticação

## 🔍 Solução de Problemas

### Erro: "Módulo não encontrado (404)"

```bash
# Verificar se o módulo está registrado no main.py
grep -r "include_router.*MODULO" backend/app/main.py

# Verificar se o servidor está rodando
curl http://localhost:8000/docs
```

### Erro: "Timeout na requisição"

```bash
# Aumentar timeout
./backend/scripts/run_health_check.sh --timeout 30

# Verificar performance do servidor
curl -w "@curl-format.txt" http://localhost:8000/health
```

### Erro: "Falha na autenticação"

```bash
# Verificar credenciais
export TEST_USERNAME="seu_usuario"
export TEST_PASSWORD="sua_senha"

# Verificar endpoint de auth
curl -X POST http://localhost:8000/auth/login/access-token \
  -d "username=admin&Truman1*Marcelo1*
```

## 🔄 Integração com CI/CD

### GitHub Actions

```yaml
name: Health Check
on: [push, pull_request]
jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r backend/requirements_test.txt
      - name: Start server
        run: cd backend && python -m uvicorn app.main:app &
      - name: Run health check
        run:
          python backend/scripts/run_health_check.py --format json --output health.json
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: health-report
          path: health.json
```

### Docker

```dockerfile
FROM python:3.9-slim
COPY backend/ /app/
WORKDIR /app
RUN pip install -r requirements_test.txt
CMD ["python", "scripts/run_health_check.py"]
```

## 📈 Métricas e Monitoramento

### KPIs do Sistema

- **Taxa de Saúde**: % de módulos funcionais
- **Tempo Médio de Resposta**: Performance geral
- **Taxa de Integração**: % de integrações funcionando
- **Disponibilidade**: % de uptime dos módulos

### Alertas Automáticos

- Saúde < 80% → Alerta crítico
- Tempo de resposta > 5s → Alerta de performance
- Falha de integração → Alerta de dependência
- Módulo não encontrado → Alerta de configuração

## 🛠️ Manutenção e Extensão

### Adicionando Novos Módulos

1. Adicionar à lista `critical_modules` em `ModuleHealthChecker`
2. Definir endpoints em `module_endpoints`
3. Adicionar integrações em `critical_integrations`

### Customizando Testes

```python
# Exemplo: teste customizado para módulo específico
@pytest.mark.asyncio
async def test_custom_module_validation(health_checker):
    result = await health_checker.test_module_endpoint(
        "custom_module", "/custom/special-endpoint"
    )
    assert result.is_healthy
    assert result.response_time < 2.0
```

### Configurações Avançadas

```python
# Exemplo: configuração personalizada
checker = ModuleHealthChecker(
    base_url="https://api.sila.com.br",
    timeout=30.0
)

# Adicionar módulos customizados
checker.critical_modules.extend(["custom1", "custom2"])
```

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique este README
2. Execute com `--verbose` para mais detalhes
3. Consulte os logs do servidor
4. Abra uma issue no repositório

---

**🛡️ Sistema de Health Check - SILA System** _Garantindo a integridade funcional dos
módulos_
