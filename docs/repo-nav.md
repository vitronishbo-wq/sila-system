# repo-nav

Ferramenta CLI leve para navegar rapidamente no repositório usando os índices já gerados em `docs/tree.json` e `docs/modules/*.json`.

Principais comandos:
- `search <padrao>` — procura por ficheiros pelo nome (modo normal/fuzzy/regex) ou `--content` para procurar no conteúdo (usa `rg`/`grep`).
- `open <padrao>` — abre o ficheiro mais relevante no editor definido por `$REPO_NAV_EDITOR` ou `$EDITOR`.
- `show <path>` — apresenta um trecho (contexto) de um ficheiro existente.
- `modules [--module NAME]` — lista módulos ou mostra info do módulo selecionado.

Nota: o `repo-nav` carrega `module.json` do root de cada módulo (quando presente) e mostra metadados como `owners`, `maturity` e `last_updated` ao listar módulos ou ao pedir `--module`.

Notas de segurança e compatibilidade:
- O CLI respeita o *bootstrap obrigatório* do repositório (use `AGENT_RULES.md` como processo de arranque manual quando interagir com agentes).
- A ferramenta NÃO faz varridas recursivas indiscriminadas: usa apenas as raízes definidas em `docs/tree.json`.

Exemplos rápidos:

```bash
python3 scripts/repo-nav search nascimento --fuzzy
python3 scripts/repo-nav open test_nascimento_success --exec
python3 scripts/repo-nav show apps/backend/app/processes/nascimento_bi_nif_ss/tests/e2e/test_nascimento_success_e2e.py --line 1
python3 scripts/repo-nav modules --module nascimento_bi_nif_ss
```

Instalação / uso interativo:
- Torne o ficheiro executável: `chmod +x scripts/repo-nav`
- Defina o editor preferido: `export REPO_NAV_EDITOR=code` ou `export EDITOR=vim`
