# 📋 Plano Executivo de Migração: modules/ → core/

**Versão**: 2.0 (Baseado em Análise Real) **Data**: 2024 **Status**: 🔵 Pronto para
Execução (Fase 1)

---

## 🎯 Objetivo

Consolidar a **camada técnica** em `core/` deixando **domínio de negócio** em
`modules/`.

**Resultado esperado:**

- `core/` = Infraestrutura, autenticação, monitoramento, utilitários
- `modules/` = 21 domínios de negócio distintos + 8 módulos em revisão

---

## 📊 Análise Real (32 módulos identificados)

### Classificação Automática

| Categoria         | Módulos                                                                         | Arquivos | Ação                 |
| ----------------- | ------------------------------------------------------------------------------- | -------- | -------------------- |
| **🔧 Técnico**    | auth, monitoring                                                                | 55       | → `core/`            |
| **🎯 Negócio**    | citizenship, justice, finance, governance, health, education...                 | 650+     | ← Fica em `modules/` |
| **⚡ Utilidade**  | common                                                                          | 26       | → `core/utils/`      |
| **❓ Indefinido** | dashboard, integration, internal, journeys, reports, social, training, urbanism | 127      | 🔄 Manual review     |

---

## ⏱️ Cronograma: 3 Semanas

```
SEMANA 1: Preparação & Fase 1 (Baixo Risco)
├── Seg-Ter: Backup + Scripts
├── Qua-Qui: Migração Técnica (monitoring, common)
└── Sex: Testes & Validação

SEMANA 2: Fase 2 (Médio Risco)
├── Seg-Ter: Migração Auth (atualizar 5 dependentes)
├── Qua-Thu: Atualizar todos os imports
└── Sex: Testes Integração

SEMANA 3: Revisão & Documentação
├── Seg: Revisão Manual (8 indefinidos)
├── Ter-Qui: Documentação & Onboarding
└── Sex: Deploy Staging
```

---

## 🚀 FASE 1: Técnico de Baixo Risco (Semana 1)

### Etapa 1.1: `monitoring/` → `core/monitoring/`

**Por quê?**

- Padrão técnico 90% confiança
- Importado por apenas 2 módulos (baixo risco)
- 37 arquivos de observabilidade pura

**O que fazer:**

```bash
# 1. Backup
cp -r modules/monitoring modules/monitoring.backup

# 2. Criar estrutura em core/
mkdir -p core/monitoring
mkdir -p core/monitoring/{sentry,metrics,logs}

# 3. Mover arquivos
mv modules/monitoring/*.py core/monitoring/

# 4. Atualizar 2 imports em:
#    - modules/governance/ (→ from core.monitoring import...)
#    - modules/justice/ (→ from core.monitoring import...)

# 5. Validar imports
python -m py_compile core/monitoring/**/*.py

# 6. Rodar testes
pytest tests/ -k monitoring
```

**Testes específicos:**

- [ ] Imports em `modules/governance/` funcionam
- [ ] Imports em `modules/justice/` funcionam
- [ ] Não há `ImportError`
- [ ] Logs continuam sendo coletados

**Risco**: 🟢 Muito Baixo

---

### Etapa 1.2: `common/` → `core/utils/common/`

**Por quê?**

- "common" é utilitário compartilhado
- Importado por 5 módulos (base compartilhada)
- 26 arquivos de helpers/constants

**O que fazer:**

```bash
# 1. Criar estrutura
mkdir -p core/utils/common

# 2. Mover arquivos
mv modules/common/*.py core/utils/common/

# 3. Atualizar 5 imports em:
#    - modules/auth/
#    - modules/governance/
#    - modules/health/
#    - modules/schemas/
#    - modules/integration/

# 4. Pattern atualizado:
#    OLD: from modules.common import BaseModel
#    NEW: from core.utils.common import BaseModel
```

**Testes específicos:**

- [ ] 5 módulos importam corretamente
- [ ] Sem duplicação de código
- [ ] Testes de schemas passam
- [ ] Testes de integração passam

**Risco**: 🟢 Muito Baixo

---

## 🔴 FASE 2: Técnico com Dependências (Semana 2)

### Etapa 2.1: `auth/` → `core/auth/`

**⚠️ CRÍTICO: Importado por 5 módulos**

