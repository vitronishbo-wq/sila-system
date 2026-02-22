# 🔗 FASE 2A — Mapa de Dependências Críticas (Nível 2)

**Data de Geração:** 2025-11-20 **Foco:** Análise de Scripts Intermediários
**Estratégia:** Documentação de Risco + Pontos Críticos

---

## 📋 Visão Geral dos Scripts Nível 2

| #   | Script                        | Função                  | Risco      | Dependências       | Status              |
| --- | ----------------------------- | ----------------------- | ---------- | ------------------ | ------------------- |
| 1   | `clean_pendrive_safe.sh`      | Limpeza segura pendrive | 🔴 Alto    | /tmp, prompts      | ⚠️ Revisar          |
| 2   | `safe_root_reorganizer.sh`    | Reorganização segura    | 🔴 Alto    | find, logs, dirs   | ⚠️ Revisar          |
| 3   | `cleanup_temp_files.sh`       | Limpeza cache/temp      | 🟠 Médio   | Docker, logs       | ⚠️ Testar           |
| 4   | `restructure_project.sh`      | Reestruturação          | 🟠 Médio   | Diretórios         | ⚠️ Validar          |
| 5   | `cleanup_project.sh`          | Limpeza de projeto      | 🔴 Alto    | Movimentação files | ⚠️ Backup           |
| 6   | `repair_all_simple.sh`        | Reparação simples       | 🔴 Alto    | Docker Compose     | ⚠️ Testar           |
| 7   | `consolidate_root_scripts.sh` | Consolidação raiz       | 🟠 Médio   | Variáveis path     | ⚠️ Revisar          |
| 8   | `cleanup_obsolete.sh`         | Limpeza obsoleta        | 🔴 Alto    | Múltiplas ops      | ⚠️ Análise profunda |
| 9   | `repair_all_runner.sh`        | Runner de reparação     | 🔴 Alto    | Backup, scripts    | ⚠️ Validar          |
| 10  | `cleanup_all_backups.sh`      | Limpeza backups         | 🔴 Crítico | Remoção files      | ⚠️ CUIDADO          |
| 11  | `structure-guard.sh`          | Guardião estrutura      | 🟠 Médio   | Módulos            | ⚠️ Testar           |
| 12  | `validate_migrations.sh`      | Validação migrations    | 🔴 Alto    | Banco de dados     | ⚠️ Testar BD        |
| 13  | `optimize_storage.sh`         | Otimização disco        | 🟠 Médio   | Análise disco      | ⚠️ Monitorar        |
| 14  | `analyze_code_quality.sh`     | Análise qualidade       | 🟢 Baixo   | Linters            | ✅ Integrar         |

---

## 🔴 Crítico: Risco Alto + Operações Destrutivas

### 1. `cleanup_all_backups.sh` — MÁXIMO CUIDADO

**Função:** Remoção de arquivos de backup

**Linhas Críticas:**

```bash
Linhas 25-70: rm -rf **/*.bak *.bak.*
```

**Risco:**

- ❌ Deletar permanentemente backups críticos
- ❌ Sem recuperação possível
- ❌ Impacto destrutivo irreversível

**Dependências:**

- Pattern matching com wildcards
- Remoção recursiva
- Sem confirmação interativa?

**Recomendação:**

```
⚠️ NUNCA consolidar ou mover sem:
   1. Validação extrema de patterns
   2. Confirmação interativa obrigatória
   3. Log de remoção permanente
   4. Backup prévio de backups
```

---

### 2. `cleanup_project.sh` — RISCO ALTO

**Função:** Limpeza e movimentação de arquivos no projeto

**Linhas Críticas:**

```bash
Linhas 27-76: Movimentação/remoção de diretórios
```

**Risco:**

- ❌ Pode mover/deletar arquivos críticos
- ❌ Pode quebrar estrutura do projeto
- ❌ Impacto em build/deploy

**Dependências:**

- Conhecimento de estrutura projeto
- Permissões de write em dirs críticos
- Sem rollback automático

**Recomendação:**

```
⚠️ Antes de executar:
   1. Fazer backup completo
   2. Executar em ambiente dev primeiro
   3. Validar estrutura pós-execução
   4. Testar build/deploy
```

---

### 3. `safe_root_reorganizer.sh` — RISCO ALTO

**Função:** Reorganização segura da raiz do projeto

**Linhas Críticas:**

```bash
Linha 154:  Redirecionamento de log
Linha 230:  Comando find recursivo
Linha 421:  Mensagens de sucesso
```

**Risco:**

- ❌ Find recursivo pode afetar todos os files
- ❌ Reorganização sem validação
- ❌ Logs podem não capturar erros

**Dependências:**

- Acesso a raiz do projeto
- Permissões para mover estrutura
- Validação de integridade pós-move

**Recomendação:**

```
⚠️ Validar:
   1. Todos os paths estão corretos
   2. Find patterns são específicos
   3. Logs capturam todas as operações
   4. Rollback é possível
```

---

### 4. `repair_all_runner.sh` — RISCO ALTO

**Função:** Execução sequencial de reparações

**Linhas Críticas:**

```bash
Linhas 59-130:  Backup Docker Compose
Linhas 200-356: Geração de tipos
```

**Risco:**

- ❌ Sequência crítica pode falhar parcialmente
- ❌ Backup podem ficar inconsistentes
- ❌ Tipos gerados podem estar errados

