# 🔧 Plano de Saneamento Técnico - SILA System

**Data de Criação:** 2025-10-04 **Versão:** 1.0 **Status:** Em Execução

---

## 📋 Sumário Executivo

Este documento detalha o plano completo de saneamento técnico do projeto SILA-System,
identificando 10 problemas críticos e propondo 7 ações automatizadas de correção.

### Problemas Identificados

1. ✅ Estrutura de módulos com duplicações e inconsistências
2. ✅ Problemas críticos de importação e dependências cíclicas
3. ✅ Inconsistência na organização de modelos, schemas e rotas
4. ✅ Falta de padronização entre camadas de domínio
5. ✅ Presença de arquivos corrompidos ou com sintaxe inválida
6. ✅ Configuração crítica de ambiente mal gerida
7. ✅ Divergência entre frontend e backend
8. ✅ Ausência de testes abrangentes
9. ⚠️ Fragilidade na integração entre módulos transversais
10. ⚠️ Risco de escalabilidade (governança, observabilidade, métricas)

---

## 🎯 Objetivos do Saneamento

1. **Consistência**: Estrutura uniforme em todos os módulos
2. **Integridade**: Código sem erros de sintaxe ou importação
3. **Operabilidade**: Sistema funcional e testável
4. **Manutenibilidade**: Código organizado e documentado
5. **Escalabilidade**: Arquitetura preparada para crescimento

---

## 🚀 Execução do Saneamento

### Comando Principal

```bash
# Executar saneamento completo
python3 scripts/saneamento_master.py

# Executar passo específico
python3 scripts/saneamento_master.py --step 1

# Modo dry-run (apenas verificação)
python3 scripts/saneamento_master.py --dry-run

# Modo verbose
python3 scripts/saneamento_master.py --verbose
```

---

## 📊 Passos do Saneamento

### Passo 1: Corrigir Estrutura de Módulos

**Objetivo**: Eliminar duplicações e pastas mal nomeadas

**Ações**:

- Identificar pastas com nomes incorretos (`citize/`, `appoi/`)
- Renomear ou mover para padrão `modules/<domínio>/`
- Garantir estrutura mínima: `models/`, `schemas/`, `routes/`, `services/`

**Scripts Utilizados**:

- `generate_modules_structure.py`
- `check_module_integrity.py`

**Critérios de Sucesso**:

- ✅ Todos os módulos seguem padrão de nomenclatura
- ✅ Estrutura de diretórios consistente
- ✅ Sem pastas vazias ou duplicadas

**Prioridade**: 🔴 CRÍTICA

---

### Passo 2: Resolver Importações e Ciclos

**Objetivo**: Eliminar imports quebrados e dependências circulares

**Ações**:

- Substituir imports absolutos inválidos
- Detectar e quebrar ciclos de dependência
- Padronizar imports de `auth_utils`, `security`, `core.auth`

**Scripts Utilizados**:

- `fix_imports.py`
- `fix_broken_imports.py`
- `fix_auth_utils_imports.py`
- `fix_security_imports.py`
- `detect_and_fix_import_cycles.py`

**Exemplo de Correção**:

```python
# Antes
from core.auth import security

# Depois
from app.core.auth.security import verify_token
```

**Critérios de Sucesso**:

- ✅ Todos os imports resolvem corretamente
- ✅ Sem ciclos de importação
- ✅ Código importa sem erros

**Prioridade**: 🔴 CRÍTICA

---

### Passo 3: Padronizar Camadas por Domínio

**Objetivo**: Garantir estrutura completa em todos os módulos

**Ações**:

- Criar `models/`, `schemas/`, `routes/`, `services/` onde faltam
- Aplicar template uniforme
- Garantir `__init__.py` em todos os pacotes

**Scripts Utilizados**:

- `check_and_generate_modules.py`
- `generate_modules_structure.py`

**Estrutura Padrão**:

```
modules/<domínio>/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── <domínio>.py
├── schemas/
│   ├── __init__.py
│   └── <domínio>.py
├── routes/
│   ├── __init__.py
│   └── <domínio>_routes.py
└── services/
    ├── __init__.py
    └── <domínio>_service.py
```

