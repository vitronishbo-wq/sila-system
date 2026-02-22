#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="/opt/sila-system/devops/docker-compose.yml"

# Perfis: backend + infra
exec docker compose -f "$COMPOSE_FILE" --profile backend --profile infra up -d