**Dependências:**

- Docker Compose funcionando
- Scripts de reparação existindo
- Tipo generation correto

**Recomendação:**

```
⚠️ Testar em dev com:
   1. Backup prévio do Docker Compose
   2. Execução step-by-step
   3. Validação de cada etapa
   4. Comparação de tipos gerados
```

---

### 5. `cleanup_temp_files.sh` — RISCO MÉDIO-ALTO

**Função:** Limpeza de arquivos temporários

**Linhas Críticas:**

```bash
Linhas 38, 53:  Limpeza de cache
Linhas 66, 83:  Remoção Docker
Linha 97:       Remoção de logs
```

**Risco:**

- ⚠️ Pode afetar aplicações rodando
- ⚠️ Logs podem ser perdidos
- ⚠️ Docker pode ficar instável

**Dependências:**

- Docker rodando ou não
- Aplicações usando cache
- Monitoramento de logs ativo

**Recomendação:**

```
⚠️ Executar apenas:
   1. Com aplicação parada
   2. Após fazer backup de logs
   3. Validar Docker stability pós-limpeza
   4. Monitorar sistema pós-execução
```

---

## 🟠 Alto Risco: Operações Estruturais

### 6. `safe_root_reorganizer.sh` (continua)

**Dependências Internas:**

- Verificação de montagem /tmp (linha 38)
- Prompt de confirmação (linha 118)
- Redirecionamento seguro de logs

**Pontos de Falha:**

```
1. Se /tmp não está montado → Falha
2. Se prompt é interrompido → Estado inconsistente
3. Se logs não gravam → Sem auditoria
```

---

### 7. `repair_all_simple.sh` — RISCO ALTO

**Função:** Reparação simples (backup Docker Compose)

**Linhas Críticas:**

```bash
Linha 33: Docker Compose backup
```

**Dependências:**

- Docker Compose instalado
- Arquivo docker-compose.yml presente
- Espaço em disco para backup

**Pontos de Falha:**

```
1. Docker Compose corrompido → Backup inútil
2. Espaço em disco insuficiente → Falha
3. Permissões de backup insuficientes → Falha
```

---

### 8. `validate_migrations.sh` — RISCO ALTO

**Função:** Validação de migrations de BD

**Dependências:**

- Banco de dados rodando
- Migrations aplicadas
- Schema compatível

**Pontos de Falha:**

```
1. Banco offline → Falha
2. Migrations inconsistentes → Falha
3. Schema incompatível → Falha
```

---

## 🟢 Médio-Baixo: Operações Seguras

### 9-14. Scripts com Risco Médio-Baixo

- `restructure_project.sh` — Validar paths antes
- `consolidate_root_scripts.sh` — Revisar variáveis
- `structure-guard.sh` — Testar em dev
- `optimize_storage.sh` — Monitorar
- `analyze_code_quality.sh` — Baixo risco, integrar CI/CD

---

## 📊 Matriz de Decisão Fase 2A

```
┌────────────────────────────────────────────────────────┐
│ DECISÃO: Consolidar ou Não Nível 2?                  │
├────────────────────────────────────────────────────────┤
│ ❌ NÃO CONSOLIDAR AGORA:                              │
│    • cleanup_all_backups.sh (risco destrutivo)        │
│    • cleanup_project.sh (risco estrutural)            │
│    • repair_all_runner.sh (sequência crítica)         │
│    • validate_migrations.sh (BD crítica)              │
│                                                        │
│ ⚠️  CONSOLIDAR COM CUIDADO:                           │
│    • safe_root_reorganizer.sh (docs + testes)        │
│    • cleanup_temp_files.sh (testes de isolamento)     │
│    • repair_all_simple.sh (validação Docker)          │
│                                                        │
│ ✅ CONSOLIDAR SEGURO:                                 │
│    • analyze_code_quality.sh (baixo risco)            │
│    • optimize_storage.sh (monitoramento)              │
│    • structure-guard.sh (validação modular)           │
└────────────────────────────────────────────────────────┘
```

---

## ✅ Checklist Fase 2A — Validação Nível 2

- [x] Todos os 14 scripts Nível 2 analisados
- [x] Dependências críticas documentadas
- [x] Pontos de risco identificados
- [x] Recomendações de ação geradas
- [ ] Validação em ambiente dev
- [ ] Testes de não-regressão
- [ ] Aprovação do time de core

---

## 🎯 Gate para Fase 2B

**Critério:** Mínimo 5 scripts Nível 2 aprovados para consolidação

**Atual:**

- ✅ Aprovados para consolidação: 3 scripts (com cuidado)
- ⚠️ Bloqueados temporariamente: 5 scripts (risco alto)
- 🔍 Sob análise detalhada: 6 scripts

**Status:** ⏳ Aguardando testes em dev

---

## 📚 Documentação Complementar

- 📄 `FASE_2_SCRIPTS_CRITICOS_NIVEL1.md` — Nível 1 intocáveis
- 📄 `FASE_2_MATRIZ_CONSOLIDACAO_NIVEL3.md` — Nível 3 candidatos
- 📄 `FASE_2_SUMARIO_ANALISE.md` — Visão consolidada

---

**Mapa de Dependências — Fase 2A** **Data:** 2025-11-20 **Status:** ✅ MAPEAMENTO
COMPLETO
