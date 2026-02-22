# 🎯 README: Migração modules/ → core/ (ETAPA 5)

**Status**: ✅ PLANEJAMENTO COMPLETO | ⏳ EXECUÇÃO PRÓXIMA SEMANA **Criado**: 2024
**Responsável**: Time Backend (Arquiteto + 2 Devs) **Duração Estimada**: 3 semanas

---

## 🚀 O Que Precisa Saber em 2 Minutos

### Problema Atual

```
modules/          → 32 domínios desorganizados, 729 arquivos
core/             → 13 arquivos soltos, sem estrutura
imports           → 287 de modules + 270 de core + 126 relativos
documentação      → Nenhuma clara
```

### Solução

```
modules/          → 21 domínios de negócio PURO
core/             → ~100 arquivos TÉCNICO organizado
imports           → 300+ de core, 250 de modules, 0 relativos
documentação      → STRUCTURE.md, PATTERNS.md, ONBOARDING.md
```

### Timeline

```
SEMana 1: Fase 1 - Técnico Baixo Risco      🟢 45 min
SEMANA 2: Fase 2 - Técnico Médio Risco     🟠 30 min
SEMANA 2: Fase 3 - Crítico (auth)          🔴 90 min
SEMANA 3: Testes + Documentação + Deploy   🟢 ~
```

### Resultado

✅ Arquitetura clara | ✅ Manutenibilidade | ✅ Escalabilidade

---

## 📚 Documentação

### 🎓 Sua Primeira Leitura

1. **`ETAPA_5_SUMMARY.md`** (5 min) ← COMECE AQUI

   - Overview visual do que foi descoberto
   - Arquivos criados
   - Próximos passos

2. **`NAVIGATION_INDEX.md`** (3 min) ← DEPOIS AQUI
   - Mapa de todos os recursos
   - Como escolher o que ler baseado em seu papel

### 👔 Para Tech Lead

- **`MIGRATION_EXECUTIVE_PLAN.md`** (20 min)
  - Cronograma executivo
  - Riscos por fase
  - Métricas de sucesso
  - Checklist

### 👨‍💻 Para Developers

- **`MIGRATION_EXECUTION_GUIDE.md`** (30 min + 3h execução)
  - Passo-a-passo com comandos prontos
  - Checklist para cada etapa
  - Troubleshooting

### 🔍 Para Entender os Dados

- **`MIGRATION_ANALYSIS_INSIGHTS.md`** (10 min)
  - O que foi descoberto
  - Problemas identificados
  - Recomendações

---

## 🔧 Scripts Criados

### Execute Em Ordem:

1️⃣ **Analisar** (já executado)

```bash
python3 migration_analyzer.py --save report.json
```

2️⃣ **Classificar** (já executado)

```bash
python3 module_classifier.py --export classifications.json
```

3️⃣ **Atualizar** (antes de cada fase)

```bash
python3 update_imports.py \
  --from "modules.monitoring" \
  --to "core.monitoring" \
  --backup --recursive
```

4️⃣ **Validar** (após cada fase)

```bash
python3 validate_migration.py --check-all
```

---

## 📊 Dados Descobertos

```
32 módulos identificados
729 arquivos Python
3.9 MB de código

Classificação:
  🔧 TÉCNICO (2): auth (18), monitoring (37) → move to core/
  🎯 NEGÓCIO (21): citizenship (50), justice (48), finance (39), ...
  ⚡ UTILIDADE (1): common (26) → move to core/utils/
  ❓ INDEFINIDO (8): dashboard, integration, internal, journeys, reports, social, training, urbanism

Dependências:
  auth importado por 5 módulos (140+ arquivos afetados)
  monitoring importado por 2 módulos
  common importado por 5 módulos
```

---

## 🎯 Fases de Execução

### FASE 1 - MONITORAMENTO ✅ Pronto

