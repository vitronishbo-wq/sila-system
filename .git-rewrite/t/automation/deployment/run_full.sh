#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="/opt/sila-system/devops/docker-compose.yml"

# Perfis: frontend + backend + infra
exec docker compose -f "$COMPOSE_FILE" --profile frontend --profile backend --profile infra up -d --build