**Dependentes:**

1. `modules/citizenship/` (50 arquivos)
2. `modules/documents/` (21 arquivos)
3. `modules/analytics/` (7 arquivos)
4. `modules/finance/` (39 arquivos)
5. `modules/dashboard/` (15 arquivos)

**Total de arquivos afetados: ~140**

**O que fazer:**

```bash
# 1. Backup COMPLETO
git commit -m "Backup antes de migração auth/"

# 2. Criar estrutura
mkdir -p core/auth
mkdir -p core/auth/{models,services,utils}

# 3. Mover módulo
mv modules/auth/*.py core/auth/

# 4. SCRIPT AUTOMÁTICO: Atualizar todos os imports
python3 update_imports.py \
  --from "from modules.auth" \
  --to "from core.auth" \
  --recursive

# 5. Verificar imports
grep -r "from modules.auth" apps/backend/  # Deve retornar 0 resultados

# 6. Testes completos
pytest tests/ -x  # Parar no primeiro erro
pytest tests/ --tb=short  # Relatório detalhado
```

**Testes específicos:**

- [ ] Login endpoint funciona (`/api/auth/login`)
- [ ] JWT validation funciona
- [ ] 140+ arquivos com imports corrigidos
- [ ] Testes de autenticação: 100% passing
- [ ] Testes de integração com citizenship: passing
- [ ] Testes com documents: passing

**Risco**: 🟠 Médio (140 arquivos afetados, mas scripts automáticos)

**Plano de Rollback:**

```bash
git revert HEAD~1  # Volta antes da migração
```

---

## 🔵 FASE 3: Revisão Manual (Semana 3)

### 8 Módulos Indefinidos - Requer Decisão

| Módulo          | Arquivos | Dependências                  | Recomendação                           |
| --------------- | -------- | ----------------------------- | -------------------------------------- |
| **integration** | 35       | 0 importa, 3 importado        | ❓ Depende do contexto de negócio      |
| **dashboard**   | 15       | 1 importa (auth), 0 importado | 🎯 Negócio (fica em modules/)          |
| **social**      | 26       | 0 importa, 0 importado        | 🎯 Negócio (fica em modules/)          |
| **training**    | 16       | 0 importa, 0 importado        | 🎯 Negócio (fica em modules/)          |
| **internal**    | 12       | 0 importa, 0 importado        | ❓ Requer discussão com time           |
| **journeys**    | 5        | 0 importa, 0 importado        | 🎯 Negócio (fica em modules/)          |
| **reports**     | 11       | 0 importa, 0 importado        | ⚡ Utilitário (→ core/utils/reporting) |
| **urbanism**    | 10       | 0 importa, 1 importado        | 🎯 Negócio (fica em modules/)          |

**Ação recomendada:**

- [ ] Reunião com Product & Tech Lead
- [ ] Documentar decisão para cada um
- [ ] Executar migração se necessário (baixíssimo risco)

---

## 📈 Impacto Esperado

### Antes (Status Quo)

```
modules/
├── common/              ← Utilitário compartilhado
├── auth/                ← Técnico mas em modules/
├── monitoring/          ← Técnico mas em modules/
├── citizenship/ (50)    ← Negócio ✓
├── justice/ (48)        ← Negócio ✓
├── finance/ (39)        ← Negócio ✓
├── governance/ (38)     ← Negócio ✓
... (26 outros)

core/
├── auth.py              ← Duplicado!
├── health.py
├── logger.py
├── security.py
... (13 arquivos, desorganizado)
```

### Depois (Alvo)

```
modules/                 ← 21 domínios de negócio puro
├── citizenship/ (50)
├── justice/ (48)
├── finance/ (39)
├── governance/ (38)
... (17 outros)

core/                    ← Técnico organizado
├── auth/                ← Autenticação
├── monitoring/          ← Observabilidade
├── utils/
│   ├── common/          ← Compartilhado
│   └── helpers/
├── database/            ← BD
├── exceptions/          ← Exceções
└── ...
```

---

## 🔒 Validação Pré-Migração

- [ ] Todos os 729 arquivos têm backup
- [ ] Git status limpo (commit antes)
- [ ] Testes passando 100%
- [ ] CI/CD verde
- [ ] Database backups atualizados

