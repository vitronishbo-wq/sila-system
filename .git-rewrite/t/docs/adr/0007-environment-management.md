# ADR-0007: Gestão de Ambientes - Estratégia Centralizada para Desenvolvimento, Staging e Produção

**Status:** Aceito **Data:** 2025-10-26 **Decisores:** Marcelo Truman, Equipe de DevOps,
Equipe de Configuração **Revisores:** Admin SILA, Equipe de Segurança

---

## 📋 Contexto

O projeto SILA apresentava problemas críticos na gestão de ambientes e configurações:

- **Configurações Espalhadas**: `.env` em múltiplos locais com valores inconsistentes
- **Segurança Fraca**: Senhas e secrets hardcoded em vários arquivos
- **Dificuldade de Deploy**: Cada ambiente exigia configuração manual
- **Ambientes Inconsistentes**: Desenvolvimento, staging e produção com diferenças não
  documentadas
- **Risco de Produção**: Configurações de desenvolvimento acidentalmente em produção

Com 900+ serviços e múltiplos ambientes, essa abordagem se tornaria um risco operacional
catastrófico.

---

## 🎯 Decisão

**Nós decidimos implementar uma estratégia centralizada de gestão de ambientes:**

### 1. Estrutura de Ambientes Padronizada

```
config/
├── .env.example          # Template completo com documentação
├── .env.development      # Configurações de desenvolvimento
├── .env.staging          # Configurações de staging/homologação
├── .env.production       # Configurações de produção
└── config_manager.py     # Gestor central de configurações
```

### 2. Gestão Centralizada de Secrets

- **Development**: Secrets simples para desenvolvimento rápido
- **Staging**: Secrets de complexidade média para testes realistas
- **Production**: Secrets robustos com rotação automática via Vault

### 3. Validação Automática

- **Schema Validation**: Validação de todas as variáveis de ambiente
- **Type Checking**: Tipagem forte para configurações
- **Dependency Validation**: Verificação de dependências entre variáveis

### 4. Deploy por Ambiente

- **Environment Detection**: Detecção automática do ambiente atual
- **Configuration Loading**: Carregamento automático das configurações corretas
- **Validation at Startup**: Validação no startup da aplicação

---

## ✅ Consequências

### Positivas

- **Consistência**: Todos os ambientes seguem o mesmo padrão
- **Segurança**: Secrets gerenciados de forma segura e centralizada
- **Deploy Simplificado**: Deploy automático por ambiente
- **Debugging Facilitado**: Configurações documentadas e validadas
- **Zero Configuration**: Novos desenvolvedores prontos em minutos
- **Compliance**: Atende requisitos de auditoria e segurança

### Negativas

- **Complexidade Inicial**: Setup mais complexo que `.env` simples
- **Curva de Aprendizagem**: Equipe precisa aprender novos padrões
- **Dependência de Ferramentas**: Requer ferramentas de gestão de secrets

### Neutras

- **Overhead**: Pequeno overhead de validação e gestão
- **Flexibilidade**: Menos flexibilidade para configurações ad-hoc

---

## 🔄 Implementação

### Passos

1. **Environment Structure**: Criar estrutura padronizada de diretórios
2. **Config Manager**: Implementar gestor central de configurações
3. **Schema Definition**: Definir schema completo de variáveis
4. **Validation Scripts**: Criar scripts de validação automática
5. **Secrets Integration**: Integrar com secrets manager (Vault)
6. **Deploy Automation**: Automatizar deploy por ambiente
7. **Documentation**: Documentar todas as variáveis e processos

### Responsáveis

- **Coordenação:** Marcelo Truman (DevOps Lead)
- **Configuração:** Equipe de Configuração
- **Segurança:** Equipe de Segurança
- **DevOps:** Equipe de Deployment

### Cronograma

- **Início:** 2025-08-01
- **Fim Previsto:** 2025-09-30
- **Milestones:**
  - 2025-08-15: Estrutura base e config manager
  - 2025-09-01: Validação automática funcionando
  - 2025-09-15: Integração com secrets manager
  - 2025-09-30: Deploy automatizado completo

