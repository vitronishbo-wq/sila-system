# ADR-0002: Migração de ORM - SQLAlchemy para Prisma Client Python

**Status:** Aceito **Data:** 2025-10-26 **Decisores:** Marcelo Truman, Equipe de Backend
**Revisores:** Admin SILA, Equipe de Banco de Dados

---

## 📋 Contexto

O projeto SILA utilizava SQLAlchemy como ORM principal, mas enfrentava vários desafios
críticos:

- **Complexidade de Migrações**: Migrations do SQLAlchemy eram verbosas e propensas a
  erros
- **Type Safety**: Falta de tipagem forte causava bugs em runtime
- **Performance**: Queries N+1 e otimizações manuais necessárias
- **Desenvolvimento**: Boilerplate excessivo para modelos simples
- **Consistência**: Diferentes convenções entre módulos

Com a necessidade de suportar 900+ serviços, a eficiência do ORM tornou-se crítica para
a performance e manutenibilidade do sistema.

---

## 🎯 Decisão

**Nós decidimos migrar de SQLAlchemy para Prisma Client Python** com as seguintes
especificações:

1. **Schema Único**: Arquivo `prisma/schema.prisma` como fonte da verdade
2. **Cliente Gerado**: Cliente Python gerado automaticamente a partir do schema
3. **Type Safety**: Tipagem forte integrada com Pydantic
4. **Async por Padrão**: Todas as operações de banco assíncronas
5. **Migrations Automáticas**: Gerenciadas pelo Prisma Migrate

**Implementação:**

- Manter PostgreSQL como banco de dados
- Migrar modelos existentes gradualmente
- Usar scripts automatizados para conversão
- Manter compatibilidade durante transição

---

## ✅ Consequências

### Positivas

- **Type Safety**: Erros detectados em tempo de desenvolvimento
- **Performance**: Queries otimizadas automaticamente
- **Productividade**: 70% menos código boilerplate
- **Consistência**: Schema único garante consistência
- **Migrations**: Gerenciamento simplificado e seguro
- **IDE Support**: Autocompleto e refatoração seguros

### Negativas

- **Curva de Aprendizagem**: Equipe precisa aprender DSL do Prisma
- **Dependência**: Nova dependência no ecossistema Prisma
- **Migração**: Esforço significativo para converter modelos existentes
- **Limitações**: Algumas features avançadas do SQLAlchemy não disponíveis

### Neutras

- **Ecossistema**: Menos maduro que SQLAlchemy, mas crescendo rapidamente
- **Debugging**: Abordagem diferente para debug de queries

---

## 🔄 Implementação

### Passos

1. **Setup Prisma**: Configurar Prisma no projeto
2. **Schema Creation**: Criar schema.prisma inicial
3. **Migration Scripts**: Desenvolver scripts de conversão automática
4. **Model Migration**: Migrar modelos módulo por módulo
5. **Service Layer Update**: Atualizar camadas de serviço
6. **Testing**: Validar funcionalidade e performance
7. **Cleanup**: Remover código SQLAlchemy legado

### Responsáveis

- **Coordenação:** Marcelo Truman (Arquiteto de Dados)
- **Desenvolvimento:** Equipe de Backend Python
- **Banco de Dados:** Equipe de DBA
- **Testes:** Equipe de QA

### Cronograma

- **Início:** 2025-08-01
- **Fim Previsto:** 2025-09-30
- **Milestones:**
  - 2025-08-10: Prisma configurado e schema inicial
  - 2025-08-20: Scripts de migração funcionais
  - 2025-09-10: Primeiros módulos migrados
  - 2025-09-30: Migração completa e testada

---

## 🔄 Alternativas Consideradas

### Alternativa 1: Manter SQLAlchemy com Melhorias

**Descrição:** Otimizar uso atual de SQLAlchemy com melhores práticas

**Prós:**

- Sem curva de aprendizagem
- Código existente mantido
- Ecossistema maduro

**Contras:**

- Complexidade persistente
- Boilerplate excessivo
- Type safety limitado

**Motivo da Rejeição:** Não resolveria problemas fundamentais de produtividade e type
safety

### Alternativa 2: Django ORM (com Django Ninja)

**Descrição:** Migrar para Django ORM com API framework moderno

**Prós:**

- ORM maduro e completo
- Admin interface automática
- Ecossistema rico

**Contras:**

- Acoplamento ao Django
- Performance inferior em larga escala
- Menos flexível que FastAPI

**Motivo da Rejeição:** Contrariaria decisão de API unificada com FastAPI

### Alternativa 3: SQL Puro com TypeSQL

**Descrição:** Usar SQL direto com type builders

**Prós:**

- Performance máxima
- Controle total

**Contras:**

- Muito boilerplate
- Sem abstração
- Difícil manutenção

**Motivo da Rejeição:** Aumentaria drasticamente a complexidade e tempo de
desenvolvimento

---

## 🔗 Referências

- **ADRs Relacionados:** ADR-0001, ADR-0004
- **Documentação:** `/backend/prisma/README.md`
- **Scripts:** `/scripts/migrate-sqla-to-prisma.ps1`
- **Issues:** GitHub Issues #201, #205, #210

---

## 📊 Impacto no SILA System

### Módulos Afetados

- **Todos os módulos com modelos**: citizenship, health, users, etc.
- **Nível de impacto**: Alto

### Serviços Impactados

- **Todos os serviços com persistência**: ~800 serviços
- **Tipo de impacto**: Performance, Desenvolvimento, Manutenibilidade

### Equipes Impactadas

- **Backend**: Requer treinamento em Prisma DSL
- **DBA**: Novas ferramentas de migração e gestão
- **QA**: Novas estratégias de teste de banco

---

## 📈 Métricas de Sucesso

### Técnicas

- Redução de 70% no código de modelos
- Performance 40% melhor em queries complexas
- Zero erros de tipo em runtime
- Tempo de migração de novos modelos reduzido em 80%

### Negócio

- Desenvolvimento de novos serviços 50% mais rápido
- Redução de 60% em bugs relacionados a banco
- Manutenção de modelos 70% mais barata

### Qualidade

- Type coverage 100%
- Schema validation automático
- Migrations zero-downtime

---

## 🔄 Histórico de Revisões

| Versão | Data       | Autor          | Mudanças                      |
| ------ | ---------- | -------------- | ----------------------------- |
| 1.0    | 2025-10-26 | Marcelo Truman | Criação inicial               |
| 1.1    | 2025-10-26 | Marcelo Truman | Adição de scripts de migração |

---

## 📝 Notas Adicionais

**Lições Aprendidas:**

- A DSL do Prisma é mais simples que o esperado após curva inicial
- Migração automática funcionou bem para 80% dos modelos
- Performance gains foram maiores que o previsto
- Integração com Pydantic é extremamente poderosa

**Problemas Inesperados:**

- Models com herança complexa exigiram tratamento manual
- Migrations de dados existentes requereram scripts customizados
- Debugging de queries Prisma exigiu novas ferramentas

**Recomendações:**

- Investir em treinamento prático da equipe
- Criar library de helpers para casos complexos
- Automatizar validação de schema
- Manter documentação de padrões de migração

---

## 🏷️ Tags

`orm` `prisma` `sqlalchemy` `database` `type-safety` `performance` `accepted`

---

**Última Atualização:** 2025-10-26 **Próxima Revisão:** 2026-01-26 **Status:** ✅ Aceito
e Implementado

---

_Este ADR estabelece a estratégia de dados para todo o projeto SILA System. Todas as
decisões relacionadas a persistência devem considerar este ADR._
