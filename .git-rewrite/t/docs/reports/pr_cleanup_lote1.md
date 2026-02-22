Title: Fase 1: Arquivamento de Duplicatas (Lote 1/6)

Branch: cleanup/archived-duplicates

Descrição:

Este PR arquiva arquivos duplicados localizados em `backend/modules/*.py` que conflitam
com pacotes homônimos. Objetivo: remover ambiguidade de importação e preparar o código
para refatorações posteriores.

O que foi alterado (5 commits, um por arquivo):

- chore(cleanup): archive duplicate file backend/modules/commercial.py ->
  backend/archived_duplicates/modules/commercial.py; add compatibility stub (9d2642e1)
- chore(cleanup): archive duplicate file backend/modules/citizenship.py ->
  backend/archived_duplicates/modules/citizenship.py; add compatibility stub (b0eb13ec)
- chore(cleanup): archive duplicate file backend/modules/auth.py ->
  backend/archived_duplicates/modules/auth.py; add compatibility stub (b5428ecb)
- chore(cleanup): archive duplicate file backend/modules/appointments.py ->
  backend/archived_duplicates/modules/appointments.py; add compatibility stub (6e868871)
- chore(cleanup): archive duplicate file backend/modules/address.py ->
  backend/archived_duplicates/modules/address.py; add compatibility stub (0fb2fab1)

Notas de validação:

- Compatibilidade de importação para os módulos arquivados foi verificada localmente
  (import smoke check). Alguns módulos requerem dependências (ex: `fastapi`) para
  importar completamente.
- Este PR é Lote 1/6. Não foram feitas alterações ao código de serviços; apenas os
  arquivos duplicados foram movidos para `backend/archived_duplicates/modules/` e stubs
  de compatibilidade foram adicionados.

Checklist:

- [ ] Revisão de código
- [ ] Validar no CI (build completo + smoke tests)
- [ ] Merged quando CI verde

Instruções para CI/local:

- Este PR deve ser validado por CI com as dependências listadas em
  `backend/requirements.txt`.
- Para validação local rápida: instale `fastapi` no venv e execute um import-check:

  /opt/sila-system/.venv/bin/pip install fastapi /opt/sila-system/.venv/bin/python -c
  "import backend.modules.address, backend.modules.appointments, backend.modules.auth,
  backend.modules.citizenship, backend.modules.commercial; print('imports OK')"

-- Gerado automaticamente por processo de saneamento.
