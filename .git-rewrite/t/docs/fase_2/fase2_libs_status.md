# Status das Libs Compartilhadas – Fase 2

Data de Geração: 2025-11-20 06:00:12

Aqui são rastreadas todas as libs que surgirem da consolidação de funções duplicadas
durante a Fase 2B. Nenhuma deve tocar diretamente os scripts originais até a Fase 3.

## Regras

- Libs devem ser **puras**, sem side-effects
- Libs devem ser **shell-agnósticas** (ou claramente bash/zsh)
- Nenhum script deve ser modificado ainda

## Tabela de Status

| Lib                 | Status    | Origem                            | Observações        |
| ------------------- | --------- | --------------------------------- | ------------------ |
| deploy_helpers.sh   | Planejado | duplicações em deploy/automação   | aguardando Fase 2A |
| database_helpers.sh | Planejado | duplicações em init_db/migrate    | aguardando Fase 2A |
| nginx_helpers.sh    | Planejado | duplicações nos scripts nginx\_\* | aguardando Fase 2A |
| system_helpers.sh   | Planejado | duplicações genéricas             | aguardando análise |

## Estrutura Recomendada

- scripts/lib/deploy_helpers.sh
- scripts/lib/database_helpers.sh
- scripts/lib/nginx_helpers.sh
- scripts/lib/system_helpers.sh

## Gatilho de Evolução

Somente após o checklist completo da Fase 2A. Antes disso, nenhuma lib pode ser criada
de fato.
