# ADR-0003: Unificação Frontend/Backend - API Única para Múltiplas Interfaces

**Status:** Aceito **Data:** 2025-10-26 **Decisores:** Marcelo Truman, Equipe de
Frontend, Equipe de Backend **Revisores:** Admin SILA, Equipe de Arquitetura

---

## 📋 Contexto

O projeto SILA originalmente planejava APIs separadas para o Portal do Cidadão e
Interface Administrativa, criando vários problemas:

- **Duplicação de Código**: Lógica de negócio replicada entre APIs
- **Inconsistências**: Comportamentos diferentes entre interfaces
- **Manutenção Complexa**: Mudanças exigiam atualizações múltiplas
- **Overhead Operacional**: Deploy e monitoramento duplicados
- **Segurança Fragmentada**: Diferentes implementações de autenticação

Com 900+ serviços para gerenciar, essa abordagem se tornaria insustentável,
multiplicando a complexidade operacional.

---

## 🎯 Decisão

**Nós decidimos adotar uma arquitetura de API única servindo múltiplas interfaces
frontend:**

1. **Backend Unificado**: Single FastAPI application servindo `/api/v1/`
2. **Frontend Dual**: Duas interfaces React (webapp e admin) consumindo a mesma API
3. **Segurança por Role**: Controle de acesso via roles e scopes no backend
4. **UI/UX Diferenciado**: Distinção apenas na camada de apresentação
5. **Compartilhamento de Lógica**: Business logic centralizada no backend

**Princípio Fundamental**: "A distinção entre Portal do Cidadão e Interface
Administrativa é feita apenas no Frontend (UI/UX) e por meio de regras de permissão
(Roles/Scopes) no Backend."

---

## ✅ Consequências

### Positivas

- **Simplicidade**: Arquitetura drasticamente mais simples
- **Consistência**: Comportamento idêntico em todas as interfaces
- **Manutenibilidade**: Mudanças feitas em um único lugar
- **Performance**: Cache e otimizações compartilhadas
- **Segurança**: Controle centralizado de permissões
- **Desenvolvimento**: Velocidade 3x maior no desenvolvimento

### Negativas

- **Complexidade de Frontend**: Frontends precisam gerenciar mais estado
- **Segurança**: Requer implementação cuidadosa de RBAC
- **Flexibilidade**: Menor capacidade de otimizações específicas por interface

### Neutras

- **API Design**: API deve ser genérica o suficiente para múltiplos casos de uso
- **Versionamento**: Controle de versão mais crítico com múltiplos clientes

---

## 🔄 Implementação

### Passos

1. **API Design**: Criar endpoints genéricos servindo ambos os casos
2. **Role System**: Implementar controle de acesso granular
3. **Frontend Webapp**: Desenvolver interface para cidadãos
4. **Frontend Admin**: Desenvolver interface administrativa
5. **Shared Components**: Criar biblioteca de componentes compartilhados
6. **Integration Testing**: Testar integração entre todos os componentes
7. **Documentation**: Documentar API para múltiplos consumidores

### Responsáveis

- **Coordenação:** Marcelo Truman (Arquiteto de Sistema)
- **Backend:** Equipe FastAPI
- **Frontend:** Equipe React
- **Segurança:** Equipe de Segurança

### Cronograma

- **Início:** 2025-08-15
- **Fim Previsto:** 2025-11-15
- **Milestones:**
  - 2025-09-01: API base com role system funcional
  - 2025-09-30: Frontend webapp MVP
  - 2025-10-15: Frontend admin MVP
  - 2025-11-15: Sistema completo e integrado

---

## 🔄 Alternativas Consideradas

### Alternativa 1: APIs Separadas por Interface

**Descrição:** Manter APIs distintas para citizen e admin

**Prós:**

- Otimização específica por interface
- Isolamento completo
- Simplicidade em cada API individual

**Contras:**

- Duplicação massiva de código
- Inconsistências garantidas
- Manutenção 3x mais complexa
- Overhead operacional alto

