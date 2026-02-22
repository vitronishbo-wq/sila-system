# RUNBOOK_COMPOSE

## Objetivo

Guia rápido para subir, parar e verificar os serviços usando perfis do Docker Compose e
scripts de atalho.

## Arquivos e locais

- Compose: `devops/docker-compose.yml`
- Scripts:
  - Backend: `scripts/backend/start_backend.sh`
  - Frontend: `scripts/frontend/start_frontend.sh`
  - Monitoring: `scripts/devops/start_monitoring.sh`
  - Orquestrador: `scripts/start_all.sh`
  - Atalho raiz: `start.sh`

## Portas e serviços

- Backend API: `8000` (container `backend:8000` → host `8000`)
- Frontend (Nginx): `80`
- Postgres: host `5434` → container `5432` (serviço `db`)
- Prometheus: `9090`
- Grafana: `3000`

## Perfis

- `infra`: `db`, `prometheus`, `grafana`, `node-exporter`
- `backend`: `backend`
- `frontend`: `frontend`

## Subir ambientes (recomendado)

- Backend + Infra:

```bash
bash scripts/backend/start_backend.sh
```

- Frontend (+ Backend + Infra):

```bash
bash scripts/frontend/start_frontend.sh
```

- Monitoring (Infra):

```bash
bash scripts/devops/start_monitoring.sh
```

- Full stack via orquestrador:

```bash
bash scripts/start_all.sh
```

- Atalho raiz (menu):

```bash
sudo bash start.sh
```

## Comandos Compose equivalentes

- Backend + Infra:

```bash
docker compose -f devops/docker-compose.yml --profile backend --profile infra up -d backend db
```

- Frontend + Backend + Infra:

```bash
docker compose -f devops/docker-compose.yml --profile frontend --profile backend --profile infra up -d frontend backend db
```

- Monitoring (Infra):

```bash
docker compose -f devops/docker-compose.yml --profile infra up -d grafana prometheus node-exporter
```

- Full stack (build):

```bash
docker compose -f devops/docker-compose.yml --profile frontend --profile backend --profile infra up -d --build
```

## Checks de saúde

- Backend:

```bash
curl -sS http://localhost:8000/docs | head -n 1
```

- Frontend:

```bash
curl -sS -I http://localhost:80 | head -n 1
```

- DB (host exposto em 5434):

```bash
nc -zv 127.0.0.1 5434 || true
```

- Prometheus / Grafana:

```bash
curl -sS http://localhost:9090/-/healthy | cat
curl -sS http://localhost:3000/api/health | cat
```

## Variáveis e conexões

- `backend` recebe por Compose:
  - `DATABASE_URL=postgresql://postgres:postgres@db:5432/sila`
  - `ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/sila`
- Frontend Nginx (`frontend/apps/web/nginx.conf`):
  - `location /api/ { proxy_pass http://backend:8000/; }`

## Troubleshooting rápido

- Porta 5432 ocupada no host → foi ajustado para `5433:5432`. Use `5433` no host.
- Frontend “host not found” no Nginx → verifique se proxy aponta para `backend:8000`.
- Backend falha em migrar DB → confira `alembic` e se o DB `sila` existe (Compose cria o
  cluster; o schema é criado por alembic).
- Conflitos entre equipes → use os perfis e scripts de start para isolar execução.

## Observabilidade

- Acesse Prometheus: http://localhost:9090
- Acesse Grafana: http://localhost:3000 (credenciais padrão configuradas no Compose)

## Anexos

- Histórico de operações: `docs/OPERATIONS_LOG.md`
