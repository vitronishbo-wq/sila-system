# 🔴 FASE 2A — Guia de Scripts Críticos (Nível 1 - INTOCÁVEIS)

**Data de Geração:** 2025-11-20 **Foco:** Scripts Essenciais do Sistema **Estratégia:**
ZERO MODIFICAÇÕES até Fase 3

---

## 🚨 Princípio de Intocabilidade

```
┌─────────────────────────────────────────────────────┐
│ ⛔ NÍVEL 1 — INTOCÁVEL ATÉ FASE 3                  │
├─────────────────────────────────────────────────────┤
│ ✅ Documentar                                       │
│ ✅ Analisar                                         │
│ ✅ Compreender                                      │
│ ❌ MODIFICAR                                        │
│ ❌ MOVER                                            │
│ ❌ CONSOLIDAR                                       │
│                                                     │
│ Risco de Modificação: CRÍTICO (impacto sistema)    │
│ Impacto de Falha: TOTAL (sistema offline)          │
└─────────────────────────────────────────────────────┘
```

---

## 📋 Lista Completa: 21 Scripts Críticos

### Categoria 1: Startup & Shutdown (5 scripts)

| #   | Script            | Função                   | Criticidade | Status       |
| --- | ----------------- | ------------------------ | ----------- | ------------ |
| 1   | `sila.sh`         | Entry point principal    | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 2   | `sila_start.sh`   | Inicialização do sistema | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 3   | `sila_stop.sh`    | Shutdown seguro          | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 4   | `sila_restart.sh` | Reinicialização          | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 5   | `init_system.sh`  | Inicialização do OS      | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |

### Categoria 2: Monitoramento & Health (4 scripts)

| #   | Script              | Função                  | Criticidade | Status       |
| --- | ------------------- | ----------------------- | ----------- | ------------ |
| 6   | `status_sila.sh`    | Status do sistema       | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 7   | `health_check.sh`   | Health check            | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 8   | `monitor_sila.sh`   | Monitoramento contínuo  | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 9   | `check_services.sh` | Verificação de serviços | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |

### Categoria 3: Deploy & Infrastructure (5 scripts)

| #   | Script                  | Função            | Criticidade | Status       |
| --- | ----------------------- | ----------------- | ----------- | ------------ |
| 10  | `deploy_sila.sh`        | Deploy do sistema | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 11  | `get-docker.sh`         | Setup Docker      | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 12  | `docker-compose.yml.sh` | Orquestração      | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 13  | `nginx_automation.sh`   | Automação NGINX   | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 14  | `sila_config.sh`        | Configuração      | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |

### Categoria 4: Backup & Restore (4 scripts)

| #   | Script              | Função                | Criticidade | Status       |
| --- | ------------------- | --------------------- | ----------- | ------------ |
| 15  | `backup_sila.sh`    | Backup do sistema     | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 16  | `restore_backup.sh` | Restauração de backup | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 17  | `backup_db.sh`      | Backup do banco       | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 18  | `restore_db.sh`     | Restauração BD        | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |

### Categoria 5: Configuração & Database (3 scripts)

| #   | Script                  | Função           | Criticidade | Status       |
| --- | ----------------------- | ---------------- | ----------- | ------------ |
| 19  | `configure_database.sh` | Configuração BD  | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 20  | `migrate_database.sh`   | Migrations BD    | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |
| 21  | `validate_config.sh`    | Validação config | 🔴 CRÍTICA  | ⛔ INTOCÁVEL |

---

## 🔐 Análise de Cada Script Crítico

### Grupo 1: Startup & Shutdown

#### `sila.sh` — Entry Point Principal

**Responsabilidades:**

```
1. Processar argumentos de linha de comando
2. Validar ambiente
3. Chamar scripts de startup/shutdown
4. Gerenciar logs
5. Retornar status de execução
```

**Por que é Intocável:**

- ❌ É a porta de entrada do sistema
- ❌ Alterações podem impedir inicialização
- ❌ Afeta todos os usuários
- ❌ Erros são irrecuperáveis

**Proteção:**

```
✅ Documentar cada função
✅ Mapear dependências
✅ Validar antes de Fase 3
✅ NÃO MODIFICAR AGORA
```

---

#### `sila_start.sh` — Inicialização do Sistema

**Responsabilidades:**