- **Arquivos**: 37 + 2 dependentes
- **Risco**: 🟢 Muito Baixo
- **Tempo**: 45 minutos
- **Comando**:
  ```bash
  python3 update_imports.py \
    --from "modules.monitoring" \
    --to "core.monitoring" \
    --backup --recursive
  ```

### FASE 2 - COMMON ✅ Pronto

- **Arquivos**: 26 + 5 dependentes
- **Risco**: 🟢 Muito Baixo
- **Tempo**: 30 minutos
- **Comando**:
  ```bash
  python3 update_imports.py \
    --from "modules.common" \
    --to "core.utils.common" \
    --backup --recursive
  ```

### FASE 3 - AUTH ✅ Pronto

- **Arquivos**: 18 + 140 dependentes
- **Risco**: 🔴 Alto
- **Tempo**: 90 minutos
- **Requer**: Validação agressiva (testes 100%)
- **Comando**:
  ```bash
  python3 update_imports.py \
    --from "modules.auth" \
    --to "core.auth" \
    --backup --recursive
  ```

---

## ✅ Checklist Pré-Execução

- [ ] Leu `ETAPA_5_SUMMARY.md`
- [ ] Leu `NAVIGATION_INDEX.md`
- [ ] Aprovou cronograma com Tech Lead
- [ ] Git repositório limpo (`git status`)
- [ ] Testes passando (`pytest tests/ -q`)
- [ ] Backup criado (`tar czf backup.tar.gz apps/backend/`)
- [ ] Branch isolado criado (`git checkout -b feature/migrate-phase1`)

---

## 🚀 Como Começar

### Option A: Rápido (~5 min)

```bash
# 1. Ler overview
cat ETAPA_5_SUMMARY.md

# 2. Ver dados
python3 module_classifier.py | head -50

# 3. Pronto!
```

### Option B: Detalhado (~2 horas)

```bash
# 1. Ler documentação
less NAVIGATION_INDEX.md
less MIGRATION_EXECUTIVE_PLAN.md

# 2. Estudar guia de execução
less MIGRATION_EXECUTION_GUIDE.md

# 3. Preparar ambiente
git checkout -b feature/test-phase1
tar czf backup_phase1.tar.gz apps/backend/

# 4. DRY RUN
python3 update_imports.py \
  --from "modules.monitoring" \
  --to "core.monitoring" \
  --dry-run

# 5. Se OK, executar para real seguindo guia
```

---

## 📈 Métricas de Sucesso

### Antes

| Métrica                 | Valor |
| ----------------------- | ----- |
| core/ arquivos          | 13    |
| modules/ arquivos       | 716   |
| imports from core.\*    | 270   |
| imports from modules.\* | 287   |
| imports relativos       | 126   |

### Depois (Target)

| Métrica                 | Valor |
| ----------------------- | ----- |
| core/ arquivos          | 100+  |
| modules/ arquivos       | 616   |
| imports from core.\*    | 300+  |
| imports from modules.\* | 250   |
| imports relativos       | 0     |

---

## 🆘 Algo Deu Errado?

### "Erro de import"

```bash
# Solução
python3 validate_migration.py --check-imports
# Se FAIL, executar:
git revert HEAD~1
```

### "Arquivo não encontrado após migração"

```bash
# Verificar
ls apps/backend/core/monitoring/  # Deve existir
grep -r "from core.monitoring" apps/backend/  # Deve ter matches

# Se não existir, copiar manualmente:
cp apps/backend/modules/monitoring/*.py apps/backend/core/monitoring/
```

### "Testes falhando"

```bash
# Debug
pytest tests/ -x -v --tb=short

# Se import error:
python3 validate_migration.py --check-imports

# Se lógica error:
# Revisar teste e import manualmente
```

### "Último recurso: Reverter"

```bash
git revert HEAD~1
# Volta para estado anterior em < 5 minutos
```

---

## 📞 Contato & Suporte

