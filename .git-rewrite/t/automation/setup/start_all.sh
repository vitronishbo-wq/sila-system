#!/usr/bin/env bash
# Define strict error checking: exit on error (-e), exit on unset variable (-u),
# exit if any command in a pipeline fails (-o pipefail).
set -euo pipefail

# Define o caminho absoluto para o arquivo docker-compose
COMPOSE_FILE="/opt/sila-system/devops/docker-compose.yml"

banner() {
  echo "=========================================================="
  echo "        🚀 SILA System - Docker Compose Orchestrator"
  echo "=========================================================="
  echo "  Arquivo Compose: $COMPOSE_FILE"
  echo "  Perfis Disponíveis: infra | backend | frontend | monitoring"
  echo "=========================================================="
}

# Inicia o banco de dados e o backend
start_backend() {
  echo "Iniciando Backend (db + backend) via perfis 'infra' e 'backend'..."
  # Certifica-se de que o db e o backend estão ativos e em modo daemon (-d)
  docker compose -f "$COMPOSE_FILE" --profile infra --profile backend up -d db backend
}

# Inicia o stack completo para desenvolvimento
start_frontend() {
  echo "Iniciando Stack Completo (db + backend + frontend) via perfis 'infra', 'backend' e 'frontend'..."
  # Inicia todos os serviços necessários para o frontend
  docker compose -f "$COMPOSE_FILE" --profile infra --profile backend --profile frontend up -d db backend frontend
}

# Inicia apenas a stack de monitoramento
start_monitoring() {
  echo "Iniciando Monitoramento (grafana + prometheus + node-exporter)..."
  docker compose -f "$COMPOSE_FILE" --profile infra up -d grafana prometheus node-exporter
}

# Inicia todos os serviços e reconstrói as imagens
start_full() {
  echo "Iniciando Full Stack e Reconstruindo Imagens..."
  # A flag --build garante que qualquer alteração nos Dockerfiles seja aplicada
  docker compose -f "$COMPOSE_FILE" --profile infra --profile backend --profile frontend up -d --build
}

# Derruba todos os serviços definidos no arquivo compose
stop_all() {
  echo "Parando e removendo todos os containers (docker compose down)..."
  docker compose -f "$COMPOSE_FILE" down
}

# Exibe o status atual dos containers
status() {
  echo "-------------------- STATUS --------------------"
  docker compose -f "$COMPOSE_FILE" ps
  echo "------------------------------------------------"
}

# Menu principal de interação
main_menu() {
  while true; do
    banner
    cat <<MENU
[1] Start Backend (db + backend)
[2] Start Frontend (db + backend + frontend)
[3] Start Monitoring (grafana + prometheus + node-exporter)
[4] Start Full Stack & Build Images (infra + backend + frontend)
[5] Stop All (compose down)
[6] Status (compose ps)
[0] Exit
MENU
    echo
    read -rp "Selecione uma opção: " opt
    echo

    case "$opt" in
      1) start_backend; status ;;
      2) start_frontend; status ;;
      3) start_monitoring; status ;;
      4) start_full; status ;;
      5) stop_all ;;
      6) status ;;
      0) exit 0 ;;
      *) echo "❌ Opção inválida. Tente novamente." ;;
    esac
    echo
  done
}

# Início da execução
main_menu
