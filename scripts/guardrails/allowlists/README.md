# Guardrails Test Allowlists

Este diretório define a allowlist oficial de testes por versão e por fase.

## Versões

- `v1.sh`: baseline inicial da consolidação.

## Fases

- `core`: execução padrão (`make architecture-guardrails`).
- `integration`: foco em integração/e2e não legada.
- `legacy`: suites fora do baseline oficial para auditoria/migração.

## Seleção da fase/versão

Use variáveis de ambiente no `scripts/run_guardrails.sh`:

```bash
GUARDRAILS_ALLOWLIST_VERSION=v1 GUARDRAILS_PHASE=core bash scripts/run_guardrails.sh
```

Overrides:

- `GUARDRAILS_TEST_CMD`: ignora allowlist e executa comando custom.
- `GUARDRAILS_PYTEST_EXTRA_ARGS`: adiciona argumentos ao `pytest` gerado.
- `GUARDRAILS_PYTEST_BIN`: define binário do pytest (default: `pytest`).
