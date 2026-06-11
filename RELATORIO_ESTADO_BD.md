# RELATÓRIO: Estado real do Banco de Dados (diagnóstico somente leitura)

Data: 2026-06-10

## Resumo executivo
- `DATABASE_URL` efetiva lida de `apps/backend/app/core/settings.py` (.env): `postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db`.
- `alembic current` conectado ao BD: `20260607_0003_create_provider_homologation_evidence (head)`.
- `alembic heads` (repositório): `20260607_0003_create_provider_homologation_evidence (head)`.
- Resultado: não há migrações pendentes segundo Alembic (current == heads).
- Verificação de existência da tabela `educacao_institution_capacities`: NÃO EXISTE no banco atual (resultado `NULL`).

## Comandos executados (e saídas)

1) Obter `DATABASE_URL` via settings

- Comando (executado via Python import):
```
from apps.backend.app.core.settings import settings
print(settings.DATABASE_URL)
```
- Saída:
```
DATABASE_URL=postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db
```
- Arquivo de configuração Alembic utilizado: `apps/backend/alembic.ini` (contém `sqlalchemy.url = postgresql+asyncpg://sila_user:...`).

2) Estado Alembic (DB)

- Comando:
```
alembic -c /home/dev03wsl/sila-system/apps/backend/alembic.ini current
```
- Saída:
```
20260607_0003_create_provider_homologation_evidence (head)
```

3) Heads do repositório Alembic

- Comando:
```
alembic -c /home/dev03wsl/sila-system/apps/backend/alembic.ini heads
```
- Saída:
```
20260607_0003_create_provider_homologation_evidence (head)
```

4) Verificação direta de existência da tabela

- Comando (psql):
```
psql postgresql://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db -c "select to_regclass('public.educacao_institution_capacities');"
```
- Saída:
```
 to_regclass 
-------------
 
(1 row)
```
(ou seja, `NULL` — a tabela não existe)

5) Evidência no código fonte (modelo presente, sem migração correspondente)

- Modelo definido em: `apps/backend/app/modules/educacao/infrastructure/models/institution_capacity_model.py`
  - `__tablename__ = "educacao_institution_capacities"`
- Busca em migrations Alembic: não foi encontrada nenhuma `op.create_table` que crie `educacao_institution_capacities` nas `apps/backend/alembic/versions/`.

## Diagnóstico
- O banco de dados apontado pela configuração está acessível e registra a revisão Alembic `20260607_0003_create_provider_homologation_evidence` como aplicada (current == head).
- Apesar disso, o modelo ORM `InstitutionCapacityModel` (tabela `educacao_institution_capacities`) existe no código-fonte, mas não há migração Alembic que a crie — por isso a tabela não existe no BD.
- Isso explica o erro observado nos testes (`UndefinedTableError: relation "educacao_institution_capacities" does not exist`) quando o código tenta inserir/usar essa tabela.

## Impacto e riscos
- Testes e fluxos que dependem de `educacao_institution_capacities` falharão até que a migração correspondente seja criada e aplicada.
- Código editado para adicionar colunas ORM (`territory_id`, `created_by`, `managed_by`) sem migração causa divergência entre modelo e esquema.
- Qualquer tentativa de executar a aplicação completa (importar `apps.backend.app.main`) também falha atualmente por dependências faltantes (ex.: `pythonjsonlogger`), bloqueando validação runtime até correções.

## Recomendações (próximos passos, operacionais — requerem permissão do responsável)
- Criar uma migração Alembic para adicionar a tabela `educacao_institution_capacities` conforme o modelo ou ajustar migrations existentes para incluí-la.
- Alternativa temporária para testes: criar a tabela manualmente no BD de desenvolvimento com DDL equivalente (apenas se for aceitável alterar o BD de desenvolvimento).
- Garantir que todas as alterações ORM (novos campos: `territory_id`, `created_by`, `managed_by`) tenham uma migração correspondente antes de validar runtime.
- Instalar dependência faltante `pythonjsonlogger` no ambiente de execução para permitir importação completa e diagnósticos adicionais.
- Após aplicar migrações, executar a suíte de testes para validar que os erros de `UndefinedTableError` foram resolvidos.

## Arquivos e locais consultados
- `apps/backend/app/core/settings.py`
- `apps/backend/alembic.ini`
- `apps/backend/alembic/versions/` (lista de migrações)
- `apps/backend/app/modules/educacao/infrastructure/models/institution_capacity_model.py`

---
Relatório gerado automaticamente via diagnóstico read-only pelo assistente (comandos `alembic` + `psql` + inspeção de código).
