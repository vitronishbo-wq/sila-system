# GAP_ANALYSIS — Sprint 001 processes

Gerado: 2026-06-08

Notas iniciais:
- Respostas ao formato "Falta X?" (Sim/Não). "Sim" = está em falta no diretório do processo listado em `apps/backend/app/processes/<process>/`.
- Quando a funcionalidade existe noutro local (por exemplo: `app/modules/educacao` ou `app/modules/society/assistencia_social`), eu assinalo na nota.
- Sistema central de EventStore/EventBus existe em: [apps/backend/app/infrastructure/event_sourcing/postgres_event_store.py](apps/backend/app/infrastructure/event_sourcing/postgres_event_store.py#L1-L120) e [apps/backend/app/core/events/bridge/event_bus_bridge.py](apps/backend/app/core/events/bridge/event_bus_bridge.py#L1-L160).

---

## nascimento_bi_nif_ss
- Falta workflow? Sim
- Falta handler? Sim
- Falta EventStore? Sim (nenhuma referência no diretório do processo)
- Falta correlation_id? Sim (nenhum código no diretório; correlation_id existe a nível de módulos em alguns pontos, ex: `educacao/foundation/observability`)
- Falta timeline? Sim (sem `workflow_definition.json` nem estados definidos no diretório)
- Falta E2E SUCCESS? Sim
- Falta E2E REJECTION? Sim
- Falta E2E CANCELLATION? Sim

Observação: `nascimento_bi_nif_ss` está listado em [docs/modules/tree.modules.json](docs/modules/tree.modules.json#L1-L20) mas o diretório (`apps/backend/app/processes/nascimento_bi_nif_ss/`) contém apenas `__pycache__` — não há implementação.

---

## constituicao_empresa
- Falta workflow? Sim
- Falta handler? Sim
- Falta EventStore? Sim
- Falta correlation_id? Sim
- Falta timeline? Sim
- Falta E2E SUCCESS? Sim
- Falta E2E REJECTION? Sim
- Falta E2E CANCELLATION? Sim

Observação: pasta existe mas vazia (apenas `__pycache__`). Nenhuma implementação encontrada nas pastas `apps/backend/app/processes/constituicao_empresa/`.

---

## matricula_pagamento_certificado
- Falta workflow? Sim (no diretório do processo), NÃO ao nível do produto: implementação e E2E existem em `app/modules/educacao`.
- Falta handler? Sim (no diretório do processo)
- Falta EventStore? Sim (no diretório do processo). Sistema possui EventStore infra central ([PostgreSQLEventStore](apps/backend/app/infrastructure/event_sourcing/postgres_event_store.py#L1-L120)).
- Falta correlation_id? Sim (no diretório do processo); observado que `modules/educacao` tem `observability` que define/assegura `correlation_id` (`apps/backend/app/modules/educacao/foundation/observability/`).
- Falta timeline? Sim no diretório `apps/.../processes`; o fluxo é implementado em `app/modules/educacao` (codigo + E2E).
- Falta E2E SUCCESS? Não (E2E presente em `apps/backend/app/modules/educacao/tests/e2e/test_01_matricula_e2e.py`)
- Falta E2E REJECTION? Não (existe `test_matricula_rejeita_sem_pagamento` no ficheiro de E2E)
- Falta E2E CANCELLATION? Não (existe `test_05_cancelamento_e2e.py`)

Observação: implementação funcional e E2E para matrícula/pagamento/certificado existe em `apps/backend/app/modules/educacao/` — criar duplicações em `apps/backend/app/processes/matricula_pagamento_certificado/` seria arriscado.

Links úteis:
- [E2E: matricula (success/rejection)](apps/backend/app/modules/educacao/tests/e2e/test_01_matricula_e2e.py#L1-L40)
- [E2E: certificado](apps/backend/app/modules/educacao/tests/e2e/test_03_certificado_e2e.py#L1-L40)

---

## licenciamento_comercial
- Falta workflow? Sim (no diretório do processo: `workflow.py` ausente)
- Falta handler? Sim
- Falta EventStore? Sim (nenhuma referência no diretório do processo)
- Falta correlation_id? Sim (no diretório do processo)
- Falta timeline? Não — existe `workflow_definition.json` com `states` e `transitions` ([link](apps/backend/app/processes/licenciamento_comercial/workflow_definition.json#L1-L200))
- Falta E2E SUCCESS? Sim (nenhum E2E identificado para este processo)
- Falta E2E REJECTION? Sim
- Falta E2E CANCELLATION? Sim

Observação: apenas `workflow_definition.json` existe em `apps/backend/app/processes/licenciamento_comercial/`. Não há handlers nem testes ligados a esse ficheiro.

---

## beneficio_social
- Falta workflow? Sim (no diretório do processo)
- Falta handler? Sim
- Falta EventStore? Sim (no diretório do processo)
- Falta correlation_id? Sim (no diretório do processo)
- Falta timeline? Não — existe `workflow_definition.json` ([link](apps/backend/app/processes/beneficio_social/workflow_definition.json#L1-L200))
- Falta E2E SUCCESS? Sim (não localizei E2E no diretório do processo)
- Falta E2E REJECTION? Sim
- Falta E2E CANCELLATION? Sim

Observação: existe implementação/testes de benefício em `apps/backend/app/modules/society/assistencia_social/` (ver [test_fluxo_completo_assistencia.py](apps/backend/app/modules/society/assistencia_social/tests/test_fluxo_completo_assistencia.py#L1-L20)). O ficheiro `workflow_definition.json` em `apps/backend/app/processes/beneficio_social/` descreve estados/transições, mas não existe código ligado no mesmo diretório.

---

## Recomendações imediatas (não implementar sem validação)
1. Parar implementações novas em `apps/backend/app/processes/*` até validar onde a lógica já existe em `app/modules/*` (evitar duplicação).
2. Normalizar a origem das definições: decidir se a sprint deve consolidar implementações em `app/modules/*` (recomendado) ou migrar tudo para `apps/backend/app/processes/*` — documentar e planear migração se necessário.
3. Atualizar `docs/modules/tree.modules.json` para incluir entradas para os processos reais e apontar para a fonte canónica (module vs process-dir).
4. Quando autorizado: implementar `workflow.py` + `handlers.py` somente depois de confirmar que não existe implementação equivalente em `app/modules/*`.

---

Se quiser, eu: 
- posso abrir cada diretório do `apps/backend/app/processes/<process>/` e gerar um diff/roteiro de implementação sugerido, ou
- posso gerar uma lista de links apontando exactamente para os ficheiros de implementação que já existem em `app/modules/*` para cada processo (para decidir canonicidade).

Diz-me qual das opções preferes.