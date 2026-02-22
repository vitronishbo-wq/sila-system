# ADR-0001: Visão Geral da Arquitetura SILA System

**Status:** Aceito **Data:** 2025-10-26 **Decisores:** Marcelo Truman, Equipe de
Arquitetura SILA **Revisores:** Admin SILA, Equipe Técnica

---

## 📋 Contexto

O projeto SILA (Plataforma Única Digital do Cidadão) precisa suportar **900+ serviços
digitais** para o governo de Angola. A arquitetura inicial baseada em Django legado
apresentava limitações críticas:

- **Escalabilidade**: Dificuldade em suportar centenas de serviços
- **Manutenibilidade**: Código monolítico e acoplado
- **Performance**: Problemas com ORM Django em larga escala
- **Desenvolvimento**: Velocidade limitada por tecnologias antigas
- **Integração**: Dificuldade em integrar novos serviços

Além disso, havia uma separação desnecessária entre frontend e backend que criava
complexidade operacional.

---

## 🎯 Decisão

**Nós decidimos adotar uma arquitetura unificada baseada em:**

1. **Backend Único**: FastAPI + Prisma + PostgreSQL servindo todos os clientes
2. **Frontend Dual**: React com duas interfaces (webapp e admin) compartilhando a mesma
   API
3. **Modularização**: Estrutura de domínios padronizada para todos os módulos
4. **API Centralizada**: Single API endpoint `/api/v1/` para todas as operações
5. **Segurança Gradual**: Abordagem faseada para implementação de segurança robusta

**Princípio Fundamental**: "A distinção entre Portal do Cidadão e Interface
Administrativa é feita apenas no Frontend (UI/UX) e por regras de permissão no Backend.
Não criar APIs separadas."

---

## ✅ Consequências

### Positivas

- **Escalabilidade**: Arquitetura preparada para 900+ serviços
- **Manutenibilidade**: Código modular e desacoplado
- **Performance**: FastAPI + Prisma oferece melhor performance
- **Desenvolvimento**: Velocidade aumentada com ferramentas modernas
- **Consistência**: API única garante comportamento consistente
- **Operação**: Simplificação do deployment e monitoramento

### Negativas

- **Curva de Aprendizagem**: Equipe precisa aprender FastAPI e Prisma
- **Migração**: Esforço significativo para migrar código legado
- **Risco**: Mudança arquitetural grande em projeto crítico

### Neutras

- **Complexidade**: Arquitetura mais moderna mas com mais conceitos
- **Dependências**: Novas dependências de ecossistema Python/Node.js

---

## 🔄 Implementação

### Passos

1. **Fase 1**: Criar estrutura base com FastAPI + Prisma
2. **Fase 2**: Migrar módulos críticos (citizenship, health)
3. **Fase 3**: Implementar frontend unificado
4. **Fase 4**: Migrar módulos restantes
5. **Fase 5**: Otimização e escalabilidade

### Responsáveis

- **Coordenação:** Marcelo Truman (Arquiteto Chefe)
- **Backend:** Equipe de Desenvolvimento Python
- **Frontend:** Equipe de Desenvolvimento React
- **DevOps:** Equipe de Infraestrutura

### Cronograma

- **Início:** 2025-08-01
- **Fim Previsto:** 2025-12-31
- **Milestones:**
  - 2025-08-15: Base arquitetural funcional
  - 2025-09-30: Primeiros módulos migrados
  - 2025-11-15: Frontend unificado completo
  - 2025-12-31: Sistema pronto para produção

---

## 🔄 Alternativas Consideradas

### Alternativa 1: Manter Django com Melhorias

**Descrição:** Evoluir arquitetura Django existente com otimizações

**Prós:**

- Menor risco de migração
- Equipe já familiarizada
- Código existente aproveitado

**Contras:**

- Limitações de escalabilidade persistem
- Performance inferior em larga escala
- Dificuldade com 900+ serviços

**Motivo da Rejeição:** Não atenderia requisitos de escalabilidade para 900+ serviços

### Alternativa 2: Microserviços Completos

**Descrição:** Arquitetura de microserviços com APIs separadas

**Prós:**

- Escalabilidade máxima
- Independência de serviços

**Contras:**

- Complexidade operacional muito alta
- Overhead para equipe atual
- Dificuldade de gestão com 900+ serviços

**Motivo da Rejeição:** Complexidade excessiva para capacidade e necessidades atuais

### Alternativa 3: Backend Monolítico + Frontends Separados

**Descrição:** Manter APIs separadas para citizen e admin

**Prós:**

- Separação clara de responsabilidades
- Segurança por isolamento

**Contras:**

- Duplicação de código e lógica
- Complexidade de manutenção
- Inconsistências entre APIs

**Motivo da Rejeição:** Criaria mais problemas de manutenção do que resolveria

---

## 🔗 Referências

- **ADRs Relacionados:** ADR-0002, ADR-0003, ADR-0004
- **Documentação:** `/docs/ARQUITETURA_ATUALIZADA.md`
- **Issues:** GitHub Issues #123, #145, #167
- **Provas de Conceito:** `/tests/poc/fastapi-prisma/`

---

## 📊 Impacto no SILA System

### Módulos Afetados

- **Todos os módulos**: Necessidade de adaptação para nova arquitetura
- **Nível de impacto**: Alto

### Serviços Impactados

- **900+ serviços**: Todos os serviços migrarão para nova arquitetura
- **Tipo de impacto**: Funcional, Performance, Manutenibilidade

### Equipes Impactadas

- **Backend**: Requer treinamento em FastAPI e Prisma
- **Frontend**: Mudança para React com API unificada
- **DevOps**: Novos processos de deployment e monitoramento

---

## 📈 Métricas de Sucesso

### Técnicas

- Performance 50% melhor em endpoints críticos
- Redução de 70% em erros de ORM
- Tempo de desenvolvimento de novos serviços reduzido em 40%
- 99.9% uptime em produção

### Negócio

- Time-to-market de novos serviços reduzido em 60%
- Custo de manutenção reduzido em 30%
- Capacidade de suportar 900+ serviços sem degradação

### Qualidade

- Cobertura de testes >80%
- Zero erros de importação em produção
- Documentação 100% atualizada

---

## 🔄 Histórico de Revisões

| Versão | Data       | Autor          | Mudanças                      |
| ------ | ---------- | -------------- | ----------------------------- |
| 1.0    | 2025-10-26 | Marcelo Truman | Criação inicial               |
| 1.1    | 2025-10-26 | Marcelo Truman | Adição de métricas detalhadas |

---

## 📝 Notas Adicionais

**Lições Aprendidas:**

- A migração do Django para FastAPI revelou ganhos significativos de performance
- A abordagem de API única simplificou enormemente o desenvolvimento
- A modularização foi essencial para gerenciar a complexidade dos 900+ serviços

**Problemas Inesperados:**

- Integração com sistemas legados exigiu adaptadores adicionais
- Curva de aprendizagem do Prisma foi maior que o esperado
- Migração de dados requereu cuidados especiais com consistência

**Recomendações:**

- Investir em capacitação contínua da equipe
- Automatizar ao máximo o processo de migração de módulos
- Manter documentação detalhada de cada passo

---

## 🏷️ Tags

`architecture` `fastapi` `prisma` `unified-api` `scalability` `accepted`

---

**Última Atualização:** 2025-10-26 **Próxima Revisão:** 2026-01-26 **Status:** ✅ Aceito
e Implementado

---

_Este ADR estabelece a fundação arquitetônica para todo o projeto SILA System e deve ser
consultado antes de qualquer decisão estrutural significativa._