**Motivo da Rejeição:** Insustentável para 900+ serviços

### Alternativa 2: Backend Múltiplo com Shared Core

**Descrição:** Múltiplas aplicações backend compartilhando bibliotecas

**Prós:**

- Algum compartilhamento de código
- Deploy independente possível

**Contras:**

- Complexidade de gestão de dependências
- Sincronização de versões difícil
- Ainda duplicação significativa

**Motivo da Rejeição:** Complexidade operacional ainda muito alta

### Alternativa 3: GraphQL com Schema Unificado

**Descrição:** Usar GraphQL com schema único servindo múltiplos clientes

**Prós:**

- Flexibilidade máxima para clientes
- Single endpoint

**Contras:**

- Curva de aprendizagem steep
- Complexidade de caching
- Debugging mais difícil
- Ecossistema menos maduro para Python

**Motivo da Rejeição:** Complexidade excessiva para benefícios marginais neste contexto

---

## 🔗 Referências

- **ADRs Relacionados:** ADR-0001, ADR-0005
- **Documentação:** `/docs/ARQUITETURA_ATUALIZADA.md`
- **API Specs:** `/docs/api/unified-api-spec.md`
- **Issues:** GitHub Issues #180, #195, #220

---

## 📊 Impacto no SILA System

### Módulos Afetados

- **Todos os módulos de API**: Necessidade de design para múltiplos consumidores
- **Frontend**: Requer arquitetura para compartilhamento de componentes
- **Nível de impacto**: Alto

### Serviços Impactados

- **Todos os 900+ serviços**: Beneficiam da abordagem unificada
- **Tipo de impacto**: Arquitetural, Operacional, Desenvolvimento

### Equipes Impactadas

- **Backend**: Mudança de mentalidade para API genérica
- **Frontend**: Maior responsabilidade na camada de apresentação
- **DevOps**: Simplificação drasticamente do deployment

---

## 📈 Métricas de Sucesso

### Técnicas

- Redução de 70% no código de API duplicado
- Tempo de desenvolvimento de novos serviços reduzido em 60%
- 100% de consistência entre interfaces
- Zero divergências de comportamento

### Negócio

- Time-to-market de novos serviços reduzido em 50%
- Custo de manutenção reduzido em 65%
- Capacidade de lançar 900+ serviços sem aumento proporcional de equipe

### Qualidade

- Bug consistency 100% entre interfaces
- Test coverage compartilhado >90%
- Documentation completeness 100%

---

## 🔄 Histórico de Revisões

| Versão | Data       | Autor          | Mudanças                            |
| ------ | ---------- | -------------- | ----------------------------------- |
| 1.0    | 2025-10-26 | Marcelo Truman | Criação inicial                     |
| 1.1    | 2025-10-26 | Marcelo Truman | Adição de exemplos de implementação |

---

## 📝 Notas Adicionais

**Lições Aprendidas:**

- A abordagem unificada foi muito mais simples de implementar que o previsto
- Role-based access control foi essencial para o sucesso
- Componentes compartilhados de frontend aceleraram desenvolvimento
- Documentação de API se tornou crítica para múltiplos times

**Problemas Inesperados:**

- Balanceamento de detalhes na API (genérica vs específica) foi desafiador
- Frontend admin ficou mais complexo que o previsto
- Caching estratégico se tornou mais importante

**Recomendações:**

- Investir pesadamente em design de API
- Criar guias de desenvolvimento para múltiplos consumidores
- Automatizar testes de consistência entre interfaces
- Manter comunicação constante entre times de frontend

---

## 🏷️ Tags

`frontend` `backend` `unification` `api-design` `rbac` `architecture` `accepted`

---

**Última Atualização:** 2025-10-26 **Próxima Revisão:** 2026-01-26 **Status:** ✅ Aceito
e Implementado

---

_Este ADR define a estratégia fundamental de integração entre frontend e backend no SILA
System. Todas as decisões de API devem seguir este princípio de unificação._
