# 🔧 SILA Pre-commit System

Sistema avançado de hooks pre-commit para garantir qualidade de código e validação
automática no SILA System.

## 🚀 Configuração Rápida

```bash
# Setup completo
make setup-precommit-all

# Ou manual
pip install pre-commit
pre-commit install --install-hooks
pre-commit install --hook-type pre-push
pre-commit install --hook-type post-commit
```

## 📋 Hooks Ativos

### **Pre-commit Stage**

- ✅ **Formatação**: Black, isort, Prettier
- ✅ **Linting**: Flake8 + Bugbear
- ✅ **Validação**: YAML, JSON, secrets
- ✅ **SILA**: estrutura, dependências, Docker

### **Pre-push Stage**

- ✅ **Validação SILA reforçada**
- ✅ **Verificação final antes do push**

### **Post-commit Stage**

- ✅ **Geração automática de relatórios**
- ✅ **Consolidação em HTML/JSON**

## 🎯 Comandos Disponíveis

```bash
# Configuração
make setup-precommit         # Setup básico
make setup-precommit-all     # Setup + execução inicial
make precommit-update        # Atualizar hooks

# Execução
make precommit-run           # Executar todos os hooks
make precommit-report        # Gerar relatórios
git commit                   # Execução automática

# Específicos
pre-commit run validate-deps # Hook específico
pre-commit run --hook-stage push # Stage específico
```

## 📊 Relatórios

### **Localização**

- `reports/pre-commit/deps_validation.json` - Validação de dependências
- `reports/pre-commit/precommit_summary.json` - Resumo consolidado
- `reports/pre-commit/precommit_summary.html` - Dashboard visual

### **Estrutura JSON**

```json
{
  "timestamp": "2025-11-16T20:54:00",
  "hooks": {
    "validate-deps": {
      "status": "PASS",
      "data": {
        "invalid": [],
        "missing": [],
        "blocked": [],
        "ok": ["fastapi==0.115.0", "uvicorn==0.32.0"]
      }
    }
  },
  "summary": {
    "total": 4,
    "passed": 4,
    "failed": 0
  }
}
```

## ⚙️ Configuração

### **Arquivo `.env.precommit`**

```bash
# Dependency validation
SILA_DEPS_STRICT=true
SILA_DEPS_REPORT_DIR=reports/pre-commit

# Structure validation
SILA_STRUCTURE_DEEP_SCAN=false

# Docker validation
SILA_DOCKER_VALIDATE_PROFILES=true

# Report generation
SILA_GENERATE_HTML_REPORTS=true
SILA_REPORT_TIMESTAMP=true
```

### **Personalização**

Edite `.pre-commit-config.yaml` para:

- Adicionar novos hooks
- Modificar stages de execução
- Ajustar argumentos dos hooks
- Configurar exclusões de arquivos

## 🔄 Integração CI/CD

### **GitHub Actions**

O workflow `sila-ci.yml` executa automaticamente:

1. Validação completa (`make ci`)
2. Hooks pre-commit (`--hook-stage push`)
3. Geração de relatórios
4. Upload de artefatos

### **Fluxo Completo**

```
git commit → pre-commit hooks → post-commit reports
git push → pre-push validation → CI/CD pipeline
```

## 🛠️ Troubleshooting

### **Hook falhou**

```bash
# Ver detalhes
pre-commit run --all-files --verbose

# Hook específico
pre-commit run validate-deps --verbose

# Pular hook temporariamente
git commit --no-verify
```

### **Atualizar hooks**

```bash
# Atualizar versões
make precommit-update

# Reinstalar hooks
pre-commit uninstall
make setup-precommit
```

### **Limpar cache**

```bash
pre-commit clean
pre-commit install --install-hooks
```

## 📈 Benefícios

- ✅ **Qualidade garantida** - código sempre formatado e validado
- ✅ **Feedback imediato** - problemas detectados antes do commit
- ✅ **CI/CD otimizado** - menos falhas no pipeline
- ✅ **Relatórios detalhados** - visibilidade completa dos problemas
- ✅ **Automação total** - zero intervenção manual necessária

---

**SILA Pre-commit System** - Qualidade enterprise automatizada 🔧✅