---

## 🔄 Alternativas Consideradas

### Alternativa 1: Manter .env Simples

**Descrição:** Continuar com arquivos .env individuais

**Prós:**

- Simplicidade máxima
- Sem curva de aprendizagem
- Funciona bem para pequenos projetos

**Contras:**

- Não escala para 900+ serviços
- Segurança inadequada
- Propenso a erros humanos
- Dificuldade de auditoria

**Motivo da Rejeição:** Insustentável para escala do projeto SILA

### Alternativa 2: Configuração por Serviço

**Descrição:** Cada serviço gerencia suas próprias configurações

**Prós:**

- Isolamento completo
- Flexibilidade máxima

**Contras:**

- Caos de configurações
- Impossível auditar
- Duplicação massiva
- Risco de inconsistências

**Motivo da Rejeição:** Criaria problemas operacionais insustentáveis

### Alternativa 3: External Configuration Service

**Descrição:** Serviço externo para gestão de configurações

**Prós:**

- Centralização completa
- Recursos avançados

**Contras:**

- Dependência externa crítica
- Custo adicional
- Complexidade de integração
- Vendor lock-in

**Motivo da Rejeição:** Adiciona complexidade e dependência desnecessárias

---

## 🔗 Referências

- **ADRs Relacionados:** ADR-0001, ADR-0005
- **Documentação:** `/config/config_manager.py`
- **Scripts:** `/scripts/validate_env.py`
- **Issues:** GitHub Issues #280, #295, #310

---

## 📊 Impacto no SILA System

### Módulos Afetados

- **Todos os módulos**: Precisam usar config manager centralizado
- **Deploy**: Processo de deploy completamente modificado
- **Nível de impacto**: Alto

### Serviços Impactados

- **Todos os 900+ serviços**: Beneficiam de configuração consistente
- **Tipo de impacto**: Operação, Segurança, Deploy

### Equipes Impactadas

- **Desenvolvimento**: Novo padrão para acessar configurações
- **DevOps**: Processos de deploy automatizados
- **Segurança**: Gestão centralizada de secrets

---

## 📈 Métricas de Sucesso

### Técnicas

- Zero erros de configuração em produção
- Tempo de setup de novo ambiente < 10 minutos
- 100% das variáveis validadas automaticamente
- Deploy por ambiente 100% automatizado

### Negócio

- Redução de 80% em incidentes de configuração
- Tempo de onboarding reduzido em 70%
- Custo de gestão de ambientes reduzido em 60%

### Qualidade

- 100% das configurações documentadas
- Auditoria de configurações sem falhas
- Compliance de segurança 100% atendido

---

## 🔄 Histórico de Revisões

| Versão | Data       | Autor          | Mudanças                   |
| ------ | ---------- | -------------- | -------------------------- |
| 1.0    | 2025-10-26 | Marcelo Truman | Criação inicial            |
| 1.1    | 2025-10-26 | Marcelo Truman | Adição de integração Vault |

---

## 📝 Notas Adicionais

**Lições Aprendidas:**

- Config manager centralizado eliminou 90% dos problemas de configuração
- Validação automática preveniu vários incidentes de produção
- Integração com Vault foi mais simples que o previsto
- Documentação de variáveis foi essencial para equipe

**Problemas Inesperados:**

- Alguns serviços legados resistiram à mudança
- Cache de configurações criou problemas de atualização
- Balanceamento entre flexibilidade e padronização foi desafiador

**Recomendações:**

- Investir em ferramentas de validação
- Manter documentação sempre atualizada
- Automatizar ao máximo o processo
- Criar exceções documentadas para casos especiais

---

## 🏷️ Tags

`environment` `configuration` `secrets-management` `deployment` `automation` `accepted`

---

**Última Atualização:** 2025-10-26 **Próxima Revisão:** 2026-01-26 **Status:** ✅ Aceito
e Implementado

---

_Este ADR estabelece a estratégia fundamental de gestão de ambientes no SILA System.
Todas as decisões de configuração devem seguir este padrão centralizado._