**Critérios de Sucesso**:

- ✅ Todos os módulos têm estrutura completa
- ✅ Arquivos `__init__.py` presentes e corretos
- ✅ Nomenclatura consistente

**Prioridade**: 🟡 ALTA

---

### Passo 4: Corrigir Arquivos Corrompidos

**Objetivo**: Detectar e reparar arquivos com problemas de sintaxe

**Ações**:

- Corrigir encoding (UTF-8, remover BOM)
- Reparar strings não terminadas
- Corrigir erros de sintaxe Python
- Validar compilação de todos os arquivos `.py`

**Scripts Utilizados**:

- `fix_encoding.py`
- `fix_unterminated_strings.py`
- `fix_syntax_errors_targeted.py`
- `validate_py_syntax.py`
- `validate_py_compile.py`

**Critérios de Sucesso**:

- ✅ Todos os arquivos `.py` compilam sem erro
- ✅ Encoding UTF-8 consistente
- ✅ Sem strings não terminadas

**Prioridade**: 🔴 CRÍTICA

---

### Passo 5: Validar Variáveis de Ambiente

**Objetivo**: Garantir configuração completa e coerente

**Ações**:

- Validar `.env.example` completo
- Sincronizar `.env.test` com `.env.example`
- Verificar variáveis críticas (DATABASE_URL, SECRET_KEY, etc.)
- Padronizar formato e nomenclatura

**Scripts Utilizados**:

- `validate_env.py`
- `padronizar_envs.py`
- `validar_env_critico.py`
- `validar_env_conexao.py`

**Variáveis Críticas**:

```bash
# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost/sila_db
DATABASE_TEST_URL=postgresql://user:pass@localhost/sila_test

# Segurança
SECRET_KEY=<gerado-automaticamente>
JWT_SECRET_KEY=<gerado-automaticamente>
JWT_ALGORITHM=HS256

# Aplicação
APP_NAME=SILA-System
ENVIRONMENT=development
DEBUG=True
```

**Critérios de Sucesso**:

- ✅ `.env.example` completo e documentado
- ✅ `.env.test` sincronizado
- ✅ Todas as variáveis críticas presentes
- ✅ Valores de teste válidos

**Prioridade**: 🔴 CRÍTICA

---

### Passo 6: Harmonizar Frontend/Backend

**Objetivo**: Alinhar endpoints e schemas entre frontend e backend

**Ações**:

- Verificar rotas do frontend vs backend
- Validar schemas de request/response
- Documentar divergências
- Gerar relatório de sincronização

**Scripts Utilizados**:

- `check-frontend-sync.py`

**Verificações**:

- ✅ Endpoints do frontend existem no backend
- ✅ Métodos HTTP correspondem
- ✅ Schemas de dados compatíveis
- ✅ Autenticação consistente

**Critérios de Sucesso**:

- ✅ 100% dos endpoints frontend mapeados
- ✅ Schemas validados
- ✅ Documentação atualizada

**Prioridade**: 🟡 ALTA

---

### Passo 7: Garantir Testes Mínimos

**Objetivo**: Criar testes esqueletos para módulos sem cobertura

**Ações**:

- Identificar módulos sem testes
- Gerar testes básicos (CRUD, endpoints)
- Criar fixtures mínimas
- Configurar pytest

**Scripts Utilizados**:

- `tests/generate_tests_simple.py`
- `tests/generate_tests.py`

**Template de Teste**:

```python
import pytest
from fastapi.testclient import TestClient

def test_create_<recurso>(client: TestClient, auth_headers):
    """Testa criação de <recurso>."""
    response = client.post(
        "/api/v1/<modulo>/<recurso>",
        json={"campo": "valor"},
        headers=auth_headers
    )
    assert response.status_code == 201

def test_list_<recurso>(client: TestClient, auth_headers):
    """Testa listagem de <recurso>."""
    response = client.get(
        "/api/v1/<modulo>/<recurso>",
        headers=auth_headers
    )
    assert response.status_code == 200
```

