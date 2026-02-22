# auto_create_admin.sh

Este documento descreve o script `scripts/auto_create_admin.sh` criado para automatizar
a criação de usuários administrativos no banco local do projeto.

## Objetivo

Automatizar o fluxo de:

- backup do `.env`,
- garantir que `DATABASE_URL` e `ASYNC_DATABASE_URL` apontem para `localhost`,
- checar disponibilidade do PostgreSQL,
- executar `scripts/create_admin_batch.py` para criar/garantir administradores,
- listar usuários existentes para validação.

## Uso

Executar o script:

```bash
chmod +x scripts/auto_create_admin.sh
./scripts/auto_create_admin.sh
```

Para reverter `.env` e tentar reverter alterações de arquivos (via git):

```bash
./scripts/auto_create_admin.sh --revert
```

## Pré-requisitos

- PostgreSQL rodando localmente (`localhost:5432`).
- Dependências Python instaladas no virtualenv `backend/venv` (consulte
  `backend/requirements.txt`).
- Ter `git` instalado se for usar a opção `--revert`.

## Flags

- `--revert` — restaura `.env` a partir de `.env.bak` e tenta reverter os arquivos
  alterados via `git checkout`.

## Comportamento

- O script cria um backup em `.env.auto.bak` e também garante que exista `.env.bak`.
- Atualiza `.env` para usar credenciais padrão `postgres:postgres` em `localhost`.
- Executa `create_admin_batch.py` e `list_users.py` usando `backend/venv`.
- Não altera o banco de produção; as mudanças são locais no `.env`.

## Segurança

- As credenciais colocadas no `.env` são para desenvolvimento local e devem ser
  substituídas em ambientes de produção.

## Observações finais

- Se você preferir rodar via Docker Compose, é preferível subir os serviços e executar
  os scripts dentro do container `backend` para que os nomes `db` e outros serviços
  resolvam automaticamente.

---

Se quiser, posso:

- Adicionar `--force` para recriar usuários (com confirmação interativa),
- Criar um `Makefile` target para esse fluxo,
- Ou abrir um branch com as alterações temporárias separadas (recomendado para PRs).
