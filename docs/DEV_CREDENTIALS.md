# DEV / HOMOLOGAÇÃO Credentials (ONLY for development/homologation)

This file documents a small set of development users for local testing. NEVER use these in production.

Formato: Usuário | Função | Senha | Status

central@sila.gov.ao        | ADMIN_CENTRAL    | Sila_1983 | ✅
prov.huambo@sila.gov.ao    | ADMIN_PROVINCIAL | Sila_1983 | ✅
prov.benguela@sila.gov.ao  | ADMIN_PROVINCIAL | Sila_1983 | ✅
mun.caala@sila.gov.ao      | ADMIN_MUNICIPAL  | Sila_1983 | ✅
mun.huambo@sila.gov.ao     | ADMIN_MUNICIPAL  | Sila_1983 | ✅
comun.huambo@sila.gov.ao   | ADMIN_COMMUNAL   | Sila_1983 | ✅
truman@gmail.com           | CITIZEN          | Sila_1983 | ✅
admin@sila.gov.ao          | ADMIN            | Sila_1983 | ✅

# Regras de uso
- Uso estritamente local: desenvolvimento e demonstração (DEV / HOMOLOGAÇÃO).
- Se for necessário criar mais usuários de teste, adicione-os neste ficheiro.
- Nunca transportar estas credenciais para ambientes de produção.
- Auditar e rotacionar antes de qualquer migração para PROD.

## Seed automático (scripts/seed_dev_data.py)

O repositório inclui um pequeno utilitário que automatiza a criação dos ficheiros
de desenvolvimento a partir deste ficheiro. O script lê as linhas em formato
`usuario | papel | senha | status` e gera os seguintes ficheiros em `data/dev`:

- `users.json` — lista de utilizadores com a senha universal.
- `institutions.json` — lista de instituições derivadas dos emails.
- `credentials.json` — metadados simples com a senha universal.

Senha universal (hardcoded para DEV/HOMOLOGAÇÃO): `Sila_1983`

Exemplos de uso:

```bash
python3 scripts/seed_dev_data.py --dry-run   # simula a criação
python3 scripts/seed_dev_data.py             # escreve ficheiros (não sobrescreve)
python3 scripts/seed_dev_data.py --force     # sobrescreve ficheiros existentes
```

Avisos:

- Estes ficheiros e a senha são apenas para desenvolvimento/homologação.
- Não usar em produção e lembre-se de auditar/rotacionar antes de migrar.
- Considere adicionar `data/dev/` ao `.gitignore` se não quiser commitar dados de teste.

