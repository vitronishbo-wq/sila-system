# ADR-XXXX: [Título da Decisão]

**Status:** [Proposto/Aceito/Rejeitado/Supersedido/Deprecado] **Data:** [YYYY-MM-DD]
**Decisores:** [Nomes dos responsáveis] **Revisores:** [Nomes dos revisores]

---

## 📋 Contexto

[Descrever a situação que levou à necessidade desta decisão. Inclua:

- Problema ou oportunidade identificada
- Restrições técnicas ou de negócio
- Requisitos que precisavam ser atendidos
- Contexto do projeto SILA (900+ serviços, etc.)
- Impacto em módulos ou equipes afetadas

Exemplo: "O projeto SILA precisa suportar 900+ serviços digitais, mas a arquitetura
atual com Django legado está causando problemas de escalabilidade e manutenção..."]

---

## 🎯 Decisão

[Descrever claramente o que foi decidido. Seja específico e direto.

- Use linguagem afirmativa: "Nós decidimos..."
- Seja específico sobre tecnologias, padrões ou abordagens
- Inclua detalhes de implementação quando relevante
- Defina escopo da decisão

Exemplo: "Nós decidimos migrar o ORM do projeto de SQLAlchemy para Prisma Client Python,
mantendo o PostgreSQL como banco de dados principal..."]

---

## ✅ Consequências

### Positivas

- [Liste os benefícios esperados da decisão]
- [Inclua ganhos técnicos, de negócio ou operacionais]
- [Seja específico e mensurável quando possível]

### Negativas

- [Liste as desvantagens ou custos da decisão]
- [Inclua riscos técnicos, esforço necessário, etc.]
- [Seja honesto sobre as desvantagens]

### Neutras

- [Aspectos que não são claramente positivos ou negativos]
- [Trade-offs que precisarão ser gerenciados]

---

## 🔄 Implementação

### Passos

1. [Passo 1 da implementação]
2. [Passo 2 da implementação]
3. [Passo 3 da implementação]

### Responsáveis

- **Coordenação:** [Nome e função]
- **Desenvolvimento:** [Equipes responsáveis]
- **Testes:** [Equipe de QA]
- **Deploy:** [Equipe de DevOps]

### Cronograma

- **Início:** [Data]
- **Fim Previsto:** [Data]
- **Milestones:** [Datas importantes]

---

## 🔄 Alternativas Consideradas

### Alternativa 1: [Nome da Alternativa]

**Descrição:** [Breve descrição da alternativa]

**Prós:**

- [Benefício 1]
- [Benefício 2]

**Contras:**

- [Desvantagem 1]
- [Desvantagem 2]

**Motivo da Rejeição:** [Por que não foi escolhida]

### Alternativa 2: [Nome da Alternativa]

**Descrição:** [Breve descrição da alternativa]

**Prós:**

- [Benefício 1]
- [Benefício 2]

**Contras:**

- [Desvantagem 1]
- [Desvantagem 2]

**Motivo da Rejeição:** [Por que não foi escolhida]

---

## 🔗 Referências

- **ADRs Relacionados:** [Links para outros ADRs relevantes]
- **Documentação:** [Links para docs, specs, etc.]
- **Issues:** [Links para issues ou discussões]
- **Provas de Conceito:** [Links para PoCs ou protótipos]

---

## 📊 Impacto no SILA System

### Módulos Afetados

- [Lista de módulos que serão impactados]
- [Nível de impacto: Alto/Médio/Baixo]

### Serviços Impactados

- [Número estimado de serviços afetados]
- [Tipo de impacto: Funcional/Performance/Segurança]

### Equipes Impactadas

- [Equipes que precisarão se adaptar]
- [Necessidade de treinamento ou capacitação]

---

## 📈 Métricas de Sucesso

### Técnicas

- [Métrica 1: ex: "Redução de 50% em erros de ORM"]
- [Métrica 2: ex: "Performance 30% melhor em queries"]
- [Métrica 3: ex: "Tempo de desenvolvimento reduzido em 20%"]

### Negócio

- [Métrica 1: ex: "Time-to-market reduzido"]
- [Métrica 2: ex: "Custo de manutenção reduzido"]

### Qualidade

- [Métrica 1: ex: "Cobertura de testes aumentada"]
- [Métrica 2: ex: "Número de bugs reduzido"]

---

## 🔄 Histórico de Revisões

| Versão | Data         | Autor   | Mudanças                 |
| ------ | ------------ | ------- | ------------------------ |
| 1.0    | [YYYY-MM-DD] | [Autor] | Criação inicial          |
| 1.1    | [YYYY-MM-DD] | [Autor] | [Descrição das mudanças] |

---

## 📝 Notas Adicionais

[Qualquer informação adicional relevante:

- Lições aprendidas durante a implementação
- Problemas inesperados encontrados
- Recomendações para projetos futuros
- Dependências externas
- Riscos remanescentes

Exemplo: "Durante a implementação, descobrimos que o Prisma tem limitações com
migrations complexas. Recomendamos testes extensivos antes de aplicar em produção..."]

---

## 🏷️ Tags

`[categoria]` `[tecnologia]` `[impacto]` `[status]`

Exemplos:

- `architecture` `orm` `performance` `accepted`
- `security` `authentication` `high-impact` `implemented`
- `frontend` `unification` `strategic` `in-progress`

---

**Última Atualização:** [YYYY-MM-DD] **Próxima Revisão:** [YYYY-MM-DD] **Status:**
[Status atual]

---

_Este ADR faz parte do processo de governança arquitetônica do SILA System e deve ser
consultado antes de fazer modificações relacionadas a esta decisão._