| Situação            | Ação                                                     |
| ------------------- | -------------------------------------------------------- |
| Entender contexto   | Leia: `ETAPA_5_SUMMARY.md`                               |
| Planejar cronograma | Leia: `MIGRATION_EXECUTIVE_PLAN.md`                      |
| Executar Fase 1     | Siga: `MIGRATION_EXECUTION_GUIDE.md`                     |
| Entender dados      | Leia: `MIGRATION_ANALYSIS_INSIGHTS.md`                   |
| Validar migração    | Rode: `python3 validate_migration.py`                    |
| Troubleshooting     | Leia: `MIGRATION_EXECUTION_GUIDE.md` → "Troubleshooting" |
| Dúvida técnica      | Pergunte ao Tech Lead                                    |

---

## 🏆 Arquivos Criados

### Scripts (4 arquivos)

```
migration_analyzer.py      # Mapeia estrutura (já executado)
module_classifier.py       # Classifica módulos (já executado)
update_imports.py          # Atualiza imports (pronto para usar)
validate_migration.py      # Valida integridade (pronto para usar)
```

### Documentação (5 arquivos)

```
ETAPA_5_SUMMARY.md                    # Este resumo visual
MIGRATION_EXECUTIVE_PLAN.md           # Plano executivo
MIGRATION_EXECUTION_GUIDE.md          # Passo-a-passo
MIGRATION_ANALYSIS_INSIGHTS.md        # Dados descobertos
NAVIGATION_INDEX.md                   # Mapa de recursos
```

### Dados (2 arquivos)

```
migration_analysis_report.json        # Análise completa (30 KB)
module_classifications.json           # Classificações (20 KB)
```

---

## 📋 Próximas Ações

### Hoje

- [ ] Leia este README
- [ ] Leia `ETAPA_5_SUMMARY.md`
- [ ] Compartilhe com Tech Lead

### SEG (Semana 1)

- [ ] Kick-off reunião
- [ ] Aprove Fase 1
- [ ] Designar Dev 1

### TER-QUA

- [ ] Dev 1 testa Fase 1 em branch isolado
- [ ] Code review
- [ ] Merge se OK

### QUI

- [ ] Executar Fase 1 em main
- [ ] Testes: 100% passando
- [ ] Deploy staging

### SEG (Semana 2)

- [ ] Executar Fase 2
- [ ] Revisão manual dos 8 indefinidos
- [ ] Começar Fase 3

### QUI (Semana 2-3)

- [ ] Executar Fase 3 (auth)
- [ ] Validação agressiva
- [ ] Deploy staging

### SEX (Semana 3)

- [ ] Documentação final
- [ ] Onboarding novo padrão
- [ ] Pronto!

---

## 🎉 Resumo

```
ANTES: Confusão, "quantos módulos temos mesmo?"
    ↓
ANÁLISE: 32 módulos, 729 arquivos, 3.9 MB encontrados
    ↓
CLASSIFICAÇÃO: 2 técnico, 21 negócio, 1 utilidade, 8 indefinidos
    ↓
PLANEJAMENTO: 3 fases, 3 semanas, cronograma claro
    ↓
AUTOMAÇÃO: 4 scripts prontos (analyze, classify, update, validate)
    ↓
DOCUMENTAÇÃO: 5 docs completas, 120+ KB
    ↓
PRONTO: Executar Fase 1 amanhã ou próxima segunda
    ↓
RESULTADO: Arquitetura clara, manutenibilidade, escalabilidade ✅
```

---

## 📖 Começar Leitura Agora

```bash
# 1. Visão Geral (5 min)
cat ETAPA_5_SUMMARY.md

# 2. Mapa de Navegação (3 min)
cat NAVIGATION_INDEX.md

# 3. Detalhes (20 min, choose one)
cat MIGRATION_EXECUTIVE_PLAN.md    # Se you're a lead
cat MIGRATION_EXECUTION_GUIDE.md   # Se you'll execute
cat MIGRATION_ANALYSIS_INSIGHTS.md # Se you want data
```

---

**Bem-vindo à Etapa 5! Migração pronta para começar! 🚀**

_Perguntas? Revise a documentação acima ou contacte seu Tech Lead_