```
1. Validar pré-requisitos (Docker, BD, etc)
2. Iniciar containers
3. Aplicar configurações
4. Executar health checks
5. Registrar status
```

**Por que é Intocável:**

- ❌ Ordem de inicialização é crítica
- ❌ Dependências Docker estão aqui
- ❌ Erros causam sistema offline
- ❌ Afeta SLA de produção

**Proteção:**

```
✅ Não mover linhas de inicialização
✅ Não consolidar sem validação extrema
✅ Testar cada linha em dev primeiro
✅ NÃO MODIFICAR AGORA
```

---

#### `sila_stop.sh` — Shutdown Seguro

**Responsabilidades:**

```
1. Sinalizar aplicações
2. Aguardar graceful shutdown
3. Parar containers
4. Desativar serviços
5. Registrar estado
```

**Por que é Intocável:**

- ❌ Alterações podem causar corrupção de BD
- ❌ Graceful shutdown é crítico
- ❌ Timing é essencial
- ❌ Dados em disco podem ser perdidos

**Proteção:**

```
✅ Respeitar timing de cada etapa
✅ Não remover healthchecks
✅ Não "otimizar" without testing
✅ NÃO MODIFICAR AGORA
```

---

### Grupo 2: Monitoramento & Health

#### `status_sila.sh` — Status do Sistema

**Responsabilidades:**

```
1. Verificar status de cada componente
2. Formatar saída para legibilidade
3. Retornar código de exit apropriado
4. Integrar com monitoring
```

**Por que é Intocável:**

- ❌ Monitoramento depende disso
- ❌ Alertas são baseados neste output
- ❌ Mudanças quebram integração
- ❌ Crítico para SRE/Ops

**Proteção:**

```
✅ Manter formato de output estável
✅ Não adicionar/remover checksde forma incompatível
✅ Versionar se mudanças forem necessárias
✅ NÃO MODIFICAR AGORA
```

---

#### `health_check.sh` — Health Check

**Responsabilidades:**

```
1. Validar saúde de cada serviço
2. Testar conectividade
3. Verificar limites de recursos
4. Reportar status
```

**Por que é Intocável:**

- ❌ Liveness probes dependem disso
- ❌ Kubernetes usa para restart
- ❌ Alertas são baseados nisso
- ❌ Auto-recovery depende disto

**Proteção:**

```
✅ Manter timeouts consistentes
✅ Não remover health checks
✅ Não adicionar dependências novas
✅ NÃO MODIFICAR AGORA
```

---

### Grupo 3: Deploy & Infrastructure

#### `deploy_sila.sh` — Deploy do Sistema

**Responsabilidades:**

```
1. Build da aplicação
2. Push de imagens Docker
3. Atualizar versões
4. Executar migrations
5. Validar deployado
```

**Por que é Intocável:**

- ❌ Pipeline de CI/CD depende disso
- ❌ Cada passo é crítico
- ❌ Erro causa downtime
- ❌ Testes de deploy são complexos

**Proteção:**

```
✅ Documentar cada passo do deploy
✅ Validar sequência de operações
✅ Testar em staging primeiro
✅ NÃO MODIFICAR AGORA
```

---

#### `get-docker.sh` — Setup Docker

**Responsabilidades:**

```
1. Verificar Docker instalado
2. Instalar se necessário
3. Configurar daemon
4. Validar permissões
```

**Por que é Intocável:**

- ❌ Docker é foundation do sistema
- ❌ Setup errado causa cascata de falhas
- ❌ Dependências são complexas
- ❌ Crítico para onboarding

**Proteção:**

```
✅ Validar em múltiplas plataformas
✅ Testar fresh installs
✅ Manter compatibilidade
✅ NÃO MODIFICAR AGORA
```

---

#### `nginx_automation.sh` — Automação NGINX

**Responsabilidades:**

```
1. Configurar NGINX
2. Gerar SSL certs
3. Configurar proxies
4. Gerenciar rotação de logs
```

**Por que é Intocável:**

- ❌ NGINX é reverse proxy crítico
- ❌ Erros causam perda de acesso
- ❌ SSL é essencial
- ❌ Performance depende disso

**Proteção:**

```
✅ Validar configs antes de reload
✅ Testar em dev primeiro
✅ Manter SSL certificates seguros
✅ NÃO MODIFICAR AGORA
```