**Critérios de Sucesso**:

- ✅ Todos os módulos têm pelo menos 1 teste
- ✅ Testes executam sem erro
- ✅ Cobertura mínima de 30%

**Prioridade**: 🟢 MÉDIA

---

## 📈 Métricas de Sucesso

### Antes do Saneamento

- ❌ Módulos com estrutura inconsistente: ~40%
- ❌ Erros de importação: ~150
- ❌ Arquivos com erros de sintaxe: ~25
- ❌ Cobertura de testes: ~15%
- ❌ Variáveis de ambiente faltantes: ~30%

### Após o Saneamento (Meta)

- ✅ Módulos com estrutura consistente: 100%
- ✅ Erros de importação: 0
- ✅ Arquivos com erros de sintaxe: 0
- ✅ Cobertura de testes: >30%
- ✅ Variáveis de ambiente: 100% documentadas

---

## 🔍 Monitoramento e Validação

### Validação Contínua

```bash
# Validar sintaxe Python
python3 scripts/validate_py_syntax.py

# Validar imports
python3 scripts/validate_model_imports.py

# Validar estrutura de módulos
python3 scripts/check_module_integrity.py

# Executar testes
pytest backend/tests/ -v --cov=backend/app

# Validar ambiente
python3 scripts/validate_env.py
```

### Relatórios Gerados

1. **saneamento*report*<timestamp>.json** - Dados estruturados
2. **saneamento*report*<timestamp>.md** - Relatório legível
3. **saneamento\_<timestamp>.log** - Log completo de execução

Localização: `scripts/saneamento_reports/`

---

## ⚠️ Riscos e Mitigações

| Risco                      | Impacto | Probabilidade | Mitigação                                  |
| -------------------------- | ------- | ------------- | ------------------------------------------ |
| Quebra de código existente | Alto    | Média         | Backup antes, testes após cada passo       |
| Perda de funcionalidades   | Alto    | Baixa         | Validação incremental, rollback disponível |
| Tempo de execução longo    | Médio   | Alta          | Execução por passos, paralelização         |
| Conflitos de merge         | Médio   | Média         | Branch dedicado, comunicação com equipe    |

---

## 📅 Cronograma Sugerido

### Fase 1: Preparação (30 min)

- Backup do projeto
- Criar branch `saneamento/master`
- Revisar scripts disponíveis

### Fase 2: Execução (2-3 horas)

- Executar passos 1-4 (críticos)
- Validar após cada passo
- Corrigir erros encontrados

### Fase 3: Validação (1 hora)

- Executar passos 5-7
- Rodar testes completos
- Gerar relatórios

### Fase 4: Revisão (30 min)

- Revisar relatórios
- Documentar pendências
- Planejar próximos passos

**Tempo Total Estimado**: 4-5 horas

---

## 🔄 Próximos Passos (Pós-Saneamento)

1. **Documentação**

   - Atualizar README de cada módulo
   - Documentar APIs com OpenAPI
   - Criar guias de desenvolvimento

2. **Testes**

   - Aumentar cobertura para >60%
   - Adicionar testes de integração
   - Configurar CI/CD

3. **Observabilidade**

   - Implementar logging estruturado
   - Configurar métricas (Prometheus)
   - Adicionar tracing (OpenTelemetry)

4. **Performance**

   - Otimizar queries N+1
   - Implementar cache
   - Revisar índices de banco

5. **Segurança**
   - Auditoria de segurança
   - Implementar rate limiting
   - Revisar permissões

---

## 📞 Suporte e Contato

- **Documentação**: `/docs/`
- **Issues**: GitHub Issues
- **Logs**: `scripts/saneamento_reports/`

---

## 📝 Changelog

### v1.0 - 2025-10-04

- ✅ Criação do plano inicial
- ✅ Definição de 7 passos de saneamento
- ✅ Criação do script master
- ✅ Documentação completa

---

**Última Atualização**: 2025-10-04 11:38:00 **Responsável**: Sistema de Saneamento
Automatizado
