# ADR-0004: Padronização de Módulos - Estrutura Consistente para 900+ Serviços

**Status:** Aceito **Data:** 2025-10-26 **Decisores:** Marcelo Truman, Equipe de
Arquitetura, Líderes de Módulo **Revisores:** Admin SILA, Equipe de Desenvolvimento

---

## 📋 Contexto

O projeto SILA apresentava inconsistências críticas na estrutura de módulos:

- **Nomenclatura Variada**: `citize/`, `appoi/`, `health/`, `saude/` - nomes
  inconsistentes
- **Estrutura Diferente**: Alguns módulos tinham `models/`, outros `entities/`
- **Falta de Padrão**: Organização arbitrária dificultava manutenção
- **Duplicação**: Módulos similares com estruturas diferentes
- **Onboarding Difícil**: Novos desenvolvedores perdidos com múltiplos padrões

Com a meta de 900+ serviços, essa inconsistência se tornaria um bloqueio para
escalabilidade e manutenibilidade.

---

## 🎯 Decisão

**Nós decidimos padronizar todos os módulos seguindo uma estrutura consistente:**

1. **Nomenclatura Padrão**: Nomes em inglês, snake_case para diretórios
2. **Estrutura Fixa**: Todos os módulos seguem o mesmo template
3. **Camadas Obrigatórias**: `models/`, `schemas/`, `routes/`, `services/`
4. **Convenções de Código**: Padrões consistentes em todos os módulos
5. **Automação**: Scripts para gerar e validar estrutura de módulos

**Estrutura Padrão:**

```
backend/app/modules/<domain>/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── <domain>.py
├── schemas/
│   ├── __init__.py
│   └── <domain>.py
├── routes/
│   ├── __init__.py
│   └── <domain>_routes.py
└── services/
    ├── __init__.py
    └── <domain>_service.py
```

---

## ✅ Consequências

### Positivas

- **Consistência**: Todos os módulos seguem o mesmo padrão
- **Manutenibilidade**: Previsibilidade facilita manutenção
- **Onboarding**: Novos desenvolvedores aprendem um padrão único
- **Automação**: Scripts podem operar em todos os módulos
- **Qualidade**: Validação automática de estrutura
- **Escalabilidade**: Fácil adicionar novos módulos

### Negativas

- **Restrição**: Menos flexibilidade para casos especiais
- **Esforço Inicial**: Migração de módulos existentes
- **Resistência**: Equipes podem resistir a padronização

### Neutras

- **Simplicidade**: Estrutura pode ser simples demais para domínios complexos
- **Extensão**: Módulos podem adicionar camadas extras se necessário

---

## 🔄 Implementação

### Passos

1. **Template Creation**: Criar template de módulo padrão
2. **Migration Scripts**: Desenvolver scripts de migração automática
3. **Module Audit**: Identificar todos os módulos não-padronizados
4. **Structure Migration**: Migrar módulos para estrutura padrão
5. **Naming Standardization**: Padronizar nomes de diretórios e arquivos
6. **Validation**: Implementar validação automática de estrutura
7. **Documentation**: Documentar padrões e convenções

### Responsáveis

- **Coordenação:** Marcelo Truman (Arquiteto de Código)
- **Desenvolvimento:** Todos os líderes de módulo
- **Qualidade:** Equipe de QA
- **DevOps:** Equipe de automação

### Cronograma

- **Início:** 2025-08-01
- **Fim Previsto:** 2025-09-15
- **Milestones:**
  - 2025-08-10: Template e scripts prontos
  - 2025-08-25: Migração dos primeiros 10 módulos
  - 2025-09-10: Todos os módulos migrados
  - 2025-09-15: Validação completa e documentação

---

## 🔄 Alternativas Consideradas

### Alternativa 1: Manter Estrutura Flexível

**Descrição:** Permitir que cada módulo defina sua própria estrutura

**Prós:**

