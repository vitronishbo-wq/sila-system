# OPERATIONS_LOG

- 2025-10-15 04:30Z: Limpeza e regeneração de árvores (`docs/estrutura_arvore_*.txt`,
  `scripts/*_tree.md`).
- 2025-10-15 04:40Z: Ajustes em `devops/docker-compose.yml` (frontend context,
  environment backend, remoção de version).
- 2025-10-15 04:45Z: Porta Postgres alterada para `5433:5432` (host x container).
- 2025-10-15 04:50Z: `frontend/apps/web/nginx.conf` proxy `/api/` →
  `http://backend:8000/`.
- 2025-10-15 04:52Z: `backend/entrypoint.sh` porta Uvicorn `8000`; fix import
  `modules.citizenship.models.citizen`.
- 2025-10-15 04:56Z: Compose validado (`docker compose config`).
- 2025-10-15 05:05Z: Criação de perfis no Compose (`frontend`, `backend`, `infra`).
- 2025-10-15 05:10Z: Scripts criados:
  - `scripts/devops/start_monitoring.sh`
  - `scripts/backend/start_backend.sh`
  - `scripts/frontend/start_frontend.sh`
  - `scripts/start_all.sh`
- 2025-10-15 05:15Z: `COORDENACAO_EQUIPES.md` atualizado (perfis, scripts, atalhos
  `start_all.sh` e `start.sh`).