---

## ✅ Validação Pós-Migração

### Cada Fase

- [ ] Nenhum arquivo duplicado
- [ ] Nenhum `ImportError`
- [ ] `pytest tests/ -x` passa 100%
- [ ] Lint clean: `pylint apps/backend/`
- [ ] Type checking: `mypy apps/backend/`
- [ ] Documentação atualizada

### Integração Completa

- [ ] Staging deployment sucesso
- [ ] Smoke tests passam
- [ ] Logs normais (Sentry limpo)
- [ ] Performance baseline mantida
- [ ] Equipe validou em staging

---

## 🛠️ Ferramentas & Scripts

### Script 1: `analyze_imports.py` ✅ Completo

Mapeia estrutura e dependências.

```bash
python3 migration_analyzer.py --save report.json
```

### Script 2: `update_imports.py` 🔄 A Criar

Atualiza imports automaticamente.

```bash
python3 update_imports.py \
  --from "from modules.auth" \
  --to "from core.auth" \
  --recursive \
  --backup
```

### Script 3: `validate_migration.py` 🔄 A Criar

Valida integridade pós-migração.

```bash
python3 validate_migration.py \
  --check-imports \
  --check-duplicates \
  --check-syntax
```

---

## 📊 Métricas de Sucesso

| Métrica                  | Antes | Depois | Target |
| ------------------------ | ----- | ------ | ------ |
| Imports `from core.*`    | 270   | 300+   | ✓      |
| Imports `from modules.*` | 287   | 250    | ✓      |
| Arquivos em `core/`      | 13    | 100+   | ✓      |
| Arquivos em `modules/`   | 716   | 616    | ✓      |
| Testes passando          | 95%   | 100%   | ✓      |
| Lint clean               | 90%   | 100%   | ✓      |

---

## 📚 Documentação a Criar

Após migração completar:

1. **CORE_STRUCTURE.md** - O que vai em core/ e por quê
2. **MIGRATION_LOG.md** - O que foi movido
3. **IMPORT_CONVENTIONS.md** - Novos padrões
4. **TROUBLESHOOTING.md** - Problemas comuns
5. **ROLLBACK_GUIDE.md** - Como voltar se necessário

---

## 👥 Responsabilidades

| Função          | Ação                             |
| --------------- | -------------------------------- |
| **Arquiteto**   | Validar escopo, aprovar decisões |
| **Tech Lead**   | Coordenar, revisar PRs           |
| **Dev 1**       | Executar Fase 1 + testes         |
| **Dev 2**       | Executar Fase 2 + testes         |
| **QA**          | Validar pós-cada-fase            |
| **DevOps**      | Deploy staging, CI/CD            |
| **Tech Writer** | Documentação                     |

---

## 🎬 Próximo Passo

**SEMANA 1 - SEG (Hoje):**

1. Executar backup completo

   ```bash
   tar czf backup-modules-core.tar.gz modules/ core/
   git commit -m "Backup completo antes de migração"
   ```

2. Criar scripts de atualização de imports

   ```bash
   # Scripts: update_imports.py, validate_migration.py
   ```

3. Testar Fase 1 em branch isolado

   ```bash
   git checkout -b feature/migrate-monitoring
   # Executar Etapa 1.1
   ```

4. Passar code review antes de merge

---

## 📋 Checklist Final

### Pré-Migração

- [ ] Backup completo testado
- [ ] Branch isolado criado
- [ ] Testes 100% passando
- [ ] CI/CD verde
- [ ] Time alinhado

### Durante

- [ ] Executar script de backup
- [ ] Mover estrutura
- [ ] Atualizar imports (auto)
- [ ] Validar sintaxe
- [ ] Rodar testes

### Pós-Migração

- [ ] Nenhum ImportError
- [ ] Testes 100%
- [ ] Lint clean
- [ ] Code review aprovado
- [ ] Merge para main
- [ ] Deploy staging

---

**Status**: 🟢 PRONTO PARA EXECUTAR **Risco Geral**: 🟡 Médio (controlável com scripts)
**Tempo Estimado**: 3 semanas **Benefício**: ✅ Arquitetura clara, manutenibilidade,
escalabilidade

---

_Documento gerado automaticamente baseado em análise real de 729 arquivos_