- Flexibilidade máxima
- Adaptação a necessidades específicas
- Menos resistência da equipe

**Contras:**

- Caos em larga escala
- Impossível automatizar
- Onboarding muito difícil
- Inconsistências garantidas

**Motivo da Rejeição:** Insustentável para 900+ serviços

### Alternativa 2: Estrutura por Categoria

**Descrição:** Diferentes estruturas para diferentes tipos de módulo

**Prós:**

- Alguma adaptação por categoria
- Menos rígido que padrão único

**Contras:**

- Complexidade de gestão
- Fronteiras entre categorias confusas
- Ainda inconsistente

**Motivo da Rejeição:** Adiciona complexidade sem resolver o problema fundamental

### Alternativa 3: Microserviços com Estrutura Própria

**Descrição:** Cada serviço como microserviço independente

**Prós:**

- Independência total
- Tecnologia adequada por serviço

**Contras:**

- Overhead operacional massivo
- Complexidade de comunicação
- Dificuldade de gestão

**Motivo da Rejeição:** Excesso de complexidade para o contexto atual

---

## 🔗 Referências

- **ADRs Relacionados:** ADR-0001, ADR-0002
- **Documentação:** `/docs/PLANO_SANEAMENTO.md`
- **Scripts:** `/scripts/generate_modules_structure.py`
- **Issues:** GitHub Issues #150, #165, #178

---

## 📊 Impacto no SILA System

### Módulos Afetados

- **Todos os 25+ módulos existentes**: Necessidade de migração
- **Futuros 900+ serviços**: Beneficiam diretamente da padronização
- **Nível de impacto**: Alto

### Serviços Impactados

- **Todos os serviços**: Estrutura consistente facilita desenvolvimento
- **Tipo de impacto**: Desenvolvimento, Manutenibilidade, Qualidade

### Equipes Impactadas

- **Desenvolvimento**: Novo padrão a seguir
- **QA**: Processos de teste padronizados
- **DevOps**: Automação simplificada

---

## 📈 Métricas de Sucesso

### Técnicas

- 100% dos módulos seguem estrutura padrão
- Tempo de criação de novo módulo reduzido em 80%
- Zero erros de estrutura em validação automática
- Onboarding de novos desenvolvedores 60% mais rápido

### Negócio

- Custo de manutenção reduzido em 40%
- Velocidade de desenvolvimento aumentada em 50%
- Qualidade consistente em todos os módulos

### Qualidade

- Code review padronizado
- Testes consistentes entre módulos
- Documentação uniforme

---

## 🔄 Histórico de Revisões

| Versão | Data       | Autor          | Mudanças                       |
| ------ | ---------- | -------------- | ------------------------------ |
| 1.0    | 2025-10-26 | Marcelo Truman | Criação inicial                |
| 1.1    | 2025-10-26 | Marcelo Truman | Adição de scripts de automação |

---

## 📝 Notas Adicionais

**Lições Aprendidas:**

- A resistência inicial da equipe foi superada com benefícios visíveis
- Scripts de automação foram essenciais para o sucesso
- Template único reduziu drasticamente erros de beginners
- Validação automática impediu regressões

**Problemas Inesperados:**

- Alguns domínios complexos precisaram de extensões ao padrão
- Migração de módulos legados foi mais complexa que o previsto
- Nomenclatura em inglês vs português gerou debates

**Recomendações:**

- Manter processo de evolução do padrão
- Criar exceções documentadas para casos especiais
- Investir em treinamento da equipe
- Automatizar ao máximo a criação e validação

---

## 🏷️ Tags

`modules` `standardization` `structure` `automation` `code-quality` `accepted`

---

**Última Atualização:** 2025-10-26 **Próxima Revisão:** 2026-01-26 **Status:** ✅ Aceito
e Implementado

---

_Este ADR estabelece os padrões fundamentais de organização de código no SILA System.
Todos os novos módulos devem seguir esta estrutura sem exceção._