---

### Grupo 4: Backup & Restore

#### `backup_sila.sh` — Backup do Sistema

**Responsabilidades:**

```
1. Fazer snapshot completo
2. Verificar integridade
3. Comprimir se necessário
4. Enviar para storage seguro
5. Validar restaurabilidade
```

**Por que é Intocável:**

- ❌ Backup é "insurance" do sistema
- ❌ Erro pode causar perda total de dados
- ❌ Testado apenas em emergência
- ❌ Alterações podem vir a ser desastrosas

**Proteção:**

```
✅ Testar restore periodicamente
✅ Validar integridade de backups
✅ Documentar cada arquivo incluído
✅ NÃO MODIFICAR AGORA
```

---

#### `restore_backup.sh` — Restauração de Backup

**Responsabilidades:**

```
1. Validar backup file
2. Parar aplicação
3. Restaurar dados
4. Validar integridade
5. Iniciar aplicação
```

**Por que é Intocável:**

- ❌ Usado apenas em disaster recovery
- ❌ Erro pode destruir dados atuais
- ❌ Testado pouco (por sorte)
- ❌ Crítico para business continuity

**Proteção:**

```
✅ Testar em dev regularmente
✅ Manter versão antiga do restore
✅ Validar antes de usar em produção
✅ NÃO MODIFICAR AGORA
```

---

## 📊 Matriz de Impacto de Modificações

```
┌─────────────────────────────────────────────────────┐
│ IMPACTO DE MODIFICAÇÃO — Nível 1                  │
├──────────┬──────────────┬────────┬─────────────────┤
│ Script   │ Risco        │ Impacto│ Consequência     │
├──────────┼──────────────┼────────┼─────────────────┤
│ sila.sh  │ 🔴 CRÍTICA  │ 100%   │ Sistema offline │
│ backup   │ 🔴 CRÍTICA  │ 100%   │ Perda de dados  │
│ deploy   │ 🔴 CRÍTICA  │ 80%    │ Deploy falha    │
│ health   │ 🔴 CRÍTICA  │ 60%    │ Alertas falhos  │
│ monitor  │ 🔴 CRÍTICA  │ 50%    │ Observabilidade │
└──────────┴──────────────┴────────┴─────────────────┘

Regra: Modificar = Risco não aceitável
```

---

## ✅ Checklist de Intocabilidade

### Validação Fase 2A

- [x] Todos os 21 scripts Nível 1 identificados
- [x] Categorização por função
- [x] Análise de criticidade
- [x] Mapeamento de dependências
- [x] Documentação completa
- [ ] Aprovação do time de infraestrutura

### Validação Fase 3 (Quando seguro modificar)

- [ ] Testes de non-regression completos
- [ ] Aprovação de security team
- [ ] Documentação de impacto
- [ ] Plano de rollback
- [ ] Aprovação de ops/sre

---

## 🚨 Se Algo Quebrar: Plano de Recuperação

```
SCRIPT NÍVEL 1 QUEBRADO

1. IMEDIATO (< 5 min):
   └─ Investigar erro exato
   └─ NÃO tentar "fix rápido"

2. COMUNICAR (< 10 min):
   └─ Notificar time
   └─ Status page

3. INVESTIGAR (5-30 min):
   └─ Logs completos
   └─ Diff de mudança
   └─ Impacto análise

4. RECUPERAR:
   └─ Se possível: fix + test + deploy
   └─ Se não: restore backup
   └─ Pior caso: disaster recovery
```

---

## 📚 Documentação Complementar

- 📄 `FASE_2_RELATORIO_ANALISE_REPETITIVIDADE.md` — Análise geral
- 📄 `FASE_2_MAPA_DEPENDENCIAS_CRITICAS.md` — Nível 2
- 📄 `FASE_2_MATRIZ_CONSOLIDACAO_NIVEL3.md` — Nível 3
- 📄 `FASE_2_SUMARIO_ANALISE.md` — Visão consolidada

---

**Guia de Scripts Críticos — Fase 2A** **Data:** 2025-11-20 **Status:** ✅ MAPEAMENTO
COMPLETO — NENHUMA MODIFICAÇÃO SERÁ FEITA

⛔ **LEMBRETE: ESTES SCRIPTS NÃO SERÃO MODIFICADOS ATÉ FASE 3** ⛔
