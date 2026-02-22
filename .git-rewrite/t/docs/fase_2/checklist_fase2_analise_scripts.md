# Checklist Fase 2 – Análise Estrutural de Scripts

Data de Geração: 2025-11-20 06:00:12

Este checklist cobre toda a análise de duplicações, mapeamento de funções repetidas,
identificação de padrões, classificação por Nível (1/2/3), e aplicação dos 6 Princípios
Obrigatórios.

## 1. Princípios Obrigatórios

- [ ] **P1 — Intocabilidade Nível 1**
- [ ] **P2 — Reversibilidade 100%**
- [ ] **P3 — Nenhuma alteração funcional na Fase 2A**
- [ ] **P4 — Libs só na Fase 2B**
- [ ] **P5 — Idempotência**
- [ ] **P6 — Transparência completa**

## 2. Classificação de Scripts

- [ ] Confirmar lista final:
  - 21 scripts → **Nível 1 (intocáveis)**
  - 36 scripts → **Nível 2**
  - 15 scripts → **Nível 3**

## 3. Mapeamento de Duplicações

- [ ] Identificar funções repetidas entre scripts
- [ ] Criar matriz de correspondência
- [ ] Detectar agrupamentos (clusters) de repetição
- [ ] Qualificar funções candidatas a libs

## 4. Análise Técnica (por script)

- [ ] Extrair funções
- [ ] Classificar por Nível
- [ ] Apontar duplicações
- [ ] Registrar dependências
- [ ] Registrar chamadas a binários externos

## 5. Saídas Obrigatórias

- [ ] Relatório técnico fase2_relatorio_analise.md
- [ ] Mapa de helpers fase2_helpers_map.md
- [ ] Atualizar fase2_libs_status.md

## 6. Gate de Conclusão Fase 2A

- [ ] TODAS as duplicações registradas
- [ ] TODAS as funções mapeadas
- [ ] Checklist 100% concluído
