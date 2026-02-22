# Checklist PR / CI — Arquivamento de Duplicatas (Lote 1/6)

Este checklist é destinado a revisar e validar PRs que movem arquivos duplicados para
`backend/archived_duplicates/modules/` e deixam stubs de compatibilidade. Inclua este
documento no PR (ou referencie-o) para orientar reviewers e o CI.

---

## 1. Objetivo

- Garantir que o arquivamento de arquivos duplicados preserve compatibilidade e seja
  seguro para merge.
- Minimizar blast radius usando lotes pequenos e validações automáticas no CI.

---

## 2. Verificações Locais (PR author)

- [ ] Confirmar commits: 1 commit por arquivo.
  - Comando: `git log --oneline -n 10`
- [ ] Listar arquivos arquivados e stubs
  - `ls -la backend/archived_duplicates/modules`
  - `ls -la backend/modules | grep -E 'address|appointments|auth|citizenship|commercial'`
- [ ] Verificação de import (PYTHONPATH temporário)
  - ```bash
    PYTHONPATH=backend /opt/sila-system/.venv/bin/python - <<'PY'
    import importlib
    names = [
      'backend.modules.address',
      'backend.modules.appointments',
      'backend.modules.auth',
      'backend.modules.citizenship',
      'backend.modules.commercial',
    ]
    for n in names:
        try:
            importlib.import_module(n)
            print(n, 'OK')
        except Exception as e:
            print(n, 'ERROR:', type(e).__name__, e)
    PY
    ```
  - Critério: imports sem `Exception` (warnings são aceitáveis).
- [ ] Lint/format rápido (opcional)
  - ` /opt/sila-system/.venv/bin/ruff check backend || true`
- [ ] Testes unitários/smoke (local)
  - ` /opt/sila-system/.venv/bin/python -m pytest -q -k "not integration" || true`
  - Documente falhas preexistentes no PR.

---

## 3. Conteúdo do PR (obrigatório)

- Título: `Fase 1: Arquivamento de Duplicatas (Lote 1/6)`.
- Corpo do PR:
  - Objetivo e escopo.
  - Lista dos commits (hash + mensagem).
  - Resultado da verificação de import local (copiar output relevante).
  - Riscos conhecidos (dependências, testes integration quebrados previamente).
  - Instruções de rollback.
- Anexar `reports/pr_cleanup_lote1.md` (gerado) como body ou referência.

---

## 4. Jobs de CI recomendados

Implemente os seguintes jobs em pipeline (em ordem curta e rápida → mais longa):

### 4.1 validate-check (rápido)

- Passos:
  - Instalar apenas dependências de lint/checagem (ex: ruff).
  - Executar linter e import-check (PYTHONPATH=backend).
- Comandos exemplo:
  ```bash
  python -m pip install ruff || true
  ruff check backend || true
  PYTHONPATH=backend python -c "import importlib; importlib.import_module('backend.modules.address')"
  ```
- Critério: import-check deve passar; linter pode dar warnings, não erros.

### 4.2 unit-tests / smoke

- Passos:
  - Executar testes rápidos e smoke tests (excluindo integrações pesadas).
- Comandos:
  ```bash
  python -m pytest -q -k "not integration"
  ```
- Critério: não introduzir novos failures.

### 4.3 dependency-scan

- Passos:
  - Executar `pip-audit` ou `safety` contra requirements (opcional neste PR, mas
    recomendado globalmente).

### 4.4 integration-tests (gated)

- Passos:
  - Rodar integrações em ambiente apropriado (staging/runner com infra).
- Observação: este job pode ser facultativo para o PR inicial se integrações forem
  custosas; porém, CI da branch de destino deve executar integrações antes de release.

---

## 5. Critérios de Merge

- Requer CI verde nos jobs obrigatórios (validate-check + unit-tests).
- Requer 1–2 approvals de reviewers com contexto.
- Preferência por manter commits separados (um commit por arquivo) para rastreabilidade.
- Merge via `merge commit` ou `rebase` conforme política do projeto — evite squash que
  apague histórico por arquivo, a menos que desejado.

---

## 6. Pós-merge (tarefas)

- Tag opcional do merge commit: `cleanup/lote-1`.
- Rodar pipeline completo em `main` (incluindo integrações) para garantir estabilidade.
- Planejar Lote 2 após CI e reviewers aprovarem e/ou eventuais correções aplicadas.

---

## 7. Rollback rápido

- Para reverter commits problemáticos:
  ```bash
  git checkout main
  git pull origin main
  git revert <commit-hash>
  git push origin main
  ```
- Para desfazer lote inteiro (testar localmente primeiro):
  ```bash
  git revert 9d2642e1..0fb2fab1
  ```

---

## 8. Checklist de aceitação (para reviewers)

- [ ] Commits claros (1 por arquivo).
- [ ] Import-check passou (CI log anexado).
- [ ] Lint/format sem novos erros.
- [ ] Unit tests/smoke sem novos failures.
- [ ] Dependências e riscos documentados.
- [ ] Plano de rollback claro.

---

Arquivo gerado automaticamente para a equipe de saneamento. Repita este fluxo para os
próximos lotes (5–10 arquivos por lote) para reduzir risco.
