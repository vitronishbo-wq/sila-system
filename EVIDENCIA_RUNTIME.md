# Evidência Runtime (tentativas) — 2026-06-10

Resumo: tentei importar a aplicação e executar suites de teste rápidas; ambos falharam. Seguem trechos das saídas com os erros-chave.

## 1) Import check — falha
Comando executado:

```bash
python - <<'PY'
from apps.backend.app.main import app
print('IMPORT_OK')
PY
```

Resultado (trecho):

```
IMPORT_ERROR
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/home/dev03wsl/sila-system/apps/backend/app/main.py", line 9, in <module>
    from apps.backend.app.modules.educacao.foundation.observability.logging import (
  File "/home/dev03wsl/sila-system/apps/backend/app/modules/educacao/foundation/observability/logging.py", line 3, in <module>
    from pythonjsonlogger import jsonlogger
ModuleNotFoundError: No module named 'pythonjsonlogger'
```

Interpretação: a dependência `python-json-logger` não está instalada no ambiente. Instalar resolve o erro de import.

## 2) Testes (pytest) — falha de schema
Comando executado:

```bash
pytest -q -k "not e2e" --maxfail=1
```

Resultado (trecho):

```
E   asyncpg.exceptions.UndefinedTableError: relation "educacao_institution_capacities" does not exist

... (stack) ...

ProgrammingError: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <class 'asyncpg.exceptions.UndefinedTableError'>: relation "educacao_institution_capacities" does not exist
[SQL: INSERT INTO educacao_institution_capacities (...)]
```

Interpretação: os testes esperam que o schema do banco (tabelas) exista — a base de dados usada pelos testes não tem as tabelas criadas. É necessário apontar os testes para um DB migrado ou executar as migrations (passo operacional).

## Conclusão e próximos passos mínimos (operacionais)
- Instalar pacote faltante:

```bash
pip install python-json-logger
```

- Garantir DB com schema (opção A): apontar `DATABASE_URL` para uma base Postgres que já contenha o schema/migrations+seeds necessários.
- Ou (opção B, se autorizado): executar Alembic migrations existentes para criar schema no DB de dev. (Você pediu: não gerar migrations; aplicar migrations já existentes é compatível com isso.)

Após esses passos, posso:
- reiniciar a verificação: importar app, iniciar servidor, gerar OpenAPI e executar os cenários de territorialidade e RBAC (Governor Huambo vs Benguela), e verificar eventos FUC.

